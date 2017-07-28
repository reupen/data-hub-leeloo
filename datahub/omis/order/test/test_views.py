import pytest
from freezegun import freeze_time
from rest_framework import status
from rest_framework.reverse import reverse

from datahub.company.test.factories import AdviserFactory, CompanyFactory, ContactFactory
from datahub.core import constants
from datahub.core.test_utils import APITestMixin

from .factories import OrderFactory, OrderSubscriberFactory

# mark the whole module for db use
pytestmark = pytest.mark.django_db


class TestAddOrder(APITestMixin):
    """Add Order test case."""

    @freeze_time('2017-04-18 13:00:00.000000+00:00')
    def test_success(self):
        """Test a successful call to create an Order."""
        company = CompanyFactory()
        contact = ContactFactory(company=company)
        country = constants.Country.france.value

        url = reverse('api-v3:omis:order:list')
        response = self.api_client.post(
            url,
            {
                'company': {
                    'id': company.pk
                },
                'contact': {
                    'id': contact.pk
                },
                'primary_market': {
                    'id': country.id
                },
            },
            format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            'id': response.json()['id'],
            'reference': response.json()['reference'],
            'company': {
                'id': company.pk,
                'name': company.name
            },
            'contact': {
                'id': contact.pk,
                'name': contact.name
            },
            'primary_market': {
                'id': country.id,
                'name': country.name,
            }
        }

    def test_fails_if_contact_not_from_company(self):
        """
        Test that if the contact does not work at the company specified, the validation fails.
        """
        company = CompanyFactory()
        contact = ContactFactory()  # doesn't work at `company`
        country = constants.Country.france.value

        url = reverse('api-v3:omis:order:list')
        response = self.api_client.post(
            url,
            {
                'company': {
                    'id': company.pk
                },
                'contact': {
                    'id': contact.pk
                },
                'primary_market': {
                    'id': country.id
                }
            },
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            'contact': ['The contact does not work at the given company.']
        }

    def test_general_validation(self):
        """Test create an Order general validation."""
        url = reverse('api-v3:omis:order:list')
        response = self.api_client.post(url, {}, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            'company': ['This field is required.'],
            'contact': ['This field is required.'],
            'primary_market': ['This field is required.']
        }


class TestViewOrder(APITestMixin):
    """View order test case."""

    def test_get(self):
        """Test getting an existing order."""
        order = OrderFactory()

        url = reverse('api-v3:omis:order:detail', kwargs={'pk': order.pk})
        response = self.api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'id': order.id,
            'reference': order.reference,
            'company': {
                'id': str(order.company.id),
                'name': order.company.name
            },
            'contact': {
                'id': str(order.contact.id),
                'name': order.contact.name
            },
            'primary_market': {
                'id': str(order.primary_market.id),
                'name': order.primary_market.name
            }
        }

    def test_not_found(self):
        """Test 404 when getting a non-existing order"""
        url = reverse('api-v3:omis:order:detail', kwargs={
            'pk': '00000000-0000-0000-0000-000000000000'
        })
        response = self.api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestGetSubscriberList(APITestMixin):
    """Get subscriber list test case."""

    def test_empty(self):
        """
        Test that calling GET returns [] if no-one is subscribed.
        """
        order = OrderFactory()

        url = reverse(
            'api-v3:omis:order:subscriber-list',
            kwargs={'order_pk': order.id}
        )
        response = self.api_client.get(url, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_non_empty(self):
        """
        Test that calling GET returns the list of advisers subscribed to the order.
        """
        advisers = AdviserFactory.create_batch(3)
        order = OrderFactory()
        for adviser in advisers[:2]:
            OrderSubscriberFactory(order=order, adviser=adviser)

        url = reverse(
            'api-v3:omis:order:subscriber-list',
            kwargs={'order_pk': order.id}
        )
        response = self.api_client.get(url, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {
                'id': adviser.id,
                'first_name': adviser.first_name,
                'last_name': adviser.last_name,
                'dit_team': {
                    'id': str(adviser.dit_team.id),
                    'name': adviser.dit_team.name
                }
            }
            for adviser in advisers[:2]
        ]


class TestChangeSubscriberList(APITestMixin):
    """Change subscriber list test case."""

    def test_add_to_empty_list(self):
        """
        Test that calling PUT with new advisers adds them to the subscriber list.
        """
        advisers = AdviserFactory.create_batch(2)
        order = OrderFactory()

        url = reverse(
            'api-v3:omis:order:subscriber-list',
            kwargs={'order_pk': order.id}
        )

        response = self.api_client.put(
            url,
            [{'id': adviser.id} for adviser in advisers],
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        assert {adv['id'] for adv in response.json()} == {adv.id for adv in advisers}

    def test_change_existing_list(self):
        """
        Test that calling PUT with a different list of advisers completely changes
        the subscriber list:
        - advisers not in the list will be removed
        - new advisers will be added
        - existing advisers will be kept
        """
        previous_advisers = AdviserFactory.create_batch(2)
        order = OrderFactory()
        subscriptions = [
            OrderSubscriberFactory(order=order, adviser=adviser)
            for adviser in previous_advisers
        ]

        final_advisers = [
            AdviserFactory(),  # new
            previous_advisers[1]  # existing
        ]

        url = reverse(
            'api-v3:omis:order:subscriber-list',
            kwargs={'order_pk': order.id}
        )
        response = self.api_client.put(
            url,
            [{'id': adviser.id} for adviser in final_advisers],
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        assert {adv['id'] for adv in response.json()} == {adv.id for adv in final_advisers}

        # check that the id of the existing subscription didn't change
        assert order.subscribers.filter(id=subscriptions[1].id).exists()

    def test_remove_all(self):
        """
        Test that calling PUT with an empty list, removes all the subscribers.
        """
        advisers = AdviserFactory.create_batch(2)
        order = OrderFactory()
        for adviser in advisers:
            OrderSubscriberFactory(order=order, adviser=adviser)

        url = reverse(
            'api-v3:omis:order:subscriber-list',
            kwargs={'order_pk': order.id}
        )
        response = self.api_client.put(url, [], format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_invalid_adviser(self):
        """
        Test that calling PUT with an invalid adviser returns 400.
        """
        advisers = AdviserFactory.create_batch(2)
        order = OrderFactory()

        url = reverse(
            'api-v3:omis:order:subscriber-list',
            kwargs={'order_pk': order.id}
        )

        data = [{'id': adviser.id} for adviser in advisers]
        data.append({
            'id': '00000000-0000-0000-0000-000000000000'
        })

        response = self.api_client.put(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == [
            {}, {}, {'id': ['00000000-0000-0000-0000-000000000000 is not a valid adviser']}
        ]