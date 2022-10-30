
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Menu

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({
            'class':"form-control", 'type':"email", 'name':"email", 'placeholder':"Email"
        })
        self.fields["username"].widget.attrs.update({
            'class':"form-control", 'type':"text", 'name':"username", 'placeholder':"Username"
        })
        self.fields["first_name"].widget.attrs.update({
            'class':"form-control", 'type':"text", 'name':"fname", 'placeholder':"First Name"
        })
        self.fields["last_name"].widget.attrs.update({
            'class':"form-control", 'type':"text", 'name':"lname", 'placeholder':"Last Name"
        })
        self.fields["password1"].widget.attrs.update({
            'class':"form-control", 'type':"password", 'name':"password1", 'placeholder':"Password"
        })
        self.fields["password2"].widget.attrs.update({
            'class':"form-control", 'type':"password", 'name':"password2", 'placeholder':"Confirm Password"
        })

    email=forms.EmailField()
    username=forms.IntegerField()


    class Meta:
        model=User
        fields=["email", "username", "first_name", "last_name", "password1", "password2"]



class MenuForm(forms.ModelForm):

    # def __init__(self):
        
        # super.__init__(*args, **kwargs)

        # self.fields['name'].widget.attrs({
        #     'type':"text", 'class':"form-control", 'id':"name", 'name':"name", 'placeholder':"Name", 'tabindex':"1",
        # })
        # self.fields['price'].widget.attrs({
        #     'type':"text", 'class':"form-control", 'id':"email", 'name':"email", 'placeholder':"Price", 'tabindex':"2",
        # })
        # self.fields['prep_time'].widget.attrs({
        #     'type':"text", 'class':"form-control", 'id':"subject", 'name':"subject", 'placeholder':"Prep Time", 'tabindex':"3",
        # })
        # self.fields['cuisine'].widget.attrs({
        #     'name':"message", 'class':"form-control", 'id':"message", 'placeholder':"Cuisine", 'tabindex':"4"
        # })


    class Meta:
        model=Menu
        fields="__all__"