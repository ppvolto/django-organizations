from django.db import models


from organizations.base import (
    OrganizationBase,
    OrganizationUserBase,
    OrganizationOwnerBase,
)

class SampleOrganization(OrganizationBase):
    custom_field = models.CharField(max_length=255)


class SampleOrganizationUser(OrganizationUserBase):
    custom_field = models.CharField(max_length=255)


class SampleOrganizationOwner(OrganizationOwnerBase):
    custom_field = models.CharField(max_length=255)


class Team(SampleOrganization):
    sport = models.CharField(max_length=100, blank=True, null=True)
