from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Printer, Owner, Appointment
from django.http import HttpResponse
from .forms import PrinterForm
from datetime import datetime


# Create your views here.

def index(request):
    appointment = Appointment.objects.all()
    return render(request, 'index.html', {'appointment': appointment})



def login(request):
    if request.method == 'POST':
        uid = request.POST['uid']
        password = request.POST['password']
        try:
            user = User.objects.get(uid=uid, upassword=password)
            request.session['uid'] = user.uid
            return redirect('dashboard')
        except User.DoesNotExist:
            error_message = "Invalid login credentials"
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        uid = request.POST['uid']
        password = request.POST['password']
        uname = request.POST['uname']
        uphone = request.POST['uphone']
        uemail = request.POST['uemail']
        try:
            user = User.objects.create(uid=uid, upassword=password, uname=uname, uphone=uphone,
                                       uemail=uemail)
            request.session['uid'] = user.uid
            return redirect('login')
        except Exception as e:
            error_message = str(e)
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')


def logout(request):
    del request.session['uid']
    return redirect('login')


def dashboard(request):
    if 'uid' not in request.session:
        return redirect('login')
    uid = request.session['uid']
    user = User.objects.get(uid=uid)

    # if user.ustatus == 'owner':
    #     return redirect('owner_dashboard')

    return render(request, 'dashboard.html', {'user': user})


def owner_dashboard(request):
    if 'owid' not in request.session:
        return redirect('owner_login')
    owid = request.session['owid']
    owner = Owner.objects.get(owid=owid)
    #user = owner.user  # Assuming there is a foreign key relationship between Owner and User

    appointment = Appointment.objects.filter(pid__owner__owid=owid)

    return render(request, 'owner_dashboard.html', {'owner': owner, 'appointment': appointment})


def printer(request):
    if request.method == 'POST':
        pname = request.POST['pname']
        pdescription = request.POST['pdescription']
        
        printer = Printer.objects.create(pname=pname, pdescription=pdescription)
        return redirect('printer')
    
    printer = Printer.objects.all()
    return render(request, 'printer.html', {'printer': printer})


def printer_detail(request, pid):
    printer = Printer.objects.get(pid=pid)
    return render(request, 'printer_detail.html', {'printer': printer})


def printer_edit(request, pid):
    if 'owid' not in request.session:
        return redirect('owner_login')
    owid = request.session['owid']
    owner = Owner.objects.get(owid=owid)

    printer = Printer.objects.get(pid=pid)
    if request.method == 'POST':
        printer.pname = request.POST['pname']
        printer.pdescription = request.POST['pdescription']
        printer.save()
        return redirect('printer')

    return render(request, 'printer_edit.html', {'printer': printer})

def printer_create(request):
    if 'owid' not in request.session:
        return redirect('owner_login')
    owid = request.session['owid']
    owner = Owner.objects.get(owid=owid)

    if request.method == 'POST':
        form = PrinterForm(request.POST)
        if form.is_valid():
            printer = form.save(commit=False)
            printer.owner = owner
            printer.save()
            return redirect('printer_detail', pid=printer.pid)  # Redirect to printer_detail view with the newly created printer ID
    else:
        form = PrinterForm()

    return render(request, 'printer_create.html', {'form': form, 'owner': owner})


def printer_delete(request, pid):
    if 'owid' not in request.session:
        return redirect('owner_login')
    owid = request.session['owid']
    owner = Owner.objects.get(owid=owid)

    printer = Printer.objects.get(pid=pid)
    printer.delete()
    return redirect('printer')


def appointment_create(request):
    if 'uid' not in request.session:
        return redirect('login')
    uid = request.session['uid']
    user = User.objects.get(uid=uid)

    if request.method == 'POST':
        pid = request.POST['pid']
        date = request.POST['date']
        programme = request.POST['programme']
        appointmentStatus = 'Pending'  # Set initial appointment status as pending
        appointment = Appointment.objects.create(pid_id=pid, uid_id=uid, date=date, programme=programme,
                                         appointmentStatus=appointmentStatus)
        return redirect('appointment_list')

    printer = Printer.objects.all()
    return render(request, 'appointment_create.html', {'user': user, 'printer': printer})


