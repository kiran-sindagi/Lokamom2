from django import forms

class ContributeForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    age = forms.IntegerField(label="Age")
    email = forms.EmailField(label="Email ID")
    CHOICES = [
        ('conduct sessions', 'Conduct sessions'),
        ('submit articles', 'Submit articles'),
        ('monetary contribution', 'Monetary contribution'),
        ('others','Others')
    ]
    contribution = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Contribute with respect to: "
    )
    elaborate = forms.CharField(max_length=500, label="Please elaborate", required=False)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    age = forms.IntegerField(label="Age")
    email = forms.EmailField(label="Email ID")
    reason = forms.CharField(max_length=500, label="Reason for contacting", required=False)