import phonenumbers
from django import forms
from django.contrib.auth import models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from validate_email import validate_email
from phonenumber_field.formfields import PhoneNumberField
#create your forms here
# we are using the django provided form, editing it to our taste

class NewUserForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'placeholder':'Email Address', 'class':'form-group'}))
    confirm_email = forms.EmailField()
    mobile_number = PhoneNumberField()
    #mobile_number = forms.IntegerField()

    class Meta:
        model = User
        fields = ("username", "email", "confirm_email", "mobile_number", "password1", "password2")


    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.confirm_email = self.cleaned_data["confirm_email"]
        user.mobile_number = self.cleaned_data["mobile_number"]
        if commit:
            user.save()
        return user


