from datahub.interaction.models import ServiceDelivery
from datahub.v2.serializers.service_deliveries import ServiceDeliverySchema

DEFAULT = object()


def build_relationship(model_instance, attribute):
    mapping = {
        'company': 'Company',
        'contact': 'Contact',
        'country': 'Country',
        'dit_advisor': 'Advisor',
        'dit_team': 'Team',
        'sector': 'Sector',
        'service': 'Service',
        'status': 'Status',
        'uk_region': 'UKRegion'
    }
    entity_name = mapping[attribute]
    data_dict = {'data': {'type': entity_name, 'id': str(model_instance.pk)}}
    return data_dict


def model_to_json_api(model_instance):
    attributes = dict()
    relationships = dict()
    for item in ServiceDeliverySchema():
        if item.name == 'attributes':
            for subitem in item:
                attributes[subitem.name] = getattr(model_instance, subitem.name, None)
        elif item.name == 'relationships':
            for subitem in item:
                relationship_instance = getattr(model_instance, subitem.name, None)
                if relationship_instance:
                    relationships[subitem.name] = build_relationship(relationship_instance, subitem.name)
    return {'attributes': attributes, 'relationships': relationships}


class ServiceDeliveryDatabaseRepo:
    """DB repo."""

    def __init__(self, config=None):
        """Initialise the repo using the config."""
        self.model = ServiceDelivery
        self.schema = ServiceDeliverySchema

    def get(self, object_id):
        """Get and return a single object by its id."""
        try:
            model_instance = self.model.objects.get(id=object_id)
            return model_to_json_api(model_instance)
        except self.model.DoesNotExist:
            return {}

    def filter(self, company_id=DEFAULT, contact_id=DEFAULT, offset=0, limit=100):
        """Filter objects."""
        queryset = self.model.objects
        if company_id:
            queryset.filter(company__pk=company_id)
        if contact_id:
            queryset.filter(contact__pk=contact_id)
        return self.schema(queryset.all(), many=True).data

    def upsert(self, data, user):
        """Insert or update an object."""
        obj_id = data.pop('id')
        obj, _ = self.model.objects.update_or_create(
            pk=obj_id,
            defaults=data
        )
        return self.schema(obj).data
