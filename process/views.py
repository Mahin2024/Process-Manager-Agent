from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Max
from .models import SystemInfo, Process
from .serializers import SystemInfoSerializer, ProcessSerializer
from django.shortcuts import render
from django.http import JsonResponse

def index_view(request):
    return render(request, 'index.html')

@api_view(["POST"])
def system_info_upsert(request):
    data = request.data
    hostname = data.get("hostname")
    if not hostname:
        return Response({"hostname": ["Required"]}, status=400)
    obj, _ = SystemInfo.objects.update_or_create(hostname=hostname, defaults=data)
    return Response(SystemInfoSerializer(obj).data)

@api_view(["POST"])
def processes_bulk(request):
    items = request.data
    if not isinstance(items, list) or not items:
        return Response({"detail": "Expected non-empty list"}, status=400)
    for it in items:
        if not it.get("hostname") or not it.get("name"):
            return Response({"detail": "hostname and name required"}, status=400)
    ser = ProcessSerializer(data=items, many=True)
    ser.is_valid(raise_exception=True)
    Process.objects.bulk_create([Process(**obj) for obj in ser.validated_data])
    return Response({"created": len(items)})

@api_view(["GET"])
def system_info_get(request, hostname):
    # Get the latest system info for this hostname
    obj = SystemInfo.objects.filter(hostname=hostname).order_by('-updated_at').first()
    if not obj:
        return Response({"detail": "System info not found"}, status=404)
    return Response(SystemInfoSerializer(obj).data)

@api_view(["GET"])
def system_info_list(request):
    # Get the latest system info for each hostname
    latest_ids = SystemInfo.objects.values('hostname').annotate(
        latest_id=Max('id')
    ).values_list('latest_id', flat=True)
    
    qs = SystemInfo.objects.filter(id__in=latest_ids)
    return Response(SystemInfoSerializer(qs, many=True).data)

@api_view(["GET"])
def processes_query(request):
    hostname = request.query_params.get("hostname")
    qs = Process.objects.all()
    if hostname:
        qs = qs.filter(hostname=hostname)
    
    # Get the latest sample time
    latest_sample = qs.order_by('-sample_time').first()
    if latest_sample:
        # Get only processes from the latest sample
        qs = qs.filter(sample_time=latest_sample.sample_time)
    
    qs = qs.order_by("-memory_mb")[:500]  # Order by memory usage
    return Response(ProcessSerializer(qs, many=True).data)

def processes_list(request):
    hostname = request.GET.get('hostname')
    queryset = Process.objects.filter(hostname=hostname)
    # Remove any .distinct()/.order_by()/.limit() unless needed
    data = list(queryset.values())
    return JsonResponse(data, safe=False)