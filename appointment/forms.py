from django import forms
from .models import Printer

class PrinterForm(forms.ModelForm):
    class Meta:
        model = Printer
        fields = ['pname', 'pdescription']
        labels = {
            'pname': 'Printer Name',
            'pdescription': 'Description',
        }
