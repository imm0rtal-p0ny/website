from django import forms
from . import models
from PIL import Image, ImageOps


def create_mini_size_photo():
    pass



class SearchForm(forms.Form):
    search = forms.CharField(required=False)


class FilterForm(forms.Form):
    region = forms.ChoiceField(required=False, choices=models.Region.get_choices_filter(), initial='----')
    condition = forms.ChoiceField(required=False, choices=models.Condition.get_choices_filter())
    division = forms.ChoiceField(required=False, choices=models.Division.get_choices_filter())


class BoardUpdateForm(forms.ModelForm):
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

    def clean(self):
        cleaned_data = super().clean()
        clear_photo = cleaned_data.get('clear_photo')
        photo = cleaned_data.get('photo')
        old_photo = self.initial.get('photo')
        if old_photo != photo and old_photo != models.DEFAULT_BOARD_PHOTO:
            old_photo.delete()

        if clear_photo:
            if photo != models.DEFAULT_BOARD_PHOTO:
                photo.delete()
                cleaned_data['photo'] = models.DEFAULT_BOARD_PHOTO

        return cleaned_data






