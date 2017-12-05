# -*- coding: utf-8 -*-

"""
Most of this code extracted and borrowed from django-model-utils

Copyright (c) 2009-2015, Carl Meyer and contributors
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.
    * Neither the name of the author nor the names of other
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from __future__ import unicode_literals

from importlib import import_module

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.apps import apps
from django.utils.timezone import now
from organizations.settings import organizations_settings


class AutoCreatedField(models.DateTimeField):
    """
    A DateTimeField that automatically populates itself at
    object creation.

    By default, sets editable=False, default=datetime.now.

    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', now)
        super(AutoCreatedField, self).__init__(*args, **kwargs)


class AutoLastModifiedField(AutoCreatedField):
    """
    A DateTimeField that updates itself on each save() of the model.

    By default, sets editable=False and default=datetime.now.

    """
    def pre_save(self, model_instance, add):
        value = now()
        setattr(model_instance, self.attname, value)
        return value


try:
    parts = organizations_settings.ORGANIZATION_SLUGFIELD.split(".")
    module_path, class_name = ".".join(parts[:-1]), parts[-1]
    module = import_module(module_path)
    BaseSlugField = getattr(module, class_name)
except (ImportError, ValueError):
    raise ImproperlyConfigured("Your SlugField class, '{0}', is improperly defined. "
                   "See the documentation and install an auto slug field".format(organizations_settings.ORGANIZATION_SLUGFIELD))

class SlugField(BaseSlugField):
    """Class redefinition for migrations"""

def get_slug_field():
    return apps.get_model(organizations_settings.ORGANIZATION_SLUGFIELD)
