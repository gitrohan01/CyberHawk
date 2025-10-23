from django.contrib import admin
from django.utils.html import format_html
import json
from .models import (
    Website,
    ScanSession,
    ReconResult,
    EnumerationResult,
    VulnScanResult,
    ExploitResult,
    FinalReport,
    DigRecord,
)

# ------------------------
# Website
# ------------------------
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ("id", "url", "scanned_at")
    search_fields = ("url",)


# ------------------------
# ScanSession
# ------------------------
class ScanSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "target_input", "status", "profile", "start_time", "end_time")
    list_filter = ("status", "profile", "start_time")
    search_fields = ("name", "target_input", "admin__username")
    readonly_fields = ("start_time", "end_time")


# ------------------------
# ReconResult
# ------------------------
class ReconResultAdmin(admin.ModelAdmin):
    list_display = ("id", "tool_name", "session", "website", "created_at")
    list_filter = ("tool_name", "created_at", "session__status")
    search_fields = ("tool_name", "target", "website__url", "session__target_input")
    readonly_fields = ("session", "website", "tool_name", "target",
                       "created_at", "raw_log_pretty", "tabular_data_table")

    def raw_log_pretty(self, obj):
        return format_html(
            "<pre style='max-height:300px;overflow:auto;'>{}</pre>",
            obj.raw_log or ""
        )
    raw_log_pretty.short_description = "Raw Log"

    def tabular_data_table(self, obj):
        if not obj.tabular_data:
            return "-"
        try:
            data = obj.tabular_data
            if isinstance(data, str):
                data = json.loads(data)

            # Case 1: list of dicts → make table
            if isinstance(data, list) and all(isinstance(i, dict) for i in data):
                headers = set()
                for row in data:
                    headers.update(row.keys())
                headers = list(headers)

                table_html = "<div style='max-width:100%;overflow:auto;'>"
                table_html += "<table border='1' style='border-collapse:collapse;width:100%;'>"
                table_html += "<tr>" + "".join(f"<th style='padding:4px;background:#f0f0f0;'>{h}</th>" for h in headers) + "</tr>"

                for row in data:
                    table_html += "<tr>" + "".join(
                        f"<td style='padding:4px;'>{row.get(h, '')}</td>" for h in headers
                    ) + "</tr>"
                table_html += "</table></div>"
                return format_html(table_html)

            # Case 2: dict → key-value table
            if isinstance(data, dict):
                table_html = "<table border='1' style='border-collapse:collapse;width:100%;'>"
                for k, v in data.items():
                    table_html += f"<tr><th style='padding:4px;background:#f0f0f0;'>{k}</th><td style='padding:4px;'>{v}</td></tr>"
                table_html += "</table>"
                return format_html(table_html)

            # Fallback: raw JSON
            return format_html("<pre>{}</pre>", json.dumps(data, indent=2, ensure_ascii=False))

        except Exception as e:
            return format_html("<pre>Error rendering data: {}</pre>", str(e))

    tabular_data_table.short_description = "Tabular Data"


# ------------------------
# EnumerationResult
# ------------------------
class EnumerationResultAdmin(admin.ModelAdmin):
    list_display = ("id", "tool_name", "session", "created_at")
    list_filter = ("tool_name", "created_at")
    search_fields = ("tool_name", "session__target_input")
    readonly_fields = ("session", "tool_name", "created_at", "output")


# ------------------------
# VulnScanResult
# ------------------------
class VulnScanResultAdmin(admin.ModelAdmin):
    list_display = ("id", "vuln_name", "severity", "session", "created_at")
    list_filter = ("severity", "created_at")
    search_fields = ("vuln_name", "session__target_input")
    readonly_fields = ("session", "vuln_name", "severity", "description", "output", "created_at")


# ------------------------
# ExploitResult
# ------------------------
class ExploitResultAdmin(admin.ModelAdmin):
    list_display = ("id", "exploit_name", "status", "session", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("exploit_name", "session__target_input", "source")
    readonly_fields = ("session", "exploit_name", "status", "source", "output", "created_at")


# ------------------------
# FinalReport
# ------------------------
class FinalReportAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "generated_at")
    list_filter = ("generated_at",)
    search_fields = ("session__target_input",)
    readonly_fields = ("session", "generated_at", "modules_included")


# ------------------------
# DigRecord
# ------------------------
class DigRecordAdmin(admin.ModelAdmin):
    list_display = ("website", "record_type", "record_name", "record_data", "ttl", "mx_priority", "created_at")
    list_filter = ("record_type", "created_at")
    search_fields = ("website__url", "record_name", "record_data")


# ------------------------
# Register Models
# ------------------------
admin.site.register(Website, WebsiteAdmin)
admin.site.register(ScanSession, ScanSessionAdmin)
admin.site.register(ReconResult, ReconResultAdmin)
admin.site.register(EnumerationResult, EnumerationResultAdmin)
admin.site.register(VulnScanResult, VulnScanResultAdmin)
admin.site.register(ExploitResult, ExploitResultAdmin)
admin.site.register(FinalReport, FinalReportAdmin)
admin.site.register(DigRecord, DigRecordAdmin)
