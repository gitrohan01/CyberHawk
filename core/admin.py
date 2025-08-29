from django.contrib import admin
from django.apps import apps
from .models import ReconResult, ScanSession, Website, EnumerationResult, VulnScanResult, ExploitResult, FinalReport

# ------------------------------
# Custom Admin for key models
# ------------------------------

@admin.register(ReconResult)
class ReconResultAdmin(admin.ModelAdmin):
    list_display = ('tool_name', 'session', 'target', 'created_at')
    readonly_fields = ('raw_log', 'tabular_data')
    search_fields = ('tool_name', 'target')
    list_filter = ('tool_name', 'session')

@admin.register(ScanSession)
class ScanSessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'target_input', 'status', 'start_time', 'end_time')
    readonly_fields = ('modules_run',)
    search_fields = ('name', 'target_input')
    list_filter = ('status', 'profile')

@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('url', 'scanned_at')
    search_fields = ('url',)

@admin.register(VulnScanResult)
class VulnScanResultAdmin(admin.ModelAdmin):
    list_display = ('vuln_name', 'severity', 'session', 'created_at')
    readonly_fields = ('output',)
    list_filter = ('severity',)

@admin.register(EnumerationResult)
class EnumerationResultAdmin(admin.ModelAdmin):
    list_display = ('tool_name', 'session', 'created_at')
    readonly_fields = ('output',)
    search_fields = ('tool_name',)

@admin.register(ExploitResult)
class ExploitResultAdmin(admin.ModelAdmin):
    list_display = ('exploit_name', 'status', 'session', 'created_at')
    readonly_fields = ('output',)
    search_fields = ('exploit_name', 'status')

@admin.register(FinalReport)
class FinalReportAdmin(admin.ModelAdmin):
    list_display = ('session', 'generated_at')
    readonly_fields = ('pdf_path', 'html_path', 'modules_included')

# ------------------------------
# Dynamically register other minor models
# ------------------------------
app = apps.get_app_config('core')

for model_name, model in app.models.items():
    if model not in [ReconResult, ScanSession, Website, VulnScanResult, EnumerationResult, ExploitResult, FinalReport]:
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass
