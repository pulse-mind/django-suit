from django.apps import AppConfig


class SuitTestsConfig(AppConfig):
    """Models and admins exercising suit's public extension points, for the test suite only"""
    name = 'suit.tests'
    label = 'suit_tests'
    default_auto_field = 'django.db.models.AutoField'
