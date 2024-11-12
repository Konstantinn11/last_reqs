from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms.models import ModelForm
from django.forms import Textarea, Select, DateInput
from django import forms
from .models import User_info, Vacation, Message, Position
from posts.models import Unit
User = get_user_model()


class DateInput(DateInput):
    input_type = 'date'

class CreationForm(UserCreationForm):
    # Добавляем поля для должности и номера отдела
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=True,  # Сделаем обязательным для выбора
        label='Должность'
    )
    otd_number = forms.ModelChoiceField(
        queryset=Unit.objects.all(),
        required=True,  # Сделаем обязательным для выбора
        label='Номер отдела'
    )

    def __init__(self, *args, **kwargs):
        # Инициализируем форму
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = User
        # Указываем, какие поля должны быть видны в форме
        fields = ('first_name', 'last_name', 'position', 'otd_number', 'username', 'email')

    def save(self, commit=True):
        # Сохраняем пользователя
        user = super().save(commit=False)
        if commit:
            user.save()

        # Создаем объект User_info и сохраняем его
        user_info = User_info(
            user=user,  # Связываем User с User_info
            position=self.cleaned_data.get('position'),
            otd_number=self.cleaned_data.get('otd_number')
        )
        if commit:
            user_info.save()  # Сохраняем User_info в базе данных

        return user

class User_infoForm(ModelForm):

    class Meta():
        model = User_info
        fields = (
            'otd_number', 'phone_number', 'reqs_access', 'stor_access', 'corr_access',
            'conf_access', 'user_access', 'vacs_access',
        )

        # exclude = ['user','position', 'boss']
        widgets = {
            'phone_number': Textarea(attrs={"readonly": False, "cols": 40, "rows": 1,}),
        }


class VacationForm(ModelForm):

    class Meta():
        model = Vacation
        exclude = ['user', 'year']
        widgets = {
            'id': Textarea(attrs={"cols": 40, "rows": 1,}),
            'how_long': Textarea(attrs={"cols": 40, "rows": 1,}),
            'day_start': DateInput(),
            'day_end': DateInput(),
            'can_redact': Textarea(attrs={"readonly": True, "cols": 40, "rows": 1,}),
        }


class MessageForm(ModelForm):
    class Meta():
        model = Message
        exclude = ['user_one', 'user_two', 'witch_write', 'pub_date', 'readed']
        widgets = {
            'text': Textarea(attrs={"cols": 40, "rows": 1,}),
        }
