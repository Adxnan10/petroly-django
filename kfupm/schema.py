import graphene

import evaluation.schema
import account.schema
import forum.schema

class Query(evaluation.schema.Query, account.schema.Query, forum.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

class Mutation(evaluation.schema.Mutation, account.schema.Mutation, forum.schema.Mutation, graphene.ObjectType):

    pass


schema = graphene.Schema(query=Query, mutation=Mutation) 