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


