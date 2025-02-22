from pyexpat import model
from flask import app, jsonify, request
from pages.models import Record
from django.shortcuts import render,redirect
from django.http import HttpResponse , JsonResponse
from django.contrib.auth.hashers import make_password
import re
from django.contrib import messages
from django.core.serializers import serialize
from django.db.models import Q,Sum
from django.utils.timezone import now,localdate,datetime
from auditlog.models import LogEntry
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json
from django.db import IntegrityError
from django.db import transaction 
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import pandas as pd
import os
from werkzeug.utils import secure_filename



def index(request):
    return render(request , 'pages/index.html')

def home(request):
    return render(request,'pages/home.html')

def validate_email(email):
    email_regex = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email)

def records_management(request):
    records = Record.objects.all()
    records_json = serialize('json', records)
    return render(request, 'pages/recordsmanagement.html', {'records_json': records_json})

@csrf_exempt  
def delete_record(request, record_id):
    if request.method == 'DELETE':
        try:
            record = get_object_or_404(Record, record_id=record_id)
            record.delete()
            return JsonResponse({'success': True, 'message': 'Record deleted successfully'}, status=200) #JSON Response
        except Record.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Record not found'}, status=404)  # 404 for not found
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)  # 500 for server error
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)



@csrf_exempt
def change_status(request, record_id):
    if request.method == 'POST':
        try:
            with transaction.atomic(): 
                record_id = int(record_id)  

                record = get_object_or_404(Record, record_id=record_id) # Use the correct field name

                data = json.loads(request.body.decode('utf-8'))
                new_status = data.get('status')

                if new_status not in ['accepted', 'rejected']:
                    current_status = record.label
                    new_status = 'rejected' if current_status == 'accepted' else 'accepted'

                record.label = new_status
                record.save()  # Now the label should update correctly
                return JsonResponse({'success': True, 'message': f'Status changed to {new_status}'}, status=200)

        except ValueError:  # Handle invalid record_id (not an integer)
            return JsonResponse({'success': False, 'message': 'Invalid record_id'}, status=400)
        except Record.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Record not found'}, status=404)
        except Exception as e:
            # Important: Log the error for debugging in production
            import logging
            logger = logging.getLogger(__name__)  # Get a logger instance
            logger.error(f"Error changing status: {e}") # Log the error
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


FLASK_API_URL = "http://127.0.0.1:5000/predict"

def analyze_activity(request):
    if request.method == "POST":
        suggestion = request.POST.get("text", "")
        
        if not suggestion:
            return JsonResponse({"error": "No suggestion provided"}, status=400)

        response = requests.post(FLASK_API_URL, json={"text": suggestion})
        return JsonResponse(response.json())

    return JsonResponse({"error": "Invalid request"}, status=400)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
import requests
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

FLASK_API_URL = "http://127.0.0.1:5000/upload"
@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file part'}, status=400)
        file = request.FILES['file']
        if file.name == '':
            return JsonResponse({'error': 'No selected file'}, status=400)

        if file:
            filename = secure_filename(file.name)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            with open(filepath, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Send file to Flask API
            with open(filepath, 'rb') as f:
                response = requests.post(FLASK_API_URL, files={'file': f})

            try:
                response_data = response.json()
            except ValueError:
                return JsonResponse({'error': 'Invalid response from Flask API'}, status=500)

            return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request'}, status=400)
