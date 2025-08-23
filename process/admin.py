from django.contrib import admin
from .models import SystemInfo, Process

@admin.register(SystemInfo)
class SystemInfoAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'os', 'processor', 'logical_cores', 'total_ram', 'updated_at')
    list_filter = ('os', 'updated_at')
    search_fields = ('hostname', 'processor')
    readonly_fields = ('updated_at',)

@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ('name', 'pid', 'hostname', 'memory_mb', 'cpu_percent', 'sample_time')
    list_filter = ('hostname', 'name', 'sample_time')
    search_fields = ('name', 'hostname', 'pid')
    readonly_fields = ('sample_time',)