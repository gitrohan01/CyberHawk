from django.db import models 
from django.contrib.auth.models import User


class Website(models.Model):
    url = models.URLField(max_length=191, unique=True)  # ✅ reduced for safe indexing
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
    name = models.CharField(max_length=255)  # ✅ not indexed, 255 is fine
    target_input = models.CharField(max_length=191, db_index=True)  # ✅ reduced
    target_type = models.CharField(max_length=50, blank=True, null=True)
    profile = models.CharField(max_length=20, choices=PROFILE_CHOICES, default='all')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)  # ✅ short, safe
    modules_run = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.name} ({self.target_input}) - {self.status}"


class ReconResult(models.Model):
    session = models.ForeignKey(ScanSession, on_delete=models.CASCADE, related_name="recon_results")
    website = models.ForeignKey(Website, on_delete=models.CASCADE, null=True, blank=True)
    target = models.CharField(max_length=191, null=True, blank=True)  # ✅ reduced

    tool_name = models.CharField(max_length=100, db_index=True)  # ✅ safe
    raw_log = models.TextField()
    tabular_data = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[Recon] {self.tool_name} - {self.session.target_input}"


class EnumerationResult(models.Model):
    session = models.ForeignKey(ScanSession, on_delete=models.CASCADE, related_name="enum_results")
    tool_name = models.CharField(max_length=100, db_index=True)  # ✅ safe
    output = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[Enum] {self.tool_name} - {self.session.target_input}"


class VulnScanResult(models.Model):
    session = models.ForeignKey(ScanSession, on_delete=models.CASCADE, related_name="vuln_results")
    vuln_name = models.CharField(max_length=191, db_index=True)  # ✅ reduced
    severity = models.CharField(max_length=50, db_index=True)   # ✅ short, safe
    description = models.TextField()
    output = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[Vuln] {self.vuln_name} ({self.severity}) - {self.session.target_input}"


class ExploitResult(models.Model):
    session = models.ForeignKey(ScanSession, on_delete=models.CASCADE, related_name="exploit_results")
    exploit_name = models.CharField(max_length=191, db_index=True)  # ✅ reduced
    source = models.CharField(max_length=191, db_index=True)       # ✅ reduced
    status = models.CharField(max_length=50, db_index=True)        # ✅ safe
    output = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[Exploit] {self.exploit_name} ({self.status}) - {self.session.target_input}"


class FinalReport(models.Model):
    session = models.ForeignKey(ScanSession, on_delete=models.CASCADE, related_name="final_reports")
    pdf_path = models.FileField(upload_to='reports/pdf/', null=True, blank=True)
    html_path = models.FileField(upload_to='reports/html/', null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    modules_included = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Final Report - {self.session.target_input} ({self.generated_at.strftime('%Y-%m-%d')})"


class DigRecord(models.Model):
    RECORD_TYPES = [
        ('A', 'A'),
        ('AAAA', 'AAAA'),
        ('CNAME', 'CNAME'),
        ('MX', 'MX'),
        ('NS', 'NS'),
        ('TXT', 'TXT'),
        ('SOA', 'SOA'),
        ('PTR', 'PTR'),
    ]
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='dig_records')
    record_type = models.CharField(max_length=10, choices=RECORD_TYPES)
    ttl = models.IntegerField(null=True, blank=True)
    record_name = models.CharField(max_length=191)  
    record_data = models.CharField(max_length=512)  
    mx_priority = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['website', 'record_type']),
        ]
        unique_together = ('website', 'record_type', 'record_name')
