from sre_constants import CATEGORY_UNI_SPACE
from django import forms
import datetime
from hs_incidents.models import HS_incident
from django.forms.widgets import SelectDateWidget, RadioSelect, Textarea, PasswordInput, TextInput
from django.contrib.auth.forms import AuthenticationForm


class RFPAuthForm(AuthenticationForm):
    username = forms.CharField(
        widget=TextInput(
            attrs={
                'class': 'rui-text-input__input rui-text-input__single-line',
                'type': 'email',
                'placeholder': 'user@domain.com'
            }
        )
    )
    password = forms.CharField(
        widget=PasswordInput(
            attrs={
                'class': 'rui-text-input__input rui-text-input__single-line',
                'placeholder':'Password'
            }
        )
    )

class HSIncidentForm(forms.ModelForm):

    class Meta:
        model=HS_incident
        fields = '__all__'
        widgets = {
            'incident_classification': RadioSelect(attrs={'class': 'rui-radio__control'}),
            'work_related': RadioSelect(attrs={'class': 'rui-radio__control'}),
            'auth_notified': RadioSelect(attrs={'class': 'rui-radio__control'}),
            'description': Textarea,
            'location': RadioSelect(attrs={'class': 'rui-radio__control'}),
            'date_occurred': SelectDateWidget(attrs={'class': 'rui-text-input__input rui-text-input__single-line'}),
            'date_reported': SelectDateWidget(attrs={'class': 'rui-text-input__input rui-text-input__single-line'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['business_activity'].widget.attrs.update({'class': 'rui-combobox__control'})
        self.fields['jti_site'].widget.attrs.update({'class': 'rui-combobox__control'})
        self.fields['latitude'].widget.attrs.update({'class': 'rui-combobox__control'})
        self.fields['longitude'].widget.attrs.update({'class': 'rui-combobox__control'})

    def clean(self):
        super(HSIncidentForm, self).clean()
            
        date_occurred = self.cleaned_data.get('date_occurred')
        date_reported = self.cleaned_data.get('date_reported')
        location = self.cleaned_data.get('location')
        jti_site = self.cleaned_data.get('jti_site')
        latitude = self.cleaned_data.get('latitude')
        longitude = self.cleaned_data.get('longitude')
        incident_classification = self.cleaned_data.get('incident_classification')
        consequence = self.cleaned_data.get('consequence')
        age = self.cleaned_data.get('age')
        gender = self.cleaned_data.get('gender')

        if incident_classification == '2':
            if not consequence:
                self._errors['consequence'] = self.error_class([
                    'Consequence should be specified for occupational health incidents'])
            if not age:
                self._errors['age'] = self.error_class([
                    'Age should be specified for occupational health incidents'])
            if not gender:
                self._errors['gender'] = self.error_class([
                    'Gender should be specified for occupational health incidents'])

        if location == 'Onsite' and not jti_site:
            self._errors['jti_site'] = self.error_class([
                'JTI Site not specified for onsite incident'])

        if location == 'Offsite':
            if not latitude:
                self._errors['latitude'] = self.error_class([
                    'Latitude not specified for offsite incident'])
            elif latitude < 25 or latitude > 40:
                self._errors['latitude'] = self.error_class([
                    'Location should be within Iran'])
            if not longitude:
                self._errors['longitude'] = self.error_class([
                    'Longitude not specified for offsite incident'])
            elif longitude < 44 or longitude > 64:
                self._errors['longitude'] = self.error_class([
                    'Location should be within Iran'])

        if not date_occurred:
            self._errors['date_occurred'] = self.error_class([
                'Non existing occurred date selected'])
        if not date_reported:
            self._errors['date_reported'] = self.error_class([
                'Non existing occurred date selected'])

        if date_occurred and date_reported:
            if date_reported < date_occurred:
                self._errors['date_occurred'] = self.error_class([
                    'Date occurred can not be later than date reported'])

            if date_reported > datetime.datetime.today().date():
                self._errors['date_reported'] = self.error_class([
                    'Date reported can not be in the future'])

            if date_occurred > datetime.datetime.today().date():
                self._errors['date_occurred'] = self.error_class([
                    'Date occurred can not be in the future'])

        return self.cleaned_data
    