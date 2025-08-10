from django.db import models
from django.contrib.auth.models import User

class Website(models.Model):
    url = models.URLField(unique=True)
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
    

class ScanSession(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    PROFILE_CHOICES = [
        ('all', 'All Modules'),
        ('passive', 'Passive Only'),
        ('footprint', 'Footprint'),
        ('investigate', 'Investigate'),
    ]

    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scan_sessions")
    name = models.CharField(max_length=255)  # NEW: user-given scan name
    target_input = models.CharField(max_length=255, db_index=True)  # e.g., domain.com or IP
    target_type = models.CharField(max_length=50, blank=True, null=True)  # NEW: domain/ip/email/etc.
    profile = models.CharField(max_length=20, choices=PROFILE_CHOICES, default='all')  # NEW
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)

    def __str__(self):
        return f"{self.name} ({self.target_input}) - {self.status}"


class ReconResult(models.Model):
    session = models.ForeignKey(ScanSession, on_delete=models.CASCADE, related_name="recon_results")
    tool_name = models.CharField(max_length=100, db_index=True)
    output = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[Recon] {self.tool_name} - {self.session.target_input}"


class EnumerationResult(models.Model):
    session = models.ForeignKey(ScanSession, on_delete=models.CASCADE, related_name="enum_results")
    tool_name = models.CharField(max_length=100, db_index=True)
    output = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[Enum] {self.tool_name} - {self.session.target_input}"


class VulnScanResult(models.Model):
    session = models.ForeignKey(ScanSession, on_delete=models.CASCADE, related_name="vuln_results")
    vuln_name = models.CharField(max_length=255, db_index=True)
    severity = models.CharField(max_length=50, db_index=True)  # Low, Medium, High, Critical
    description = models.TextField()
    output = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[Vuln] {self.vuln_name} ({self.severity}) - {self.session.target_input}"


class ExploitResult(models.Model):
    session = models.ForeignKey(ScanSession, on_delete=models.CASCADE, related_name="exploit_results")
    exploit_name = models.CharField(max_length=255, db_index=True)
    source = models.CharField(max_length=255, db_index=True)  # Exploit-DB, CVE, etc.
    status = models.CharField(max_length=50, db_index=True)  # Success, Failed
    output = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[Exploit] {self.exploit_name} ({self.status}) - {self.session.target_input}"


class FinalReport(models.Model):
    session = models.ForeignKey(ScanSession, on_delete=models.CASCADE, related_name="final_reports")
    pdf_path = models.FileField(upload_to='reports/pdf/', null=True, blank=True)
    html_path = models.FileField(upload_to='reports/html/', null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Final Report - {self.session.target_input} ({self.generated_at.strftime('%Y-%m-%d')})"
