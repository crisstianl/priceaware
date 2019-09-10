from django import forms
from persistence.models import Store, Item

class SearchForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput, required=True, label="Search", max_length=128, min_length=3)

class StoreForm(forms.ModelForm):
    # define the helper class
    class Meta:
        model = Store
        fields = ["title", "address", "icon", "rating", "size"]

class ItemForm(forms.ModelForm):
    # define the helper class
    class Meta:
        model = Item
        fields = ["id", "name", "link", "price", ]
        #exclude = ('store', )

    # Foreign key
    store_id = forms.IntegerField(widget=forms.NumberInput, required=True, min_value=1, max_value=9999)

    # custom post validation for "store_id" field, e.g. def clean_<fieldName>()
    def clean_store_id(self, *args, **kwargs):
        return self.cleaned_data.get("store_id")