from django.shortcuts import render, redirect
from .forms import ScanForm
from .models import ScanSession   # Assuming you store scans like this

def home(request):
    if request.method == 'POST':
        form = ScanForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data['target']
            # Process the scan logic (placeholder)
            # You can kick off a scanner or save the target
            return redirect('results')  # Redirect to results or a summary page
    else:
        form = ScanForm()
    return render(request, 'core/home.html', {'form': form})
