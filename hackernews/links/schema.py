import graphene
from graphene_django import DjangoObjectType

from .models import Links

class LinkType(DjangoObjectType):
    """GraphQL type representation for the Links model.

    This class defines the GraphQL type for the Links model, allowing it to be queried and manipulated through GraphQL. 
    It inherits from DjangoObjectType to leverage Django's ORM capabilities for GraphQL integration.
    """
    class Meta:
        model = Links
        
class Query(graphene.ObjectType):
    """GraphQL query root type.

    This class defines the root query type for the GraphQL API. It includes a single field, 'links', which returns a list of all links.
    """
    links=graphene.List(LinkType)
    
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
        link = Links(url=url,description=description)
        link.save()
        
        return CreateLink(
            id=link.id, 
            url=link.url, 
            description=link.description
        )
            
class Mutation(graphene.ObjectType):
    """
    Mutation root type.

    This class defines the root mutation type for the GraphQL API. 
    It includes a single field, 'create_link', which creates a new link.
    """
    create_link = CreateLink.Field()


