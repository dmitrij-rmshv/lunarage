from django import forms

from models import BirthDay


class BdInputForm(forms.ModelForm):
    birthday = forms.DateTimeField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = BirthDay
        fields = ('birthday')


# ---------NN----------------
# from django import forms

# class UserProfileForm(forms.Form):
#     birth_date = forms.DateField(
#         label='Дата рождения',
#         widget=forms.DateInput(attrs={'type': 'date'})
#     )

# from django import forms
# from .models import Profile

# class ProfileModelForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['birth_date']
#         widgets = {
#             'birth_date': forms.DateInput(attrs={'type': 'date'}),
#         }
