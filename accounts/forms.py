from django import forms
from django.contrib.auth.models import User
from .models import EmployeeProfile
from django.core.exceptions import ValidationError


class EmployeeForm(forms.ModelForm):
    username      = forms.CharField(required=True,max_length=150, widget = forms.TextInput(attrs={ 'class': 'form-control'}), help_text="Allowed only Letters, digits and @/./+/-/_ only")
    first_name     = forms.CharField(required=True,max_length=100, widget = forms.TextInput(attrs={ 'class': 'form-control'}))
    last_name     = forms.CharField(required=True,max_length=100, widget = forms.TextInput(attrs={ 'class': 'form-control'}))

    password1 = forms.CharField(required=True,max_length=100,widget=forms.PasswordInput(attrs={
        
        'class': 'form-control'
    }))

    password2 = forms.CharField(required=True,max_length=100,widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    email = forms.EmailField(required=True,max_length=100,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'email',
    }))
    
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')


    def clean(self):
        cleaned_data = super(EmployeeForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError(
                "Password Doesn't Match!"
            )

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 6:
            raise ValidationError('Password too short')

        return password


class UpdateEmployeeForm(EmployeeForm):
    def __init__(self, *args, **kwargs):
        super(UpdateEmployeeForm, self).__init__(*args, **kwargs)
        self.fields.pop('password1')
        self.fields.pop('password2')


class EmployeeProfileForm(forms.ModelForm):
    address         = forms.CharField(required=False,max_length=200, 
    widget = forms.Textarea(attrs={ 
                                'class': 'form-control',
                                'rows':'3',
                            }))
    phone_number    = forms.IntegerField(required=False,max_length=20, widget = forms.NumberInput(attrs={ 'class': 'form-control'}))
    driving_license = forms.CharField(required=False,max_length=30, widget = forms.TextInput(attrs={ 'class': 'form-control'}), label="Driving License No")
    security_license = forms.CharField(required=False,max_length=30, widget = forms.TextInput(attrs={ 'class': 'form-control'}), label="Security License No")
    profile_picture = forms.ImageField(required=False, help_text="*Keep Blank if you want to keep old picture. Choose <2MB image size", error_messages = {'invalid':{"Image Files Only"}}, widget=forms.FileInput(attrs={ 'class': 'form-control'}))
    document_image  = forms.ImageField(required=False, help_text="*Keep Blank if you want to keep old picture. Choose <2MB image size", error_messages = {'invalid':{"Image Files Only"}}, widget=forms.FileInput(attrs={ 'class': 'form-control'}))

    
    class Meta:
        model = EmployeeProfile
        fields = ['address','phone_number','driving_license','profile_picture','document_image','security_license']
    
    # Add some custom validation to our image field
    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture', True)
        if profile_picture:
            if profile_picture.size > 2*1024*1024:
                raise ValidationError("Profile Picture file too large ( > 2MB )")
            return profile_picture
        else:
            return False


    def clean_document_image(self):
        document_image = self.cleaned_data.get('document_image', True)
        if document_image:
            if document_image.size > 2*1024*1024:
                raise ValidationError("Document file too large ( > 2MB )")
            return document_image
        else:
            return False    



    
