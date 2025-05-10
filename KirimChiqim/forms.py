from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    type = forms.ChoiceField(
        choices=Transaction.TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'typeSelect'
        })
    )
    category = forms.ChoiceField(
        choices=Transaction.KATEGORIYALAR,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'categorySelect'
        })
    )
    pul_turi = forms.ChoiceField(
        choices=Transaction.PUL_TURLARI,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    karta_nomi = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'kartaNom'})
    )

    valyuta_turi = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Tanlang'),
            ('USD', 'USD'),
            ('EUR', 'EUR'),
            ('RUB', 'RUB'),
        ],
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'valyutaTuri'})
    )

    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    class Meta:
        model = Transaction
        exclude = ['user']

class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )