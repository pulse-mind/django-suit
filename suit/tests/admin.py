from django.contrib import admin
from django.forms import ModelForm

from suit import apps
from suit.admin import RelatedFieldAdmin, get_related_field
from suit.admin_filters import IsNullFieldListFilter
from suit.sortables import SortableModelAdmin, SortableStackedInline, SortableTabularInline
from suit.widgets import AutosizedTextarea, EnclosedInput

from .models import Book, City, Continent, Country, Movie, Shelf


class CityInline(admin.TabularInline):
    model = City
    extra = 1
    suit_classes = 'suit-tab suit-tab-cities'


class CountryForm(ModelForm):
    class Meta:
        widgets = {
            'area': EnclosedInput(prepend='fa-globe', append='km<sup>2</sup>'),
            'population': EnclosedInput(prepend='fa-users', append='Search', append_class='btn'),
            'description': AutosizedTextarea,
        }


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    form = CountryForm
    search_fields = ('name', 'code')
    list_display = ('name', 'code', 'continent', 'independence_day')
    list_filter = ('continent', 'independence_day', 'code', ('population', IsNullFieldListFilter))
    suit_list_filter_horizontal = ('code', 'population')
    inlines = (CityInline,)
    fieldsets = [
        (None, {'classes': ('suit-tab suit-tab-general',),
                'fields': ['name', 'code', 'continent', 'independence_day']}),
        ('Statistics', {'classes': ('suit-tab suit-tab-general',),
                        'description': 'EnclosedInput widgets',
                        'fields': [('area', 'population')]}),
        ('Collapsed', {'classes': ('suit-tab suit-tab-general', 'collapse'),
                       'fields': ['description']}),
    ]
    suit_form_size = {
        'fields': {'code': apps.SUIT_FORM_SIZE_INLINE},
        'widgets': {'AutosizedTextarea': apps.SUIT_FORM_SIZE_XXX_LARGE},
    }
    suit_form_tabs = (('general', 'General'), ('cities', 'Cities'), ('info', 'Info'))
    suit_form_includes = (
        ('suit_tests/include.html', 'top', 'general'),
        ('suit_tests/include.html', '', 'info'),
    )


class CountryInline(SortableTabularInline):
    model = Country
    fields = ('name', 'code')
    extra = 1
    show_change_link = True


@admin.register(Continent)
class ContinentAdmin(SortableModelAdmin):
    list_display = ('name', 'countries')
    inlines = (CountryInline,)

    def suit_row_attributes(self, obj, request):
        return {'class': 'table-success'} if obj.name == 'Europe' else None

    def suit_column_attributes(self, column):
        if column == 'countries':
            return {'class': 'text-center'}

    def suit_cell_attributes(self, obj, column):
        if column == 'countries':
            return {'class': 'text-center suit-test-cell'}

    def countries(self, obj):
        return obj.country_set.count()


class BookInline(SortableTabularInline):
    model = Book
    extra = 1
    suit_form_inlines_hide_original = True


class MovieInline(SortableStackedInline):
    model = Movie
    extra = 1
    suit_form_size = {'default': apps.SUIT_FORM_SIZE_X_LARGE}


@admin.register(Shelf)
class ShelfAdmin(RelatedFieldAdmin):
    list_display = ('name', 'link_to_country', 'country__continent')
    raw_id_fields = ('raw_country',)
    inlines = (BookInline, MovieInline)
    link_to_country = get_related_field('link_to_country')


admin.site.register(City)
