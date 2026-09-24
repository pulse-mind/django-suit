from django.db import models


class Continent(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2, help_text='ISO 3166-1 alpha-2 code')
    continent = models.ForeignKey(Continent, null=True, blank=True, on_delete=models.SET_NULL)
    independence_day = models.DateField(null=True, blank=True)
    population = models.PositiveIntegerField(null=True, blank=True)
    area = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'countries'

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_capital = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.name


class Shelf(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    raw_country = models.ForeignKey(Country, null=True, blank=True, related_name='+', on_delete=models.SET_NULL)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Movie(models.Model):
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
