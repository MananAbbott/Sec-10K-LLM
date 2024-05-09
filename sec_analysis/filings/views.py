# filings/views.py
from django.shortcuts import render
from .forms import TickerForm
from .analysis import analyze_10k_filings  # Make sure to move your analysis function to a module

def index(request):
    if request.method == 'POST':
        form = TickerForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data['ticker']
            insights = analyze_10k_filings(ticker)
            return render(request, 'filings/results.html', {'ticker': ticker, 'insights': insights})
    else:
        form = TickerForm()
    return render(request, 'filings/index.html', {'form': form})
