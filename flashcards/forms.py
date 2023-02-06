from django import forms
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# modify django's create user form
class NewUserForm(UserCreationForm):
    # inherit attributes of template form

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        password = cleaned_data.get('password1')

        # check for min length
        min_length = 8
        if len(password) < min_length:
            msg = 'Password must be at least %s characters long.' % (str(min_length))
            self.add_error('password1', msg)

        # check for letter
        if sum(c.isalpha() for c in password) < 1:
            msg = 'Password must contain at least 1 letter.'
            self.add_error('password1', msg)

        # check for digit
        if sum(c.isdigit() for c in password) < 1:
            msg = 'Password must contain at least 1 number.'
            self.add_error('password1', msg)

        # check for special character
        if sum(not c.isalnum() for c in password) < 1: # not a number or letter
            msg = 'Password must contain at least 1 special character.'
            self.add_error('password1', msg)
            
        


