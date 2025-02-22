from django.shortcuts import render
from django.utils.timezone import localdate
from django.db.models import Sum
from ..models import Record
import json
from auditlog.models import LogEntry


def admindashboard(request):
    total_records = Record.objects.count() 
    total_accepted = Record.objects.filter(label='accepted').count() 
    total_rejected = Record.objects.filter(label='rejected').count()
     
    entries = LogEntry.objects.all()[:10]
    parsed_entries = []
    for entry in entries:
        changes_dict = entry.changes if isinstance(entry.changes, dict) else json.loads(entry.changes) if entry.changes else {}
        changes_items = list(changes_dict.items())
        
        parsed_entries.append({
            'id': entry.id,
            'action': entry.get_action_display(),
            'actor': entry.actor,
            'content_type': entry.content_type,
            'object_repr': entry.object_repr,
            'changes': changes_items, 
            'timestamp': entry.timestamp,
        })
    context = {
        'entries': parsed_entries,
        'admin_name': request.session.get('admin_name'),
        'admin_email': request.session.get('admin_email'),
        'total_records': total_records,
        'total_accepted': total_accepted,
        'total_rejected': total_rejected,
    }
    return render(request, 'pages/admindashboard.html', context)

