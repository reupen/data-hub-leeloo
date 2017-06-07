from django.conf import settings
from rest_framework import serializers

from datahub.company.models import Advisor, Company
from datahub.core.serializers import NestedRelatedField
from datahub.core.validate_utils import UpdatedDataView
from datahub.leads.models import BusinessLead
from datahub.metadata import models as meta_models

NAME_REQUIRED_MESSAGE = 'Company name or first name and last name required'
CONTACT_REQUIRED_MESSAGE = 'Email address or phone number required'


class BusinessLeadSerializer(serializers.ModelSerializer):
    """Business lead serialiser."""

    company = NestedRelatedField(
        Company, required=False, allow_null=True
    )
    adviser = NestedRelatedField(
        Advisor, read_only=True,
        extra_fields=('first_name', 'last_name')
    )
    address_country = NestedRelatedField(
        meta_models.Country, required=False, allow_null=True
    )
    archived = serializers.BooleanField(read_only=True)
    archived_on = serializers.DateTimeField(read_only=True)
    archived_reason = serializers.CharField(read_only=True)
    archived_by = NestedRelatedField(
        settings.AUTH_USER_MODEL, read_only=True,
        extra_fields=('first_name', 'last_name')
    )

    def validate(self, data):
        """
        Performs cross-field validation after individual fields have been
        validated.

        Ensures that either a person or company name has been provided,
        as well as an email address or phone number.
        """
        errors = {}
        data_view = UpdatedDataView(self.instance, data)
        company_name = data_view.get_value('company_name')
        trading_name = data_view.get_value('trading_name')
        company = data_view.get_value('company')
        first_name = data_view.get_value('first_name')
        last_name = data_view.get_value('last_name')
        telephone_number = data_view.get_value('telephone_number')
        email = data_view.get_value('email')

        has_company_name = any((company_name, company, trading_name))
        has_contact_name = first_name and last_name

        if not (has_company_name or has_contact_name):
            errors['company_name'] = NAME_REQUIRED_MESSAGE
            errors['first_name'] = NAME_REQUIRED_MESSAGE
            errors['last_name'] = NAME_REQUIRED_MESSAGE

        if not (email or telephone_number):
            errors['telephone_number'] = CONTACT_REQUIRED_MESSAGE
            errors['email'] = CONTACT_REQUIRED_MESSAGE

        if errors:
            raise serializers.ValidationError(errors)

        return data

    class Meta:  # noqa: D101
        model = BusinessLead
        fields = (
            'id', 'first_name', 'last_name', 'job_title', 'company_name',
            'trading_name', 'company', 'adviser', 'telephone_number', 'email',
            'address_1', 'address_2', 'address_town', 'address_county',
            'address_country', 'address_postcode', 'telephone_alternative',
            'email_alternative', 'contactable_by_dit',
            'contactable_by_dit_partners', 'contactable_by_email',
            'contactable_by_phone', 'notes', 'archived', 'archived_on',
            'archived_reason', 'archived_by'
        )
        extra_kwargs = {
            'adviser': {'read_only': True},
            'archived': {'read_only': True},
            'archived_on': {'read_only': True},
            'archived_reason': {'read_only': True},
            'archived_by': {'read_only': True}
        }