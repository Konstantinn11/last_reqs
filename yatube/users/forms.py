from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms.models import ModelForm
from django.forms import Textarea, Select, DateInput
from .models import User_info, Vacation, Message, Position
from django import forms
User = get_user_model()


class DateInput(DateInput):
    input_type = 'date'

class CreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        # Инициализируем форму
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    class Meta(UserCreationForm.Meta):
        # укажем модель, с которой связана создаваемая форма
        model = User
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ('first_name', 'last_name', 'username', 'email')

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


class VacationForm(forms.ModelForm):
    class Meta:
        model = Vacation
        exclude = ['user', 'year', 'can_redact']
        widgets = {
            'id': forms.Textarea(attrs={"cols": 40, "rows": 1}),
            'day_start': forms.DateInput(attrs={'id': 'id_day_start', 'placeholder': 'Выберите дату'}),
            'day_end': forms.DateInput(attrs={'id': 'id_day_end', 'placeholder': 'Выберите дату'}),
            'how_long': forms.NumberInput(attrs={
                'id': 'id_how_long',
                'placeholder': 'календарных дней',
                'min': '1', 
                'step': '1',
                'class': 'form-control'
            }),
        }
        labels = {
            'day_start': 'Начало отпуска',
            'day_end': 'Окончание отпуска',
            'how_long': 'Кол-во дней',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем одинаковые классы и атрибуты в поля формы
        date_field_style = {'class': 'form-control'}
        self.fields['day_start'].widget.attrs.update(date_field_style)
        self.fields['how_long'].widget.attrs.update(date_field_style)
        self.fields['day_end'].widget.attrs.update(date_field_style)

        # Перестановка полей
        self.order_fields(['day_start', 'how_long', 'day_end'])


class MessageForm(ModelForm):
    class Meta():
        model = Message
        exclude = ['user_one', 'user_two', 'witch_write', 'pub_date', 'readed']
        widgets = {
            'text': Textarea(attrs={"cols": 40, "rows": 1,}),
        }
