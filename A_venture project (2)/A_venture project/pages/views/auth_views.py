from django.shortcuts import render, redirect  
from ..models import User
import re
from django.views.decorators.csrf import csrf_exempt
#done
@csrf_exempt
def login(request):
    request.session.clear()
    if request.method == 'POST':
        # Get the username or email and password
        username_or_email = request.POST['username'].strip()
        password = request.POST['password'].strip()

        try:
            # Check if the input is an email
            if re.match(r"[^@]+@[^@]+\.[^@]+", username_or_email):  # Email validation
                user = User.objects.get(email=username_or_email)
            else:
                user = User.objects.get(name=username_or_email)

            # Check if user is active
            if user.status == 'active':
                # Check if password matches
                if password == user.password:  # Use check_password if passwords are hashed
                    # Store session data based on role
                    if user.role == 'admin':
                        request.session['admin_name'] = user.name
                        request.session['admin_email'] = user.email
                        return redirect('admin_dashboard')
                else:
                    return render(request, 'pages/login.html', {'error_message': 'Incorrect password.'})
            else:
                return render(request, 'pages/login.html', {'error_message': 'User is not active.'})
        except User.DoesNotExist:
            return render(request, 'pages/login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'pages/login.html')

def logout(request):
    request.session.clear()
    return redirect('login')