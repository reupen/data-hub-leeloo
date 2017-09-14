import csv
from unittest import mock

import pytest
from django.utils.text import slugify
from rest_framework import status
from rest_framework.reverse import reverse

from datahub.company.test.factories import CompanyFactory
from datahub.core import constants
from datahub.core.test_utils import APITestMixin

pytestmark = pytest.mark.django_db


@pytest.fixture
def setup_data():
    """Sets up data for the tests."""
    country_uk = constants.Country.united_kingdom.value.id
    country_us = constants.Country.united_states.value.id
    CompanyFactory(
        name='abc defg ltd',
        trading_address_1='1 Fake Lane',
        trading_address_town='Downtown',
        trading_address_country_id=country_uk
    )
    CompanyFactory(
        name='abc defg us ltd',
        trading_address_1='1 Fake Lane',
        trading_address_town='Downtown',
        trading_address_country_id=country_us,
        registered_address_country_id=country_us
    )


class TestSearch(APITestMixin):
    """Tests search views."""

    def test_search_company(self, setup_es, setup_data):
        """Tests detailed company search."""
        setup_es.indices.refresh()

        term = 'abc defg'

        url = reverse('api-v3:search:company')
        united_states_id = constants.Country.united_states.value.id

        response = self.api_client.post(url, {
            'original_query': term,
            'trading_address_country': united_states_id,
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['trading_address_country']['id'] == united_states_id

    def test_company_search_paging(self, setup_es, setup_data):
        """Tests pagination of results."""
        setup_es.indices.refresh()

        url = reverse('api-v3:search:company')
        response = self.api_client.post(url, {
            'original_query': '',
            'offset': 1,
            'limit': 1,
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] > 1
        assert len(response.data['results']) == 1

    def test_company_search_paging_query_params(self, setup_es, setup_data):
        """Tests pagination of results."""
        setup_es.indices.refresh()

        url = f"{reverse('api-v3:search:company')}?offset=1&limit=1"
        response = self.api_client.post(url, {
            'original_query': '',
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] > 1
        assert len(response.data['results']) == 1

    @mock.patch('datahub.search.views.elasticsearch.apply_aggs_query')
    def test_company_search_no_aggregations(self, apply_aggs_query, setup_es, setup_data):
        """Tests if no aggregation occurs."""
        setup_es.indices.refresh()

        url = reverse('api-v3:search:company')
        response = self.api_client.post(url, {
            'original_query': '',
        })

        assert apply_aggs_query.call_count == 0

        assert response.status_code == status.HTTP_200_OK
        assert 'aggregations' not in response.data

    def test_search_company_no_filters(self, setup_es, setup_data):
        """Tests case where there is no filters provided."""
        setup_es.indices.refresh()

        url = reverse('api-v3:search:company')
        response = self.api_client.post(url, {})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0

    def test_search_foreign_company_json(self, setup_es, setup_data):
        """Tests detailed company search."""
        setup_es.indices.refresh()

        url = reverse('api-v3:search:company')

        response = self.api_client.post(url, {
            'uk_based': False,
        }, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['uk_based'] is False


class TestBasicSearch(APITestMixin):
    """Tests basic search view."""

    def test_all_companies(self, setup_es, setup_data):
        """Tests basic aggregate all companies query."""
        setup_es.indices.refresh()

        term = ''

        url = reverse('api-v3:search:basic')
        response = self.api_client.get(url, {
            'term': term,
            'entity': 'company'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] > 0

    def test_companies(self, setup_es, setup_data):
        """Tests basic aggregate companies query."""
        setup_es.indices.refresh()

        term = 'abc defg'

        url = reverse('api-v3:search:basic')
        response = self.api_client.get(url, {
            'term': term,
            'entity': 'company'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2
        assert response.data['results'][0]['name'].startswith(term)
        assert [{'count': 2, 'entity': 'company'}] == response.data['aggregations']

    def test_no_results(self, setup_es, setup_data):
        """Tests case where there should be no results."""
        setup_es.indices.refresh()

        term = 'there-should-be-no-match'

        url = reverse('api-v3:search:basic')
        response = self.api_client.get(url, {
            'term': term,
            'entity': 'company'
        })

        assert response.data['count'] == 0

    def test_companies_no_term(self, setup_es, setup_data):
        """Tests case where there is not term provided."""
        setup_es.indices.refresh()

        url = reverse('api-v3:search:basic')
        response = self.api_client.get(url, {})

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestSearchExport(APITestMixin):
    """Tests search export views."""

    def test_company_export(self, setup_es, setup_data):
        """Tests export of detailed company search."""
        setup_es.indices.refresh()

        term = 'abc defg'

        url = reverse('api-v3:search:company-export')
        united_states_id = constants.Country.united_states.value.id

        response = self.api_client.post(url, {
            'original_query': term,
            'trading_address_country': united_states_id,
        })

        assert response.status_code == status.HTTP_200_OK

        filename = slugify(term)

        # checks if filename includes our search term
        assert filename in response['Content-Disposition']

        csv_file = csv.DictReader(line.decode('utf-8') for line in response.streaming_content)

        rows = list(csv_file)

        assert len(rows) == 1

        # checks if we have alphabetically ordered headers in the CSV file
        assert ['account_manager',
                'alias',
                'archived',
                'archived_by',
                'archived_on',
                'archived_reason',
                'business_type',
                'classification',
                'companies_house_data',
                'company_number',
                'contacts',
                'created_on',
                'description',
                'employee_range',
                'export_to_countries',
                'future_interest_countries',
                'headquarter_type',
                'id',
                'modified_on',
                'name',
                'one_list_account_owner',
                'parent',
                'registered_address_1',
                'registered_address_2',
                'registered_address_country',
                'registered_address_county',
                'registered_address_postcode',
                'registered_address_town',
                'sector',
                'trading_address_1',
                'trading_address_2',
                'trading_address_country',
                'trading_address_county',
                'trading_address_postcode',
                'trading_address_town',
                'turnover_range',
                'uk_based',
                'uk_region',
                'website'] == csv_file.fieldnames

        # checks if we have a company we look for in the CSV file
        assert 'abc defg' in rows[0]['name']
        assert 'United States' in rows[0]['trading_address_country']
