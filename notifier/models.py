"""
Here are the related models definition for the `notifier` app.

## Models:
    - `Course` model, to abstract and store related info of each corse
    from KFUPM API identify by its `crn`.
        ### Fields:
            - `crn`: a pk
    - `TrackingList` model, to assign each users to what `Course` they are willing to track
        ### Fields:
            - `courses`
            - `user`

    - `NotificationEvent` model, to track the number, channel , and date of the notifications.
        ### Fields:
            - `user`
            - `channel`
            - `sent_on`
"""


from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django_choices_field import TextChoicesField
from multiselectfield import MultiSelectField

from data import DepartmentEnum

User = get_user_model()


class Term(models.Model):
    """
    A small model to store the allowed terms
    to be used in the notifier methods.
    """

    long = models.CharField(_("long"), max_length=10)
    short = models.CharField(_("short"), max_length=5)
    allowed = models.BooleanField(_("allowed"))

    class Meta:
        verbose_name = _("term")
        verbose_name_plural = _("terms")

    def __str__(self):
        return self.long


class Course(models.Model):
    """
    It abstracts and store related info of each corse from KFUPM API identify by its `crn`.
    pk: `crn`
    """

    crn = models.CharField(_("CRN"), max_length=5, unique=True)
    term = models.CharField(_("term"), max_length=6)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    last_updated = models.DateTimeField(_("last updated"), auto_now=True)
    available_seats = models.IntegerField(_("available seats"), default=0)
    raw = models.JSONField(_("raw info"), default=None, null=True)
    waiting_list_count = models.IntegerField(
        _("waiting list count"), default=0
    )
    department = TextChoicesField(
        verbose_name=_("department"), choices_enum=DepartmentEnum
    )

    class Meta:
        ordering = ["term", "department"]

    def __str__(self) -> str:
        return str(self.crn)


class ChannelEnum(models.TextChoices):
    """Choices of `channel` as Enum"""

    SMS = "sms", _("sms")
    PUSH = "push", _("push")
    EMAIL = "email", _("email")
    WHATSAPP = "whatsapp", _("whatsapp")
    TELEGRAM = "telegram", _("telegram")


class TrackingList(models.Model):
    """
    It assigns each users to what `Course` they are willing to track.
    pk: OneToOneField `user`.
    """

    user = models.OneToOneField(
        User,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="tracking_list",
    )
    courses = models.ManyToManyField(
        Course,
        verbose_name=_("courses"),
        related_name="tracked_courses",
        blank=True,
    )
    channels = MultiSelectField(
        choices=ChannelEnum.choices, default=ChannelEnum.EMAIL
    )


class NotificationEvent(models.Model):
    """
    It tracks the number, channels, and date of the sent notifications.
    """

    success = models.BooleanField(_("success"), default=True, blank=True)
    sent_on = models.DateTimeField(
        _("sent on"), auto_now=False, auto_now_add=True
    )
    course = models.ForeignKey(
        Course, verbose_name=_("course"), on_delete=models.CASCADE
    )
    to = models.ForeignKey(
        User, verbose_name=_("user"), on_delete=models.CASCADE
    )
    channel = models.CharField(
        _("channel"), max_length=50, choices=ChannelEnum.choices
    )
