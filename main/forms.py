from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='نام', max_length=100)
    email = forms.EmailField(label='ایمیل')
    phone = forms.CharField(label='تلفن', max_length=15, required=False)
    subject = forms.CharField(label='موضوع', max_length=200)
    message = forms.CharField(label='پیام', widget=forms.Textarea)