
from django import forms
from userprofile.models import UserProfile,Address
from account.models import CustomUser


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False,error_messages={'invalid':("image files only")},widget=forms.FileInput) 
    class Meta:
        model = UserProfile
        fields = ('address_line_1','address_line_2','city','state','country','profile_picture')

    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)   

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','phone','email')

    def __init__(self,*args,**kwargs):
        super(CustomUserForm,self).__init__(*args,**kwargs)   

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'




class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields=['first_name','last_name','phone','email','address_line1','address_line2','country','state','city']
    
    def __init__(self, *args, **kwargs):
      super(AddressForm,self).__init__(*args, **kwargs)  
      for field  in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'