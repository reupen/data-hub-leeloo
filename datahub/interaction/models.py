import uuid

from django.conf import settings
from django.db import models
from model_utils import Choices

from datahub.core import reversion
from datahub.core.models import BaseConstantModel, BaseModel, BaseOrderedConstantModel
from datahub.core.utils import StrEnum

MAX_LENGTH = settings.CHAR_FIELD_MAX_LENGTH


class InteractionPermission(StrEnum):
    """
    Permission codename constants.

    (Defined here rather than in permissions to avoid an import of that module.)


    The following codenames mean that the user can read, change, add or delete any type of
    interaction:

    read_all_interaction
    change_all_interaction
    add_all_interaction
    delete_interaction


    The following codenames mean that the user can only read, change and add interactions for
    investment projects that they are associated with:

    read_associated_investmentproject_interaction
    change_associated_investmentproject_interaction
    add_associated_investmentproject_interaction

    They cannot read, change or add interactions that do not relate to an investment project.

    An associated project has the same meaning that it does in investment projects (that is a
    project that was created by an adviser in the same team, or an adviser in the same team has
    been linked to the project).


    Note that permissions on other models are independent of permissions on interactions. Also
    note that if both *_all_* and *_associated_investmentproject_* permissions are assigned to the
    same user,  the *_all_* permission will be the effective one.

    The following permissions grant users additional permissions to manage policy-feedback
    interactions:

    read_policy_feedback_interaction
    change_policy_feedback_interaction
    add_policy_feedback_interaction

    These are not effective without the standard *_all permissions.
    """

    read_all = 'read_all_interaction'
    read_associated_investmentproject = 'read_associated_investmentproject_interaction'
    read_policy_feedback = 'read_policy_feedback_interaction'
    change_all = 'change_all_interaction'
    change_associated_investmentproject = 'change_associated_investmentproject_interaction'
    change_policy_feedback = 'change_policy_feedback_interaction'
    add_all = 'add_all_interaction'
    add_associated_investmentproject = 'add_associated_investmentproject_interaction'
    add_policy_feedback = 'add_policy_feedback_interaction'
    delete = 'delete_interaction'
    export = 'export_interaction'


class CommunicationChannel(BaseConstantModel):
    """Communication channel/mode of communication."""


class ServiceDeliveryStatus(BaseOrderedConstantModel):
    """
    Status of a service delivery.

    Primarily used for Tradeshow Access Programme (TAP) grants.
    """


class PolicyArea(BaseOrderedConstantModel):
    """
    Policy area for a policy feedback interaction.
    """


class PolicyIssueType(BaseOrderedConstantModel):
    """
    Policy issue type for a policy feedback interaction.
    """


@reversion.register_base_model()
class Interaction(BaseModel):
    """Interaction."""

    # Note: Kinds should also be added to _KIND_PERMISSION_MAPPING in the permissions module
    KINDS = Choices(
        ('interaction', 'Interaction'),
        ('service_delivery', 'Service delivery'),
        ('policy_feedback', 'Policy feedback'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    kind = models.CharField(max_length=MAX_LENGTH, choices=KINDS)
    date = models.DateTimeField()
    company = models.ForeignKey(
        'company.Company',
        related_name="%(class)ss",  # noqa: Q000
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    contact = models.ForeignKey(
        'company.Contact',
        related_name="%(class)ss",  # noqa: Q000
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    event = models.ForeignKey(
        'event.Event',
        related_name="%(class)ss",  # noqa: Q000
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='For service deliveries only.'
    )
    service = models.ForeignKey(
        'metadata.Service', blank=True, null=True, on_delete=models.SET_NULL
    )
    subject = models.TextField()
    dit_adviser = models.ForeignKey(
        'company.Advisor',
        related_name="%(class)ss",  # noqa: Q000
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    notes = models.TextField(max_length=settings.CDMS_TEXT_MAX_LENGTH, blank=True)
    dit_team = models.ForeignKey(
        'metadata.Team', blank=True, null=True, on_delete=models.SET_NULL
    )
    communication_channel = models.ForeignKey(
        'CommunicationChannel', blank=True, null=True,
        on_delete=models.SET_NULL,
        help_text='For interactions only.',
    )
    investment_project = models.ForeignKey(
        'investment.InvestmentProject',
        related_name="%(class)ss",  # noqa: Q000
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text='For interactions only.',
    )
    archived_documents_url_path = models.CharField(
        max_length=MAX_LENGTH, blank=True,
        help_text='Legacy field. File browser path to the archived documents for this interaction.'
    )
    service_delivery_status = models.ForeignKey(
        'ServiceDeliveryStatus', blank=True, null=True, on_delete=models.PROTECT,
        verbose_name='status',
        help_text='For service deliveries only.'
    )
    grant_amount_offered = models.DecimalField(
        null=True, blank=True, max_digits=19, decimal_places=2,
        help_text='For service deliveries only.',
    )
    net_company_receipt = models.DecimalField(
        null=True, blank=True, max_digits=19, decimal_places=2,
        help_text='For service deliveries only.',
    )
    policy_areas = models.ManyToManyField(
        'PolicyArea',
        blank=True,
        help_text='For policy feedback only.',
        related_name='interactions',
    )
    policy_issue_type = models.ForeignKey(
        'PolicyIssueType',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        help_text='For policy feedback only.',
        related_name='interactions',
    )

    @property
    def is_event(self):
        """Whether this service delivery is for an event."""
        if self.kind == self.KINDS.service_delivery:
            return bool(self.event)
        return None

    def __str__(self):
        """Human-readable representation."""
        return self.subject

    class Meta:
        indexes = [
            models.Index(fields=['-date', '-created_on']),
        ]
        permissions = (
            (
                InteractionPermission.read_all.value,
                'Can read all interaction'
            ),
            (
                InteractionPermission.read_associated_investmentproject.value,
                'Can read interaction for associated investment projects'
            ),
            (
                InteractionPermission.add_associated_investmentproject.value,
                'Can add interaction for associated investment projects'
            ),
            (
                InteractionPermission.change_associated_investmentproject.value,
                'Can change interaction for associated investment projects'
            ),
            (
                InteractionPermission.read_policy_feedback.value,
                'Can read policy feedback interaction'
            ),
            (
                InteractionPermission.add_policy_feedback.value,
                'Can add policy feedback interaction'
            ),
            (
                InteractionPermission.change_policy_feedback.value,
                'Can change policy feedback interaction'
            ),
            (
                InteractionPermission.export.value,
                'Can export interaction'
            ),
        )
        default_permissions = (
            'add_all',
            'change_all',
            'delete',
        )
