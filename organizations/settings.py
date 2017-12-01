# -*- coding: utf-8 -*-

# Copyright (c) 2012-2015, Ben Lopatin and contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.  Redistributions in binary
# form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with
# the distribution
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from django.conf import settings

import importlib

from organizations.utils import model_field_attr

USER_SETTINGS = getattr(settings, "DJANGO_ORGANIZATION", None)

ORGANIZATION_MODEL = getattr(settings, "DJANGO_ORGANIZATION_ORGANIZATION_MODEL", "organizations.Organization")
ORGANIZATION_USER_MODEL = getattr(settings, "DJANGO_ORGANIZATION_ORGANIZATION_USER_MODEL", "organizations.OrganizationUser")
ORGANIZATION_OWNER_MODEL = getattr(settings, "DJANGO_ORGANIZATION_ORGANIZATION_OWNER_MODEL", "organizations.OrganizationOwner")
ORGANIZATION_SLUGFIELD = getattr(settings, "DJANGO_ORGANIZATION_ORGANIZATION_SLUGFIELD", "django_extensions.db.fields.AutoSlugField")

DEFAULTS = {
    "ORGANIZATION_MODEL": ORGANIZATION_MODEL,
    "ORGANIZATION_USER_MODEL": ORGANIZATION_USER_MODEL,
    "ORGANIZATION_OWNER_MODEL": ORGANIZATION_OWNER_MODEL,
    "ORGANIZATION_SLUGFIELD": ORGANIZATION_SLUGFIELD,
    "INVITATION_BACKEND": 'organizations.backends.defaults.InvitationBackend',
    "REGISTRATION_BACKEND": 'organizations.backends.defaults.RegistrationBackend',
}

MANDATORY = (
    "ORGANIZATION_MODEL",
    "ORGANIZATION_USER_MODEL",
    "ORGANIZATION_OWNER_MODEL",
    "ORGANIZATION_SLUGFIELD",
    "INVITATION_BACKEND",
    "REGISTRATION_BACKEND",
)

IMPORT_STRINGS = (
    "INVITATION_BACKEND",
    "REGISTRATION_BACKEND",
)


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    elif "." in val:
        return import_from_string(val, setting_name)
    else:
        raise ImproperlyConfigured("Bad value for %r: %r" % (setting_name, val))


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        parts = val.split(".")
        module_path, class_name = ".".join(parts[:-1]), parts[-1]
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except ImportError as e:
        msg = "Could not import %r for setting %r. %s: %s." % (val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


class DjangoOrganizationsSettings(object):
    """
    A settings object, that allows OAuth2 Provider settings to be accessed as properties.
    Any setting with string import paths will be automatically resolved
    and return the class, rather than the string literal.
    """

    def __init__(self, user_settings=None, defaults=None, import_strings=None, mandatory=None):
        self.user_settings = user_settings or {}
        self.defaults = defaults or {}
        self.import_strings = import_strings or ()
        self.mandatory = mandatory or ()

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise AttributeError("Invalid DjangoOrganizationsSettings setting: %r" % (attr))

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if val and attr in self.import_strings:
            val = perform_import(val, attr)

        self.validate_setting(attr, val)

        # Cache the result
        setattr(self, attr, val)
        return val

    def validate_setting(self, attr, val):
        if not val and attr in self.mandatory:
            raise AttributeError("DjangoOrganizationsSettings setting: %r is mandatory" % (attr))


organizations_settings = DjangoOrganizationsSettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS, MANDATORY)