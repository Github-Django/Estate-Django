from django import forms
from .models import MyUser
from blog.models import Article

class ListingForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = (
            "title",
            "description",
            "thumbnail",
            "unit_price",
            "area",
            "year_built",
            "region",
            "property_contract",
            "property_type",
            "bedrooms",
            'conditions_contract',
            'foundation',
            'document_contract',
            'address',
            'Deposit1',
            'Deposit2',
            'direction_contract',
            'cooling_contract',
            'heating_contract',
            'water_contract',
            'covering_contract',
            'construction_contract',
            'advertiser',
            'mobile',
            'full_name',
            'photo_1',
            'photo_2',
            'photo_3',
            'photo_4',
        )


class RegisterForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['mobile','first_name' ]
