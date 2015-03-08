from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from cms.admin.placeholderadmin import FrontendEditableAdminMixin
from parler.admin import TranslatableAdmin

from aldryn_apphooks_config.admin import BaseAppHookConfig
from aldryn_people.models import Person
from aldryn_reversion.admin import VersionedPlaceholderAdminMixin

from . import models


def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)
make_published.short_description = _(
    "Mark selected articles as published")


def make_unpublished(modeladmin, request, queryset):
    queryset.update(is_published=False)
make_unpublished.short_description = _(
    "Mark selected articles as not published")


def make_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)
make_featured.short_description = _(
    "Mark selected articles as featured")


def make_not_featured(modeladmin, request, queryset):
    queryset.update(is_featured=False)
make_not_featured.short_description = _(
    "Mark selected articles as not featured")


class ArticleAdmin(VersionedPlaceholderAdminMixin,
                   TranslatableAdmin,
                   FrontendEditableAdminMixin,
                   admin.ModelAdmin):

    list_display = ('title', 'app_config', 'slug', 'is_featured',
                    'is_published')
    actions = (
        make_featured, make_not_featured,
        make_published, make_unpublished,
    )

    def add_view(self, request, *args, **kwargs):
        data = request.GET.copy()
        try:
            person = Person.objects.get(user=request.user)
            data['author'] = person.pk
            request.GET = data
        except Person.DoesNotExist:
            pass
        return super(ArticleAdmin, self).add_view(request, *args, **kwargs)

admin.site.register(models.Article, ArticleAdmin)


class NewsBlogConfigAdmin(TranslatableAdmin, BaseAppHookConfig):
    def get_config_fields(self):
        return ('app_title', 'config.random_field')

admin.site.register(models.NewsBlogConfig, NewsBlogConfigAdmin)
