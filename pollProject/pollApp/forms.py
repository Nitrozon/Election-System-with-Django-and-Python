from django import forms

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField()

class AdmissionNumberLoginForm(forms.Form):
    admission_no = forms.CharField(max_length=20)