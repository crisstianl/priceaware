from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.serializers.json import DjangoJSONEncoder
from json import dumps

class Store(models.Model):
    id = models.AutoField(primary_key=True) # IntegerField that automatically increments
    title = models.CharField(max_length=128, blank=False, unique=True) # small strings
    address = models.URLField(max_length=256, blank=False, unique=True) # CharField validated by URLValidator
    icon = models.URLField(max_length=256, blank=True) # CharField validated by URLValidator
    rating = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    size = models.PositiveSmallIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(20)])

    def __str__(self):
        self.__dict__.pop("_state", None)
        return dumps(self.__dict__)

class Item(models.Model):
    id = models.AutoField(primary_key=True) # IntegerField that automatically increments
    name = models.CharField(max_length=128, blank=False) # small strings
    link = models.URLField(max_length=256, blank=False) # CharField validated by URLValidator
    # price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, default=0) # numbers up to 99 999.99
    price = models.CharField(max_length=32, blank=False) # small strings
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # relations
    store = models.ForeignKey(Store, on_delete=None, related_name="store_id")

    def __str__(self):
        self.__dict__.pop("_state", None)
        return dumps(self.__dict__, cls=DjangoJSONEncoder)
