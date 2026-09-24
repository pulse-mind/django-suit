from django.contrib.admin import FieldListFilter
from django.contrib.admin.utils import get_last_value_from_parameters
from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _


class IsNullFieldListFilter(FieldListFilter):
    """
    Filter on whether a nullable field is set: All / Is present / Is Null.
    Override notnull_label / isnull_label to rename the choices.
    Supports facets (ModelAdmin.show_facets, Django 5.0), like Django's EmptyFieldListFilter.
    """
    notnull_label = _('Is present')
    isnull_label = _('Is Null')

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = '%s__isnull' % field_path
        self.lookup_val = get_last_value_from_parameters(params, self.lookup_kwarg)
        super().__init__(field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        return [self.lookup_kwarg]

    def get_facet_counts(self, pk_attname, filtered_qs):
        isnull = Q(**{self.lookup_kwarg: True})
        return {
            'isnull__c': Count(pk_attname, filter=isnull),
            'notnull__c': Count(pk_attname, filter=~isnull),
        }

    def choices(self, changelist):
        add_facets = changelist.add_facets
        facet_counts = self.get_facet_queryset(changelist) if add_facets else None
        for lookup, title, count_field in (
                (None, _('All'), None),
                ('False', self.notnull_label, 'notnull__c'),
                ('True', self.isnull_label, 'isnull__c'),
        ):
            if add_facets and count_field is not None:
                title = '%s (%s)' % (title, facet_counts[count_field])
            yield {
                'selected': self.lookup_val == lookup,
                'query_string': changelist.get_query_string({self.lookup_kwarg: lookup}),
                'display': title,
            }
