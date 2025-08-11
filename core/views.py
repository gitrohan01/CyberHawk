from django.shortcuts import render, redirect, get_object_or_404
from .forms import ScanForm
from .models import ScanSession, ReconResult, EnumerationResult  # Add more result models
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings


def custom_admin_login(request):
    if request.user.is_authenticated:
        return redirect('/admin/')  # Already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:  # Ensure it's an admin/staff account
            login(request, user)
            return redirect('/admin/')
        else:
            messages.error(request, "Invalid credentials or not an admin.")

    return render(request, 'custom_admin_login.html')

# Home page (New Scan form)
def home(request):
    if request.method == 'POST':
        form = ScanForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data['target']
            module = form.cleaned_data.get('module')  # if your form has module selection

            # Auto-generate scan name
            scan_name = f"Scan_{timezone.now().strftime('%Y%m%d_%H%M%S')}"

            # Save to DB
            scan = ScanSession.objects.create(
                name=scan_name,
                target=target,
                module=module,
                status="pending"  # Track status: pending/running/completed
            )

            # TODO: Trigger scan logic here (Celery, subprocess, etc.)

            return redirect('results', scan_id=scan.id)
    else:
        form = ScanForm()
    
    return render(request, 'core/home.html', {'form': form})


# Scan Results (main results page for one scan)
def results(request, scan_id):
    scan = get_object_or_404(ScanSession, id=scan_id)
    # You can combine results from all modules here
    recon_data = ReconResult.objects.filter(scan=scan)
    enumeration_data = EnumerationResult.objects.filter(scan=scan)
    return render(request, "core/results.html", {
        "scan": scan,
        "recon_data": recon_data,
        "enumeration_data": enumeration_data,
    })


# Individual pages
def info_results(request):
    results = ReconResult.objects.all().select_related('session')  # <-- changed here
    return render(request, "core/infogathering_results.html", {"results": results})

def enumeration_results(request):
    results = EnumerationResult.objects.all().select_related('session')  # fix field name here too
    return render(request, "core/enumeration_results.html", {"results": results})

def service_results(request):
    results = []  # or query your model when ready
    # Temporarily render a different existing template
    return render(request, "core/placeholder.html", {"results": results})

def web_results(request):
    results = []  # Replace with your Web Exploitation model query
    return render(request, "core/web_results.html", {"results": results})

def report(request):
    reports = []  # Replace with your report model/query
    return render(request, "core/report.html", {"reports": reports})

