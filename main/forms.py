from datetime import datetime, timedelta
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from captcha.fields import CaptchaField

# from .models import BirthDay


# class BdInputForm(forms.ModelForm):
#     birthday = forms.DateTimeField(
#         label='Дата рождения',
#         widget=forms.DateInput(attrs={'type': 'datetime'})
#     )

#     class Meta:
#         model = BirthDay
#         fields = ('birthday',)


def validate_date_range(value):
    # Пример: дата не должна быть в будущем и не раньше, чем 2 года назад
    if value > timezone.now():
        raise ValidationError("Дата не может быть в будущем!")
    if value < timezone.make_aware(datetime.now() - timedelta(days=365*96)):
        raise ValidationError("Дата не может быть старше 96 лет!")


class BdInputForm(forms.Form):
    birthday = forms.DateTimeField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    # for_someone_else = forms.BooleanField(
    #     label='не для себя',
    #     widget=forms.CheckboxInput()
    # )
    captcha = CaptchaField(
        label='Введите текст с картинки',
        error_messages={'invalid': 'Неправильный текст'}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Применяем валидатор к полю
        self.fields['birthday'].validators.append(validate_date_range)


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
