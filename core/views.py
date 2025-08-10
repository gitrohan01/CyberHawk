from django.shortcuts import render, redirect
from .forms import ScanForm
from .models import ScanSession
from django.utils import timezone

def home(request):
    if request.method == 'POST':
        form = ScanForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data['target']
            module = form.cleaned_data.get('module')  # if your form has module selection

            # Auto-generate scan name (optional)
            scan_name = f"Scan_{timezone.now().strftime('%Y%m%d_%H%M%S')}"

            # Save to DB
            scan = ScanSession.objects.create(
                name=scan_name,
                target=target,
                module=module,
                status="pending"  # you can track status: pending/running/completed
            )

            # Optionally: trigger scan logic here (Celery, subprocess, etc.)

            return redirect('results', scan_id=scan.id)
    else:
        form = ScanForm()
    
    return render(request, 'core/home.html', {'form': form})
