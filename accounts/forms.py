
from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
    }))

    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_no','email','password']

    # apply css to each field like 'first_name','last_name','phone_no','email','password'
    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)

        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['phone_no'].widget.attrs['placeholder'] = '(+91)'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        clean_data = super(RegistrationForm,self).clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Password and confirm password does not match'
            )