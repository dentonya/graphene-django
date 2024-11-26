import graphene
import graphql_jwt
import links.schema
import users.schema

class Query(users.schema.Query,links.schema.Query,graphene.ObjectType):
    """Defines the root query for the GraphQL schema.

    This class serves as the entry point for all GraphQL queries in the application. 
    It inherits from the existing query class in the links schema and extends it with additional functionality as needed.
    """
    pass

class Mutation(users.schema.Mutation, links.schema.Mutation, graphene.ObjectType):
    """Defines the root mutation for the GraphQL schema.

    This class serves as the entry point for all GraphQL mutations in the application. 
    It inherits from the existing mutation class in the links schema and extends it with additional functionality as needed.
    """
    # used to authenticate the User with its username and password to obtain the JSON Web token.
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    # to confirm that the token is valid, passing it as an argument.
    verify_token = graphql_jwt.Verify.Field()
    # to generate a new token with the same user for expired tokens, 
    # passing the old token as an argument.
    refresh_token = graphql_jwt.Refresh.Field()
    

schema = graphene.Schema(query=Query, mutation=Mutation)
