"""Company views URL config."""

from django.conf.urls import url

from .views import OrderViewSet


order_collection = OrderViewSet.as_view({
    'post': 'create'
})

order_item = OrderViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    url(r'^order$', order_collection, name='list'),
    url(r'^order/(?P<pk>[0-9a-z-]{36})$', order_item, name='detail'),
]
