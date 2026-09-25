from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem


class SuitConfig(DjangoSuitConfig):
    menu = (
        ParentItem('Content', children=[
            ChildItem(model='demo.country', params={'o': '1.2'}),
            ChildItem(model='demo.continent'),
            ChildItem(model='demo.showcase'),
            ChildItem('Custom view', url='/admin/custom/'),
        ], icon='fa fa-leaf'),
        ParentItem('Integrations', children=[
            ChildItem(model='demo.city'),
        ]),
        ParentItem('Users', children=[
            ChildItem(model='auth.user'),
            ChildItem('User groups', 'auth.group'),
        ], icon='fa fa-users'),
        ParentItem('Right Side Menu', children=[
            ChildItem('Password change', url='admin:password_change'),
            ChildItem('Open Google', url='http://google.com', target_blank=True),

        ], align_right=True, icon='fa fa-cog'),
    )

    def ready(self):
        super(SuitConfig, self).ready()

        # DO NOT COPY FOLLOWING LINE
        # It is only to prevent updating last_login in DB for demo app
        self.prevent_user_last_login()

    def prevent_user_last_login(self):
        """
        Keep logins from writing to the committed demo database (last_login).
        django.contrib.auth connects update_last_login in its own ready(), which runs after this one
        (INSTALLED_APPS order): disconnect it on the first request instead.
        """
        from django.contrib.auth import user_logged_in
        from django.core.signals import request_started

        def disconnect_update_last_login(**kwargs):
            user_logged_in.disconnect(dispatch_uid='update_last_login')
            request_started.disconnect(disconnect_update_last_login)

        request_started.connect(disconnect_update_last_login, weak=False)
