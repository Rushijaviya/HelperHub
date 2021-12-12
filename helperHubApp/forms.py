from django import forms
from django.contrib.auth.models import User
from .models import userInfo, Doctor, Tutor, Service_Provider, Logistic, Other


class userForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name']


class userInfoForm(forms.ModelForm):
    class Meta():
        model = userInfo
        fields = ['mobile_number', 'flat_no', 'occupation']


class doctorForm(forms.ModelForm):
    class Meta():
        model = Doctor
        fields = ['doctor', 'degree_type',
                  'specialities_type', 'dob', 'bio', 'gender', 'description']


class tutorForm(forms.ModelForm):
    class Meta():
        model = Tutor
        fields = ['tutor', 'degree_type',
                  'description', 'bio']


class service_providerForm(forms.ModelForm):
    class Meta():
        model = Service_Provider
        fields = ['service_provider', 'service_type',
                  'description', 'bio']


class logisticForm(forms.ModelForm):
    class Meta():
        model = Logistic
        fields = ['logistic', 'logistic_type',
                  'description', 'bio']


class otherForm(forms.ModelForm):
    class Meta():
        model = Other
        fields = ['other', 'description', 'bio']

class userInfoUpdateForm(forms.ModelForm):
    class Meta():
        model = userInfo
        fields = ("mobile_number", "flat_no", "occupation")

    # def save(self, commit=True):
    #     user_info = self.instance
    #     user_info.name = self.cleaned_data['name']
    #     user_info.phone = self.cleaned_data['mobile_number']

    #     if commit:
    #         user_info.save()

    #     return user_info