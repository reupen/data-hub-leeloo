from datahub.company.models import CompaniesHouseCompany as DBCompaniesHouseCompany
from datahub.search.apps import SearchApp
from datahub.search.companieshousecompany.models import CompaniesHouseCompany
from datahub.search.companieshousecompany.views import SearchCompaniesHouseCompanyAPIView


class CompaniesHouseCompanySearchApp(SearchApp):
    """SearchApp for companies house companies."""

    name = 'companieshousecompany'
    es_model = CompaniesHouseCompany
    view = SearchCompaniesHouseCompanyAPIView
    view_permissions = ('company.read_companieshousecompany',)
    queryset = DBCompaniesHouseCompany.objects.select_related(
        'registered_address_country',
    )
