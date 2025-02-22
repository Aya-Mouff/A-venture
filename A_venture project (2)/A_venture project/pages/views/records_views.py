from django.shortcuts import render, get_object_or_404
from django.core.serializers import serialize
from django.http import JsonResponse
from ..models import Record
#done
def recordsmanagement(request):
    record= Record.objects.all()
    record_json = serialize('json', record)  
    return render(request, 'pages/recordsmanagement.html', {"record_json": record_json})

def delete_record(request, record_id):
    if request.method == 'DELETE':
        record = get_object_or_404(Record, record_id=record_id)
        record.delete()
        return JsonResponse({'success': True, 'message': 'Record deleted successfully '}, status=200)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
