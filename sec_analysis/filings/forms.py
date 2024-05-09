# filings/forms.py
from django import forms

class TickerForm(forms.Form):
    ticker = forms.CharField(label='Enter Ticker Symbol', max_length=100)
