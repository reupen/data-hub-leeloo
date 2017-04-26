from rest_framework import serializers

import datahub.metadata.models as meta_models
from datahub.company.models import Advisor, Company, Contact
from datahub.core.serializers import NestedRelatedField
from datahub.investment.models import InvestmentProject


class IProjectSerializer(serializers.ModelSerializer):
    """Serialiser for investment project endpoints."""

    investment_type = NestedRelatedField(meta_models.InvestmentType)
    phase = NestedRelatedField(meta_models.InvestmentProjectPhase)
    investor_company = NestedRelatedField(
        Company, required=False, allow_null=True
    )
    intermediate_company = NestedRelatedField(
        Company, required=False, allow_null=True
    )
    investment_recipient_company = NestedRelatedField(
        Company, required=False, allow_null=True
    )
    client_contacts = NestedRelatedField(Contact, many=True, required=False)

    client_relationship_manager = NestedRelatedField(
        Advisor, required=False, allow_null=True,
        extra_fields=('first_name', 'last_name')
    )
    referral_source_advisor = NestedRelatedField(
        Advisor, required=False, allow_null=True,
        extra_fields=('first_name', 'last_name')
    )
    referral_source_activity = NestedRelatedField(
        meta_models.ReferralSourceActivity, required=False, allow_null=True
    )
    referral_source_activity_website = NestedRelatedField(
        meta_models.ReferralSourceWebsite, required=False, allow_null=True
    )
    referral_source_activity_marketing = NestedRelatedField(
        meta_models.ReferralSourceMarketing, required=False, allow_null=True
    )
    referral_source_activity_event = NestedRelatedField(
        meta_models.Event, required=False, allow_null=True
    )
    fdi_type = NestedRelatedField(
        meta_models.FDIType, required=False, allow_null=True
    )
    non_fdi_type = NestedRelatedField(
        meta_models.NonFDIType, required=False, allow_null=True
    )
    sector = NestedRelatedField(
        meta_models.Sector, required=False, allow_null=True
    )
    business_activity = NestedRelatedField(
        meta_models.InvestmentBusinessActivity, many=True, required=False
    )

    class Meta:  # noqa: D101
        model = InvestmentProject
        fields = (
            'id', 'name', 'project_code', 'description', 'document_link',
            'nda_signed', 'estimated_land_date', 'project_shareable',
            'anonymous_description', 'not_shareable_reason',
            'investment_type', 'phase', 'investor_company',
            'intermediate_company', 'investment_recipient_company',
            'client_contacts', 'client_relationship_manager',
            'referral_source_advisor', 'referral_source_activity',
            'referral_source_activity_website',
            'referral_source_activity_marketing',
            'referral_source_activity_event', 'fdi_type', 'non_fdi_type',
            'sector', 'business_activity'
        )


class IProjectValueSerializer(serializers.ModelSerializer):
    """Serialiser for investment project value objects."""

    class Meta:  # noqa: D101
        model = InvestmentProject
        fields = (
            'total_investment', 'foreign_equity_investment',
            'government_assistance', 'number_new_jobs',
            'number_safeguarded_jobs', 'r_and_d_budget',
            'non_fdi_r_and_d_budget', 'new_tech_to_uk', 'export_revenue'
        )


class IProjectRequirementsSerializer(serializers.ModelSerializer):
    """Serialiser for investment project requirements objects."""

    competitor_countries = NestedRelatedField(
        meta_models.Country, many=True, required=False
    )
    uk_region_locations = NestedRelatedField(
        meta_models.UKRegion, many=True, required=False
    )
    strategic_drivers = NestedRelatedField(
        meta_models.InvestmentStrategicDriver, many=True, required=False
    )

    class Meta:  # noqa: D101
        model = InvestmentProject
        fields = (
            'client_requirements', 'site_decided', 'address_line_1',
            'address_line_2', 'address_line_3', 'address_line_postcode',
            'competitor_countries', 'uk_region_locations',
            'strategic_drivers'
        )
