from django import forms
from . import models


class SearchForm(forms.Form):
    search = forms.CharField(required=False)


class FilterForm(forms.Form):
    region = forms.ChoiceField(required=False, choices=models.Region.get_choices_filter(), initial='----')
    condition = forms.ChoiceField(required=False, choices=models.Condition.get_choices_filter())
    division = forms.ChoiceField(required=False, choices=models.Division.get_choices_filter())


class BoardUpdateForm(forms.ModelForm):
    photo = forms.ImageField(required=True)
    clear_photo = forms.BooleanField(required=False)

    class Meta:
        model = models.Board
        fields = [
            'name',
            'description',
            'price',
            'count',
            'region',
            'division',
            'condition',
            'status',
            'photo',
        ]







