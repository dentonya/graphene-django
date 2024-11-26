import graphene
from graphene_django import DjangoObjectType

from .models import Links, Vote
from users.schema import UserType

class LinkType(DjangoObjectType):
    """GraphQL type representation for the Links model.

    This class defines the GraphQL type for the Links model, allowing it to be queried and manipulated through GraphQL. 
    It inherits from DjangoObjectType to leverage Django's ORM capabilities for GraphQL integration.
    """
    class Meta:
        model = Links
        
class VoteType(DjangoObjectType):
    """GraphQL type representation for the Vote model.

    This class defines the GraphQL type for the Vote model, allowing it to be queried and manipulated through GraphQL. 
    It inherits from DjangoObjectType to leverage Django's ORM capabilities for GraphQL integration.
    """
    class Meta:
        model = Vote
        
class Query(graphene.ObjectType):
    """GraphQL query root type.

    This class defines the root query type for the GraphQL API. It includes a single field, 'links', which returns a list of all links.
    """
    links = graphene.List(LinkType)
    votes = graphene.List(VoteType)
    
    def resolve_links(self, info, **kwargs):
        """Retrieves all Link objects from the database.

        This resolver function is responsible for fetching all instances of the Links model. 
        It is typically used in GraphQL queries to provide a list of links to the client.

        Args:
            info: Information about the execution state of the query.

        Returns:
            QuerySet: A queryset containing all Link objects.
        """
        return Links.objects.all()
    
    def resolve_votes(self,info,**kwargs):
        """Retrieves all Vote objects from the database.

        This resolver function is responsible for fetching all instances of the Vote model. 
        It is typically used in GraphQL queries to provide a list of votes to the client.

        Args:
            info: Information about the execution state of the query.

        Returns:
            QuerySet: A queryset containing all Vote objects.
        """
        return Vote.objects.all()
    
class CreateLink(graphene.Mutation):
    """
    CreateLink is a GraphQL mutation for creating a new link entry. 
    It encapsulates the necessary fields for a link, including its identifier, URL, and description.

    Attributes:
        id (int): The unique identifier for the link.
        url (str): The URL of the link.
        description (str): A brief description of the link.
    """
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        """
        Arguments is a class that defines the input parameters for the CreateLink mutation. 
        It includes the URL and description of the link to be created.
        Data you send to the server.

        Attributes:
            url (str): The URL of the link.
            description (str): A brief description of the link.

        Methods:
            mutate(info, url, description):
                Creates a new link with the provided URL and description, 
                saving it to the database and returning the created link's details.
            
            Args:
                info: The GraphQL context information.
                url (str): The URL of the link to create.
                description (str): A brief description of the link to create.

            Returns:
                CreateLink: An instance containing the details of the created link.
        """
        url = graphene.String()
        description = graphene.String()
        
    def mutate(self,info,url,description):
        user = info.context.user or None
        link = Links(
            url=url,
            description=description,
            # associate the link with the current user if authenticated, or None if not.
            posted_by=user,  
        )
        link.save()
        
        return CreateLink(
            id=link.id, 
            url=link.url, 
            description=link.description,
            posted_by=link.posted_by
        )
            
class CreateVote(graphene.Mutation):
    """
    CreateVote is a GraphQL mutation that allows a logged-in user to cast a vote on a specific link. 
    It ensures that the user is authenticated and that the link exists before recording the vote.

    Attributes:
        user (UserType): The user who cast the vote.
        link (LinkType): The link that received the vote.

        Arguments:
            link_id (int): The identifier of the link on which the user is voting.

        Methods:
            mutate(info, link_id):
                Handles the voting logic, including user authentication and link validation, and creates a Vote record if the conditions are met.

        Args:
            info: The GraphQL context information.
            link_id (int): The ID of the link to vote on.

        Returns:
            CreateVote: An instance containing the user and link associated with the vote.

        Raises:
            Exception: If the user is not logged in or if the specified link is not found.
    """

    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)
    
    class Arguments:
        link_id = graphene.Int()
        
    def mutate(self, info, link_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("User must be logged in to vote.")
            
        link = Links.objects.filter(id=link_id).first()
        if not link:
            raise Exception("Link not found.")
        
        Vote.objects.get_or_create(
            user=user, 
            link=link
        )
        
        return CreateVote(user=user, link=link)
    
class Mutation(graphene.ObjectType):
    """
    Mutation root type.

    This class defines the root mutation type for the GraphQL API. 
    It includes a single field, 'create_link', which creates a new link.
    """
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()
    


