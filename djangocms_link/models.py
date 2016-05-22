# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.models import CMSPlugin, Page
from cms.utils.compat.dj import python_2_unicode_compatible
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.fields import PageField

from .validators import IntranetURLValidator
from django.core.exceptions import ValidationError


@python_2_unicode_compatible
class AbstractLink(CMSPlugin):
    """
    A link to an other page or to an external website
    """

    TARGET_CHOICES = (
        ('', _('same window')),
        ('_blank', _('new window')),
        ('_parent', _('parent window')),
        ('_top', _('topmost frame')),
    )

    # Used by django-cms search
    search_fields = ('name', )

    url_validators = [IntranetURLValidator(intranet_host_re=getattr(
        settings, 'DJANGOCMS_LINK_INTRANET_HOSTNAME_PATTERN', None)), ]

    # Add an app namespace to related_name to avoid field name clashes
    # with any other plugins that have a field with the same name as the
    # lowercase of the class name of this model.
    # https://github.com/divio/django-cms/issues/5030
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin, related_name='%(app_label)s_%(class)s', parent_link=True)

    name = models.CharField(_('name'), max_length=256)
    # Re: max_length, see: http://stackoverflow.com/questions/417142/
    url = models.CharField(_('link'), blank=True, null=True,
                           validators=url_validators, max_length=2048)

    page = PageField(null=True, blank=True)
    url = models.URLField(max_length=255, null=True, blank=True,
                          help_text=_('If page is not set, you can enter a link here.'))

    anchor = models.CharField(_('anchor'), max_length=128, blank=True,
                              help_text=_('This applies only to page and text links.'
                                          ' Do <em>not</em> include a preceding "#" symbol.'))
    # Explicitly set a max_length so that we don't end up with different
    # schemata on Django 1.7 vs. 1.8.
    mailto = models.EmailField(_('email address'), max_length=254, blank=True, null=True,
                               help_text=_('An email address has priority over a text link.'))
    phone = models.CharField(_('Phone'), blank=True, null=True, max_length=40,
                             help_text=_('A phone number has priority over a mailto link.'))
    target = models.CharField(_('target'), blank=True, max_length=100,
                              choices=TARGET_CHOICES)

    def clean(self):
        """
        Require at least one link field to be set
        """
        if not (self.url or self.page or self.anchor or self.mailto or self.phone):
            raise ValidationError("One of these link fields is required.")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def link(self):
        if self.phone:
            link = 'tel:%s' % self.phone
        elif self.mailto:
            link = 'mailto:%s' % self.mailto
        elif self.page:
            return self.page.get_absolute_url()
        elif self.url:
            return self.url
        else:
            link = ''
        if (self.url or self.page or not link) and self.anchor:
            link += '#%s' % self.anchor
        return link


class Link(AbstractLink):

    class Meta:
        abstract = False
