from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student
from django.contrib import messages


def index(request):
    return render(request, "index.html")
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        # Perform basic validation
        if not name or not email or not password or not address:
            messages.error(request, 'All fields are required.')
        elif Student.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
        else:
            # Save the student to the database
            student = Student(name=name, email=email, password=password, address=address)
            student.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')  # Redirect to login page after successful registration

    return render(request, 'registration.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the email and password match a student in the database
        try:
            student = Student.objects.get(email=email, password=password)
        except Student.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')

        # If the student exists, create a session for the user
        request.session['student_id'] = student.id
        request.session['student_name'] = student.name
        messages.success(request, f'Welcome, {student.name}!')
        return redirect('dashboard')  # Redirect to the dashboard page after successful login

    return render(request, 'login.html')

def dashboard(request):
    # Check if student_id exists in session (i.e., if user is logged in)
    if 'student_id' in request.session:
        student_id = request.session['student_id']
        try:
            student = Student.objects.get(id=student_id)
            return render(request, 'dashboard.html', {'student': student})
        except Student.DoesNotExist:
            messages.error(request, 'Student does not exist.')
            return redirect('login')
    else:
        messages.error(request, 'You must be logged in to view the dashboard.')
        return redirect('login')






def logout(request):
    if 'student_id' in request.session:
        del request.session['student_id']
    if 'student_name' in request.session:
        del request.session['student_name']
    messages.success(request, 'You have been logged out.')
    return redirect('login')
