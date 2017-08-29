import pytest

from django.conf import settings

from datahub.interaction.test.factories import InteractionFactory
from datahub.investment.test.factories import InvestmentProjectFactory
from datahub.search.interaction.apps import InteractionSearchApp

pytestmark = pytest.mark.django_db


def test_new_interaction_synced(setup_es):
    """Test that new interactions are synced to ES."""
    interaction = InteractionFactory()
    setup_es.indices.refresh()

    assert setup_es.get(
        index=settings.ES_INDEX,
        doc_type=InteractionSearchApp.name,
        id=interaction.pk
    )


def test_updated_interaction_synced(setup_es):
    """Test that when an interaction is updated it is synced to ES."""
    interaction = InteractionFactory()
    new_subject = 'pluto'
    interaction.subject = new_subject
    interaction.save()
    setup_es.indices.refresh()

    result = setup_es.get(
        index=settings.ES_INDEX,
        doc_type=InteractionSearchApp.name,
        id=interaction.pk
    )
    assert result['_source']['subject'] == new_subject


def test_updating_company_name_updates_interaction(setup_es):
    """Test that when a company name is updated, the company's interactions are synced to ES."""
    interaction = InteractionFactory()
    new_company_name = 'exogenous'
    interaction.company.name = new_company_name
    interaction.company.save()
    setup_es.indices.refresh()

    result = setup_es.get(
        index=settings.ES_INDEX,
        doc_type=InteractionSearchApp.name,
        id=interaction.pk
    )
    assert result['_source']['company']['name'] == new_company_name


def test_updating_contact_name_updates_interaction(setup_es):
    """Test that when a contact's name is updated, the contact's interactions are synced to ES."""
    interaction = InteractionFactory()
    new_first_name = 'Jamie'
    new_last_name = 'Bloggs'
    interaction.contact.first_name = new_first_name
    interaction.contact.last_name = new_last_name
    interaction.contact.save()
    setup_es.indices.refresh()

    result = setup_es.get(
        index=settings.ES_INDEX,
        doc_type=InteractionSearchApp.name,
        id=interaction.pk
    )
    assert result['_source']['contact'] == {
        'id': str(interaction.contact.id),
        'first_name': new_first_name,
        'last_name': new_last_name,
        'name': f'{new_first_name} {new_last_name}',
    }


def test_updating_project_name_updates_interaction(setup_es):
    """
    Test that when an investment project's name is updated, the project's interactions are
    synced to ES.
    """
    project = InvestmentProjectFactory()
    interaction = InteractionFactory(
        investment_project=project
    )
    new_project_name = 'helios'
    project.name = new_project_name
    project.save()
    setup_es.indices.refresh()

    result = setup_es.get(
        index=settings.ES_INDEX,
        doc_type=InteractionSearchApp.name,
        id=interaction.pk
    )
    assert result['_source']['investment_project']['name'] == new_project_name