# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from djangocms_link.models import Link


class LinkPlugin(CMSPluginBase):

    model = Link
    name = _('Link')
    render_template = 'cms/plugins/link.html'
    text_enabled = True
    allow_children = True

    def render(self, context, instance, placeholder):
        link = instance.link()
        context.update({
            'name': instance.name,
            'link': link,
            'target': instance.target,
            'placeholder': placeholder,
            'object': instance
        })
        return context

    def icon_src(self, instance):
        return '{0}cms/img/icons/plugins/link.png'.format(settings.STATIC_URL)

plugin_pool.register_plugin(LinkPlugin)


class ButtonPlugin(CMSPluginBase):

    model = Link
    name = _('Button')
    render_template = 'cms/plugins/button.html'
    text_enabled = True
    allow_children = False

    def render(self, context, instance, placeholder):
        link = instance.link()
        context.update({
            'name': instance.name,
            'link': link,
            'target': instance.target,
            'placeholder': placeholder,
            'object': instance
        })
        return context

    def icon_src(self, instance):
        return '{0}cms/img/icons/plugins/link.png'.format(settings.STATIC_URL)

plugin_pool.register_plugin(ButtonPlugin)
