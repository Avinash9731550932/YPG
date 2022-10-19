from django import forms
from .models import Asset
from django.core.exceptions import ValidationError
 
# creating a form
class AssetForm(forms.ModelForm):

    car_name       = forms.CharField(max_length=100, 
        widget = forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})
    )

    car_model       = forms.CharField(max_length=100, required=False, 
        widget = forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})
    )

    plate_number    = forms.CharField(max_length=100, required=False,
        widget = forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})
    )

    car_image       = forms.ImageField(required=False, help_text="*Keep Blank if you want to keep old picture. Choose <2MB image size", error_messages = {'invalid':{"Image Files Only"}}, widget=forms.FileInput(attrs={ 'class': 'form-control'}))
    


    
    class Meta:
        model = Asset
        fields = ['car_name','car_model','plate_number','car_image','is_available']

    # Add some custom validation to our image field
    def clean_car_image(self):
        car_image = self.cleaned_data.get('car_image', True)
        if car_image:
            if car_image.size > 2*1024*1024:
                raise ValidationError("Car Image file too large ( > 2MB )")
            return car_image
        else:
            return False