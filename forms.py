from django import forms
from .models import Comment
# Подключаем компонент UserCreationForm
from django.contrib.auth.forms import UserCreationForm
# Подключаем модель User
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User
from django.forms import widgets

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('com_text',)
        widgets = {
          'com_text': Textarea(attrs={'rows':10, 'cols':300}),}
        
      
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
         self.fields[field].widget.attrs['size']='1'

# Создаём класс формы
class RegistrForm(UserCreationForm):
  # Добавляем новое поле Email
  email = forms.EmailField(max_length=254, help_text='This field is required')
  
  # Создаём класс Meta
  class Meta:
    # Свойство модели User
    model = User
    # Свойство назначения полей
    fields = ('username', 'email', 'password1', 'password2', )

from django import forms

class ContactForm(forms.Form):
	subject = forms.CharField(max_length = 100)
	sender = forms.EmailField()
	message = forms.CharField(widget = forms.Textarea(attrs = {'class': 'form-control'}))
	copy = forms.BooleanField(required = False)