from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from .registry import registry


def _create_metadata_view(mapping):
    attrs = {
        'authentication_classes': (),
        'filter_backends': (DjangoFilterBackend,) if mapping.filter_fields else (),
        'filter_fields': mapping.filter_fields,
        'pagination_class': None,
        'permission_classes': (),
        'queryset': mapping.queryset,
        'serializer_class': mapping.serializer,
    }

    view_set = type(
        f'{mapping.model.__name__}ViewSet',
        (GenericViewSet, ListModelMixin),
        attrs,
    )

    return view_set.as_view({
        'get': 'list'
    })


urls_args = []

# programmatically generate metadata views
for name, mapping in registry.mappings.items():
    view = _create_metadata_view(mapping)
    path = f'{name}/'
    urls_args.append(((path, view), {'name': name}))
