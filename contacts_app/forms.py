from django import forms
from .models import Contact

class UploadCSVForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(
        attrs={
            'class': 'bg-teal-700 text-white border border-teal-500 px-3 py-2 rounded',
            'accept': '.csv'
        }
    ))


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'state', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'bg-teal-700 text-white border border-teal-500 px-3 py-2 rounded',
                'placeholder': 'Customer Full Name'
            }),
            'state': forms.TextInput(attrs={
                'class': 'bg-teal-700 text-white border border-teal-500 px-3 py-2 rounded',
                'placeholder': 'State'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'bg-teal-700 text-white border border-teal-500 px-3 py-2 rounded',
                'placeholder': 'Phone Number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'bg-teal-700 text-white border border-teal-500 px-3 py-2 rounded',
                'placeholder': 'Customer Address',
                'rows': 3,
            }),
        }

    # Auto-uppercase the name before saving
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            return name.upper()
        return name
