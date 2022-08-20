"""
A django custom command to start the Notifier checking.
"""

import time
import signal
import logging
import warnings

from django_q.tasks import async_task
from django.core.cache import CacheKeyWarning
from django.core.management.base import BaseCommand

from notifier.utils import check_changes, collect_tracked_courses

warnings.simplefilter('ignore', CacheKeyWarning)
warnings.simplefilter('ignore', DeprecationWarning)

# setting up the logger
logger = logging.getLogger(__name__)


class GracefulKiller:
    """To catch SIGINT $ SIGTERM signals
    then exit gracefully."""

    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        self.kill_now = True


class Command(BaseCommand):
    """a command that get in infinite loop of checking"""

    help = "Start checking and notifying the courses"

    def handle(self, *args, **options):
        """Check all tracked courses
        and grouped the notification by user
        then send a notification details

        This method is infinite loop,
        it should be called from a async context.

        return: the structure is
        {
            'user1_pk': [
                    {
                        'course1': <Course1>,
                        'status': {
                            'available_seats': 0
                            'waiting_list_count': 0
                            'available_seats_old': 0
                            'waiting_list_count_old': 0
                        }
                    },
                ], ...
            'user2_pk': ...,
        }
        """

        logger.info("Starting the Notifier Checking")
        killer = GracefulKiller()

        while not killer.kill_now:
            t_start = time.perf_counter()

            collection = collect_tracked_courses()
            changed_courses = []

            for _, value in collection.items():
                changed, status = check_changes(value["course"])

                if changed:
                    value["status"] = status
                    changed_courses.append(value)

            # group `changed_courses` by unique trackers
            courses_by_tracker = {}
            for c in changed_courses:
                for tracker in c["trackers"]:
                    try:
                        courses_by_tracker[tracker.pk].append(
                            {
                                "course_pk": c["course"].pk,
                                "status": c["status"],
                            }
                        )
                    except KeyError:
                        courses_by_tracker[tracker.pk] = [
                            {
                                "course_pk": c["course"].pk,
                                "status": c["status"],
                            }
                        ]

            for tracker_pk, info in courses_by_tracker.items():
                async_task(
                    "notifier.utils.send_notification",
                    tracker_pk,
                    str(info),
                )

            # log execution time
            logger.info(
                "Courses changes checked within %0.4f",
                time.perf_counter() - t_start,
            )

            time.sleep(5)

        logger.info("Stopping the Notifier Checking.")
