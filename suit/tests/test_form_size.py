from django.test import SimpleTestCase

from suit import apps

FORM_SIZES = ('INLINE', 'X_TINY', 'TINY', 'SMALL', 'HALF', 'LARGE', 'X_LARGE', 'XX_LARGE',
              'XXX_LARGE', 'FULL')


class FormSizeConstantsTestCase(SimpleTestCase):
    """SUIT_FORM_SIZE_* are public API, used in suit_form_size and DjangoSuitConfig.form_size"""

    def test_shape(self):
        for name in FORM_SIZES:
            size = getattr(apps, 'SUIT_FORM_SIZE_%s' % name)
            self.assertIsInstance(size, tuple, name)
            self.assertEqual(len(size), 2, name)
            self.assertEqual(size[0], apps.SUIT_FORM_SIZE_LABEL, name)
            self.assertIsInstance(size[1], str, name)

    def test_bootstrap5_grid_vocabulary(self):
        for name in ('LABEL',) + FORM_SIZES:
            value = getattr(apps, 'SUIT_FORM_SIZE_%s' % name)
            classes = ' '.join(value) if isinstance(value, tuple) else value
            # col-xs-* is Bootstrap 3: no rule under Bootstrap 5, the xs size is col-*
            self.assertNotIn('col-xs-', classes, name)
            self.assertIn('col-12', classes.split(), name)

    def test_default_form_size(self):
        form_size = apps.DjangoSuitConfig.form_size
        self.assertEqual(form_size['default'], apps.SUIT_FORM_SIZE_X_LARGE)
        self.assertEqual(form_size['widgets']['RelatedFieldWidgetWrapper'], apps.SUIT_FORM_SIZE_XXX_LARGE)
