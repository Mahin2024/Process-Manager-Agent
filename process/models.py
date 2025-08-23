from django.db import models

class SystemInfo(models.Model):
    hostname = models.CharField(max_length=255, unique=True)
    ip = models.CharField(max_length=64, blank=True, default="")
    os = models.CharField(max_length=64, blank=True, default="")
    os_version = models.CharField(max_length=128, blank=True, default="")
    release = models.CharField(max_length=64, blank=True, default="")
    machine = models.CharField(max_length=64, blank=True, default="")
    processor = models.CharField(max_length=256, blank=True, default="")
    physical_cores = models.IntegerField(default=0)
    logical_cores = models.IntegerField(default=0)
    cpu_freq_current = models.FloatField(default=0)
    cpu_freq_max = models.FloatField(default=0)
    cpu_percent = models.FloatField(default=0)
    total_ram = models.BigIntegerField(default=0)
    boot_time = models.BigIntegerField(default=0)
    collected_at = models.CharField(max_length=64, blank=True, default="")
    updated_at = models.DateTimeField(auto_now=True)
    used_ram = models.BigIntegerField(default=0)
    available_ram = models.BigIntegerField(default=0)
    storage_total = models.BigIntegerField(default=0)
    storage_used = models.BigIntegerField(default=0)
    storage_free = models.BigIntegerField(default=0)

    def __str__(self):
        return self.hostname


class Process(models.Model):
    hostname = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    pid = models.IntegerField()
    ppid = models.IntegerField(default=0)
    cpu_percent = models.FloatField(default=0)
    memory_mb = models.FloatField(default=0)  # ADD THIS FIELD
    memory_percent = models.FloatField(default=0)
    exe_path = models.TextField(blank=True, default="")
    username = models.CharField(max_length=255, blank=True, default="")
    sample_time = models.BigIntegerField(default=0)
    create_time = models.BigIntegerField(default=0)  # Add this if needed

    def __str__(self):
        return f"{self.name} (PID: {self.pid})"

    class Meta:
        indexes = [
            models.Index(fields=['hostname']),
            models.Index(fields=['sample_time']),
        ]