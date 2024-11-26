from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType

class UserType(DjangoObjectType):
    """GraphQL type representation for the User model.

    This class defines the GraphQL type for the User model, allowing it to be queried and manipulated through GraphQL. 
    It inherits from DjangoObjectType to leverage Django's ORM capabilities for GraphQL integration.
    """
    class Meta:
        model = get_user_model()
                
class CreateUser(graphene.Mutation):
    """GraphQL mutation for creating a new User.

    This mutation allows clients to create a new User in the database. 
    It takes in the required fields (username, email, and password) and returns the newly created User.
    """
    user = graphene.Field(UserType)
    
    class Arguments:
        """
        Arguments is a class that defines the input parameters required for user-related mutations in a GraphQL API. It includes fields for the username, password, and email, all of which are mandatory for creating or updating a user.

        Attributes:
            username (str): The unique username for the user, required for user creation.
            password (str): The password for the user account, required for user creation.
            email (str): The email address of the user, required for user creation.
        """

        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        
    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username, 
            email=email, 
            password=password
        )
        user.set_password(password)
        user.save()
        
        return CreateUser(user=user)
class Mutation(graphene.ObjectType):
    """Defines the root mutation for the GraphQL schema.

    This class serves as the entry point for all GraphQL mutations in the application. 
    It inherits from the existing mutation class in the users schema and extends it with additional functionality as needed.
    """
    create_user = CreateUser.Field()
    
class Query(graphene.ObjectType):
    """Defines the root query for the GraphQL schema.

    This class serves as the entry point for all GraphQL queries in the application. 
    It includes a single field, 'user', which returns the details of a specific user.
    """
    users = graphene.List(UserType)
    
    def resolve_users(self, info, **kwargs):
        """Retrieves all User objects from the database."""
        return get_user_model().objects.all()