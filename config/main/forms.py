import re

from captcha.fields import CaptchaField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.core.exceptions import ValidationError

from .models import News


class ContactForm(forms.Form):
    """Контактная форма"""
    name = forms.CharField(label='Ваше имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'class': 'form-control', "rows": 2}))
    captcha = CaptchaField()


class AddNewsForm(forms.ModelForm):
    """Форма добавления статей через сайт"""
    content = forms.CharField(widget=CKEditorUploadingWidget())
    captcha = CaptchaField()

    class Meta:
        model = News
        exclude = ["author"]
        fields = ['title', 'content', 'category', 'photo', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 20}),
            'category': forms.Select(attrs={'class': 'form-control'}),

        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title



