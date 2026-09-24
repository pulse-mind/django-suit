import datetime

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from .models import Book, City, Continent, Country, Movie, Shelf


class AdminPagesTestCase(TestCase):
    """
    Smoke tests: every admin page renders (HTTP 200) with suit's templates, for the models of
    suit.tests.admin that exercise suit's public extension points. This is what would have
    caught the removal of the length_is filter (Django 5.1) before a release.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        cls.group = Group.objects.create(name='Editors')
        cls.europe = Continent.objects.create(name='Europe', order=1)
        cls.asia = Continent.objects.create(name='Asia', order=2)
        cls.france = Country.objects.create(
            name='France', code='FR', continent=cls.europe, independence_day=datetime.date(843, 8, 10),
            population=68000000, area=551695, description='Some text', order=1)
        cls.latvia = Country.objects.create(name='Latvia', code='LV', continent=cls.europe, order=2)
        cls.paris = City.objects.create(country=cls.france, name='Paris', is_capital=True)
        cls.shelf = Shelf.objects.create(name='Classics', country=cls.france, raw_country=cls.latvia)
        Book.objects.create(shelf=cls.shelf, title='Don Quixote', order=1)
        Movie.objects.create(shelf=cls.shelf, title='Tron', order=1)

    def setUp(self):
        self.client.force_login(self.user)

    def assertPage(self, url, *contains):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, url)
        for text in contains:
            self.assertContains(response, text, msg_prefix=url)
        return response

    def admin_urls(self, obj):
        info = obj._meta.app_label, obj._meta.model_name
        return {
            'changelist': reverse('admin:%s_%s_changelist' % info),
            'add': reverse('admin:%s_%s_add' % info),
            'change': reverse('admin:%s_%s_change' % info, args=[obj.pk]),
            'delete': reverse('admin:%s_%s_delete' % info, args=[obj.pk]),
            'history': reverse('admin:%s_%s_history' % info, args=[obj.pk]),
        }

    def test_every_model_page(self):
        for obj in (self.europe, self.france, self.paris, self.shelf, self.user, self.group):
            for name, url in self.admin_urls(obj).items():
                with self.subTest(model=obj._meta.label, page=name):
                    self.assertPage(url)

    def test_index_pages(self):
        self.assertPage(reverse('admin:index'), 'id="suit-nav"')
        self.assertPage(reverse('admin:app_list', args=['suit_tests']))
        self.assertPage(reverse('admin:app_list', args=['auth']))

    def test_logout_is_a_post_form(self):
        # GET logout is deprecated since Django 4.1 and removed in 5.0
        self.assertPage(reverse('admin:index'), '<form id="logout-form" method="post" action="%s">' % reverse('admin:logout'))
        response = self.client.post(reverse('admin:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get(reverse('admin:index')).status_code, 302)

    def test_login_page(self):
        self.client.logout()
        self.assertPage(reverse('admin:login'), 'id="login-form"')
        response = self.client.post(reverse('admin:login'), {'username': 'admin', 'password': 'wrong'})
        self.assertContains(response, 'errornote')

    def test_password_pages(self):
        self.assertPage(reverse('admin:password_change'))
        self.assertPage(reverse('admin:password_change_done'), 'logout-form')
        self.assertPage(reverse('admin:auth_user_password_change', args=[self.user.pk]))

    def test_change_form_tabs_includes_and_sizes(self):
        response = self.assertPage(self.admin_urls(self.france)['change'],
                                   'id="suit_form_tabs"', 'suit-tab-cities', 'suit-test-include',
                                   'widget-EnclosedInput', 'widget-AutosizedTextarea', 'input-group')
        # suit_form_size: fields -> INLINE for code, widgets -> XXX_LARGE for AutosizedTextarea
        self.assertContains(response, 'col-12 col-sm-9 col-md-10 form-inline')
        self.assertContains(response, 'col-12 col-sm-9 col-md-10 col-lg-9')
        self.assertNotContains(response, 'col-xs-')

    def test_fieldsets_headings_and_collapse(self):
        response = self.assertPage(self.admin_urls(self.france)['change'],
                                   'aria-labelledby="fieldset-0-1-heading"',
                                   '<h2 id="fieldset-0-1-heading" class="fieldset-heading">Statistics</h2>')
        # classes: ('collapse',) -> <details> (Django 5.1), no collapse.js
        self.assertContains(response, '<details><summary>')
        self.assertContains(response, 'class="fieldset-heading">Collapsed</h2>')

    def test_user_password_forms(self):
        # usable_password (Django 5.1): enable / disable password-based authentication
        response = self.assertPage(reverse('admin:auth_user_password_change', args=[self.user.pk]),
                                   'name="usable_password"', 'unusable_password_field.js',
                                   'name="unset-password"', 'field-password1')
        self.assertContains(response, 'class="default set-password"')
        self.assertPage(reverse('admin:auth_user_add'), 'name="usable_password"', 'unusable_password_field.js')

    def test_change_form_with_errors(self):
        response = self.client.post(self.admin_urls(self.france)['add'], {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'has-danger')

    def test_changelist_filters(self):
        url = self.admin_urls(self.france)['changelist']
        # suit_list_filter_horizontal filters in the toolbar; the other list_filter entries are
        # not displayed (no vertical filter panel), but still apply when present in the URL
        response = self.assertPage(url, 'search-filter')
        self.assertNotContains(response, 'id="changelist-filter"')
        response = self.assertPage(url + '?continent__id__exact=%d' % self.asia.pk)
        self.assertContains(response, '0 results')
        self.assertPage(url + '?code=FR', '1 result')
        self.assertPage(url + '?population__isnull=True')
        self.assertPage(url + '?q=fra', '1 result')
        self.assertPage(url + '?_to_field=id&_popup=1')

    def test_sortable_changelist_and_row_cell_attributes(self):
        response = self.assertPage(self.admin_urls(self.europe)['changelist'], 'suit-sortable',
                                   'table-success', 'suit-test-cell')
        self.assertContains(response, 'class="text-center')

    def test_sortable_inlines(self):
        self.assertPage(self.admin_urls(self.europe)['change'], 'suit-sortable')
        self.assertPage(self.admin_urls(self.shelf)['change'], 'suit-sortable-stacked', 'suit-sortable')

    def test_related_field_admin(self):
        self.assertPage(self.admin_urls(self.shelf)['changelist'], 'link-with-icon', 'Europe')

    def test_delete_selected_confirmation(self):
        response = self.client.post(self.admin_urls(self.france)['changelist'], {
            'action': 'delete_selected', '_selected_action': [self.france.pk, self.latvia.pk]})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'delete-confirmation')
