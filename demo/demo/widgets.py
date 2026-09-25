from django import forms

SELECT2_BOOTSTRAP_THEME = '//cdnjs.cloudflare.com/ajax/libs/select2-bootstrap-theme/0.1.0-beta.6/select2-bootstrap.min.css'


class Bootstrap4Select(object):
    """
    Mixin for django-select2 widgets: Bootstrap theme on top of django-select2's own media
    (select2 assets, i18n file, django_select2.js / .css).
    """
    def build_attrs(self, base_attrs, attrs=None, **kwargs):
        attrs = super(Bootstrap4Select, self).build_attrs(base_attrs, attrs, **kwargs)
        attrs.setdefault('data-theme', 'bootstrap')
        # Full column width like the other selects (django_select2.css sets 20em)
        attrs.setdefault('data-width', '100%')
        return attrs

    @property
    def media(self):
        return super().media + forms.Media(css={'screen': [SELECT2_BOOTSTRAP_THEME]})
