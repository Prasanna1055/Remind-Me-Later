from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from RemindMe.models import REMINDME
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils.timezone import make_aware
from .utils import send_scheduled_email
from .utils import send_sms_via_msg91


@login_required(login_url='/loginn')
def home(request):
    return redirect('/remindpage')

def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('emailid')
        pwd = request.POST.get('pwd')
        my_user = User.objects.create_user(fnm, emailid, pwd)
        my_user.save()
        return redirect('/loginn')
    return render(request, 'signup.html')

def loginn(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        userr = authenticate(request, username=fnm, password=pwd)
        if userr is not None:
            login(request, userr)
            return redirect('remind')
        else:
            return redirect('/loginn')
    return render(request, 'loginn.html')

@login_required(login_url='/loginn')
def remind(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        date = request.POST.get('date') 
        time_ = request.POST.get('time')  
        send_via = request.POST.get('send_via')

        obj = REMINDME.objects.create(
            user=request.user,
            title=title,
            message=message,
            date=date,
            time=time_,
            send_via=send_via
        )

        if send_via == 'email':
            dt = datetime.strptime(f"{date} {time_}", "%Y-%m-%d %H:%M")
            dt = make_aware(dt)

            success = send_scheduled_email(
                to_email=request.user.email,
                subject=title,
                message=message,
                send_datetime=dt
            )
            if not success:
                print("Failed to schedule email.")
        elif send_via == 'sms':
            phone = request.user.username
            try:
                sms_result = send_sms_via_msg91(phone, message)
                print("SMS Result:", sms_result)
            except Exception as e:
                print("SMS sending failed:", e)


        return redirect('remind')

    res = REMINDME.objects.filter(user=request.user)
    return render(request, 'remind.html', {'res': res})

@login_required(login_url='/loginn')
def edit_remind(request, srno):
    obj = REMINDME.objects.get(srno=srno)
    if request.method == 'POST':
        obj.title = request.POST.get('title')
        obj.message = request.POST.get('message')
        obj.date = request.POST.get('date')
        obj.time = request.POST.get('time')
        obj.send_via = request.POST.get('send_via')
        obj.save()
        return redirect('/remindpage')
    return render(request, 'edit_remind.html', {'obj': obj})

@login_required(login_url='/loginn')
def delete_remind(request, srno):
    obj = REMINDME.objects.get(srno=srno)
    obj.delete()
    return redirect('/remindpage')

def signout(request):
    logout(request)
    return redirect('/loginn')


