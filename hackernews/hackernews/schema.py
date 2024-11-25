import graphene
import links.schema

class Query(links.schema.Query,graphene.ObjectType):
    """Defines the root query for the GraphQL schema.

    This class serves as the entry point for all GraphQL queries in the application. 
    It inherits from the existing query class in the links schema and extends it with additional functionality as needed.
    """
    pass
schema = graphene.Schema(query=Query)