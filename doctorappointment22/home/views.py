from django.shortcuts import render, redirect,get_object_or_404
from .models import Doctor, Appointment, ContactMessage,Profile
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# Create your views here.

def homefn(request):
    return render(request,'home.html')

def aboutusfn(request):
    return render(request,'about.html')

def locationfn(request):
    return render(request,'ourlocation.html')

def servicesfn(request):
    return render(request,'services.html')


# def contactfn(request):
#     return render(request,'contact1.html')



def booking_view(request):
    doctors = Doctor.objects.all()

    if request.method == 'POST':
        name = request.POST.get('patient_name')
        email = request.POST.get('patient_email')
        phone = request.POST.get('patient_phone')
        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        message = request.POST.get('message')

        doctor = Doctor.objects.get(id=doctor_id)

        Appointment.objects.create(
            patient_name=name,
            patient_email=email,
            patient_phone=phone,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            message=message
        )
        return redirect('booking_success')  

    return render(request, 'booking.html', {'doctors': doctors})



def booking_success(request):
    return render(request, 'booking_success.html')



def contact_view(request):
    success = False

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save to the database
        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )

        success = True  # To show the success message

    return render(request, 'contact.html', {'success': success})




def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                profile = Profile.objects.get(user=user)
                if profile.role == "admin":
                    return redirect("admin_dashboard")
                elif profile.role == "doctor":
                    return redirect("doctor_dashboard")
                elif profile.role == "patient":
                    return redirect("patient_dashboard")
                else:
                    messages.error(request, "Unknown role.")
                    return redirect("login")
            except Profile.DoesNotExist:
                messages.error(request, "Profile not found for this user.")
                return redirect("login")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('/')  # Redirect to your login page




@login_required(login_url='/login')
def admindashboardfn(request):
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.all()
    contact_messages = ContactMessage.objects.all().order_by('-sent_at')
    total_doctors = doctors.count()
    total_appointments = appointments.count()
    total_messages = contact_messages.count()


    context = {
        'doctors': doctors,
        'appointments': appointments,
        'contact_messages': contact_messages,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'total_messages': total_messages,
    }
    return render(request, 'admin_dashboard.html', context)

def doctor_dashboard(request):
    return render(request, "doctor_dashboard.html")

def patient_dashboard(request):
    return render(request, "patient_dashboard.html")




@login_required(login_url='/login')
def add_doctor(request):
    if request.method == "POST":
        Doctor.objects.create(
            name=request.POST["name"],
            specialization=request.POST["specialization"],
            email=request.POST["email"],
            phone=request.POST["phone"],
            available_days=request.POST["available_days"],
            start_time=request.POST["start_time"],
            end_time=request.POST["end_time"],
        )
        return redirect("admin_dashboard")
    return redirect("admin_dashboard")


@login_required(login_url='/login')
def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == "POST":
        doctor.name = request.POST["name"]
        doctor.specialization = request.POST["specialization"]
        doctor.email = request.POST["email"]
        doctor.phone = request.POST["phone"]
        doctor.available_days = request.POST["available_days"]
        doctor.start_time = request.POST["start_time"]
        doctor.end_time = request.POST["end_time"]
        doctor.save()
        return redirect("admin_dashboard")

    return render(request, "editdoctor.html", {"doctor": doctor})


@login_required(login_url='/login')
def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.delete()
    return redirect("admin_dashboard")


@login_required(login_url='/login')
def confirm_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = "Confirmed"
    appointment.save()
    return redirect("admin_dashboard")


@login_required(login_url='/login')
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = "Cancelled"
    appointment.save()
    return redirect("admin_dashboard")

@login_required(login_url='/login')
def add_appointment(request):
    if request.method == 'POST':
        patient_name = request.POST['patient_name']
        doctor_id = request.POST['doctor']
        date = request.POST['appointment_date']
        time = request.POST['appointment_time']

        Appointment.objects.create(
            patient_name=patient_name,
            doctor_id=doctor_id,
            appointment_date=date,
            appointment_time=time,
            status='Pending'
        )
        return redirect('admin_dashboard')
    return redirect("admin_dashboard")



@login_required(login_url='/login')
def delete_message(request, message_id):
    msg = get_object_or_404(ContactMessage, id=message_id)
    msg.delete()
    # messages.success(request, "Message deleted successfully.")
    return redirect('admin_dashboard')


