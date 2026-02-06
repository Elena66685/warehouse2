from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Иванов Иван'
            })
        }
        labels = {
            'name': 'Имя сотрудника'
        }
        help_texts = {
            'name': 'Введите полное имя сотрудника'
        }