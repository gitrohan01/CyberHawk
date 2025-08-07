from django import forms

class ScanForm(forms.Form):
    target = forms.CharField(
        label='Target (URL or IP)',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a URL or IP (e.g. https://example.com or 192.168.1.1)',
            'autocomplete': 'off'
        })
    )