def appointment_list(request):
    if 'uid' not in request.session:
        return redirect('login')
    uid = request.session['uid']
    user = User.objects.get(uid=uid)

    # if user.ustatus == 'owner':
    #     appointment = Appointment.objects.filter(pid__owner__owid=uid)
    # else:
    appointment = Appointment.objects.filter(uid_id=uid)

    return render(request, 'appointment_list.html', {'appointment': appointment},)



def appointment_detail(request, appointmentId):
    appointment = Appointment.objects.get(appointmentId=appointmentId)
    return render(request, 'appointment_detail.html', {'appointment': appointment})



def appointment_edit(request, appointmentId):
    if 'uid' not in request.session:
        return redirect('login')
    uid = request.session['uid']
    user = User.objects.get(uid=uid)
    appointment = Appointment.objects.get(appointmentId=appointmentId)

    if user.uid != appointment.uid.uid:
        return redirect('appointment_list')

    if request.method == 'POST':
        date_str = request.POST['date']
        try:
            date = datetime.strptime(date_str, '%B %d, %Y').date()
            appointment.date = date.strftime('%Y-%m-%d')
            appointment.programme = request.POST['programme']
            appointment.save()
            return redirect('appointment_list')
        except ValueError:
            # Handle invalid date format error
            # You can display an error message or redirect to a form with errors
            pass

    printer = Printer.objects.all()
    return render(request, 'appointment_edit.html', {'appointment': appointment, 'printer': printer})

def appointment_delete(request, appointmentId):
    if 'uid' not in request.session:
        return redirect('login')
    uid = request.session['uid']
    user = User.objects.get(uid=uid)
    appointment = Appointment.objects.get(appointmentId=appointmentId)

    if user.uid != appointment.uid.uid:
        return redirect('appointment_list')

    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment_list')

    return render(request, 'appointment_delete.html', {'appointment': appointment})


def approve_appointment(request, appointmentId):
    if 'owid' not in request.session:
        return redirect('owner_login')
    owid = request.session['owid']
    owner = Owner.objects.get(owid=owid)

    appointment = Appointment.objects.get(appointmentId=appointmentId)
    appointment.appointmentStatus = 'Approved'
    appointment.save()

    return redirect('appointment_list')

def disapprove_appointment(request, appointmentId):
    if 'owid' not in request.session:
        return redirect('owner_login')
    owid = request.session['owid']
    owner = Owner.objects.get(owid=owid)

    appointment = Appointment.objects.get(appointmentId=appointmentId)
    appointment.appointmentStatus = 'Disapprove'
    appointment.save()

    return redirect('appointment_list')


def printer_create(request):
    if 'owid' not in request.session:
        return redirect('owner_login')
    owid = request.session['owid']
    owner = Owner.objects.get(owid=owid)

    if request.method == 'POST':
        pname = request.POST['pname']
        pdescription = request.POST['pdescription']

        facility = Printer.objects.create(owner=owner,pname=pname, pdescription=pdescription)
        facility.save()
        return redirect('printer')

    return render(request, 'printer_create.html', {'owner': owner})


def owner_register(request):
    if request.method == 'POST':
        owid = request.POST.get('owid')
        opassword = request.POST.get('opassword')
        owname = request.POST.get('owname')
        owphone = request.POST.get('owphone')

        if owid and opassword and owname and owphone:
            try:
                owner = Owner.objects.create(owid=owid, opassword=opassword, owname=owname, owphone=owphone)
                request.session['owid'] = owner.owid
                return redirect('owner_login')
            except Exception as e:
                error_message = str(e)
                return render(request, 'owner_register.html', {'error_message': error_message})
        else:
            error_message = "Please fill in all the required fields"
            return render(request, 'owner_register.html', {'error_message': error_message})
    return render(request, 'owner_register.html')


def owner_login(request):
    if request.method == 'POST':
        owid = request.POST['owid']
        password = request.POST['password']
        try:
            owner = Owner.objects.get(owid=owid, opassword=password)
            request.session['owid'] = owner.owid
            return redirect('owner_dashboard')
        except Owner.DoesNotExist:
            error_message = "Invalid login credentials"
            return render(request, 'owner_login.html', {'error_message': error_message})
    return render(request, 'owner_login.html')


def owner_logout(request):
    del request.session['owid']
    return redirect('owner_login')