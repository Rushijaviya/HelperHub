from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import (
    userForm,
    userInfoForm,
    doctorForm,
    tutorForm,
    service_providerForm,
    logisticForm,
    otherForm,
    userInfoUpdateForm,
)
from .models import userInfo, Doctor, Tutor, Logistic, Service_Provider, Other
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse, HttpResponse
from .models import Message
from .serializers import MessageSerializer, UserSerializer



account_sid = "twilio_account_sid"
auth_token = "twilio_account_auth_token"


def error(request):
    return render(request, "error.html")


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == "GET":
        
        messages = Message.objects.filter(
            sender_id=sender, receiver_id=receiver, is_read=False
        )
        serializer = MessageSerializer(
            messages, many=True, context={"request": request}
        )
        for message in messages:
            
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    # elif request.method == "post":
    else:
        
        data = JSONParser().parse(request)
        
        serializer = MessageSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
        
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)




def message_view(request, sender, receiver):
    

    if not request.user.is_authenticated:
        return redirect("index")

    # if request.method == "GET":
    return render(
        request,
        "chat/messages.html",
        {
            "users": User.objects.exclude(username=request.user.username),
            "receiver": User.objects.get(id=receiver),
            "messages": Message.objects.filter(sender_id=sender, receiver_id=receiver)
            | Message.objects.filter(sender_id=receiver, receiver_id=sender),
        }
    )


def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'chat/chat.html',
                      {'users': User.objects.exclude(username=request.user.username)})


def recivedMessages(request):
    

    if not request.user.is_authenticated:
        return redirect("index")
    if request.method == "GET":
        user = User.objects.exclude(username=request.user.username)
        Msg = Message.objects.all()
        
        return render(
            request,
            "chat/chat.html",
            {
                "users": user,
            },
        )


def index(request):
    return render(request, "index.html")


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


# def loginnew(request):
#     return render(request, 'login.html')


@login_required(login_url="error")
def menu(request):
    users = User.objects.all()
    all_doctors = userInfo.objects.filter(occupation="Doctor")

    doctors = []
    doctorsinfo = []
    u1 = []

    for i in all_doctors:
        try:
            obj = Doctor.objects.get(doctor=i.user)
            doctorsinfo.append(obj)
            doctors.append(i)
            u1.append(User.objects.get(username=i.user))
        except:
            pass

    fin_ans1 = zip(doctors, doctorsinfo, u1)
    fin_ans1 = list(fin_ans1)

    all_tutors = userInfo.objects.filter(occupation="Tutor")

    tutors = []
    tutorsinfo = []
    u2 = []

    for i in all_tutors:
        try:
            obj = Tutor.objects.get(tutor=i.user)
            tutorsinfo.append(obj)
            tutors.append(i)
            u2.append(User.objects.get(username=i.user))

        except:
            pass

    fin_ans2 = zip(tutors, tutorsinfo, u2)
    fin_ans2 = list(fin_ans2)

    all_service_providers = userInfo.objects.filter(occupation="Doctor")

    service_providers = []
    service_providersinfo = []
    u3 = []

    for i in all_service_providers:
        try:
            obj = Service_Provider.objects.get(service_provider=i.user)
            service_providersinfo.append(obj)
            service_providers.append(i)
            u3.append(User.objects.get(username=i.user))

        except:
            pass

    fin_ans3 = zip(service_providers, service_providersinfo, u3)
    fin_ans3 = list(fin_ans3)

    all_logistics = userInfo.objects.filter(occupation="Logistic")

    logistics = []
    logisticsinfo = []
    u4 = []

    for i in all_logistics:
        try:
            obj = Logistic.objects.get(logistic=i.user)
            logisticsinfo.append(obj)
            logistics.append(i)
            u4.append(User.objects.get(username=i.user))

        except:
            pass

    fin_ans4 = zip(logistics, logisticsinfo, u4)
    fin_ans4 = list(fin_ans4)

    all_others = userInfo.objects.filter(occupation="Other")

    others = []
    othersinfo = []
    u5 = []

    for i in all_others:
        try:
            obj = Other.objects.get(other=i.user)
            othersinfo.append(obj)
            others.append(i)
            u5.append(User.objects.get(username=i.user))

        except:
            pass

    fin_ans5 = zip(others, othersinfo, u5)
    fin_ans5 = list(fin_ans5)

    context = {
        "fin_ans1": fin_ans1,
        "fin_ans2": fin_ans2,
        "fin_ans3": fin_ans3,
        "fin_ans4": fin_ans4,
        "fin_ans5": fin_ans5,
    }

    return render(request, "menu.html", context)


def contact(request):
    return render(request, "contact.html")


def chat_masala(request):
    return render(request, "chat/index.html")


def lul(request):
    return render(request, "chat/index.html")


def signup_doctor(request):
    return render(request, "forms/doc_form.html")


def signup_tutor(request):
    return render(request, "forms/tutor_form.html")


def signup_logistic(request):
    return render(request, "forms/logistic_form.html")


def signup_serive_provider(request):
    return render(request, "forms/service_provider_new_form.html")


def signup_other(request):
    return render(request, "forms/other_form.html")


def signup(request):

    if request.method == "POST":
        user_form = userForm(request.POST)
        user_info_form = userInfoForm(request.POST, request.FILES)

        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_info = user_info_form.save(commit=False)
            user_info.user = user
            user_info.save()

            login(request, user)

            return redirect("index")

        else:
            
            context = {
                "user_form.errors": user_form.errors,
                "user_info_form.errors": user_info_form.errors,
                "user_form": user_form,
                "user_info_form": user_info_form,
            }
            return render(request, "user/login.html", context)

    else:
        user_form = userForm()
        user_info_form = userInfoForm()

        context = {"user_form": user_form, "user_info_form": user_info_form}
        return render(request, "user/login.html", context)


def signin(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)

            # user = request.user
            # user = userInfo.objects.get(user=user)

            # mobile_number = user.mobile_number

            # client = Client(account_sid, auth_token)
            # message = client.messages.create(
            #     body='Hello {}, you are successfully loggedin to Musicbuzz.'.format(
            #         username),
            #     from_='+14582365794',
            #     to='+91{}'.format(mobile_number)
            # )

            return redirect("index")
        else:
            return redirect("signin")

    else:
        return render(request, "user/login.html")


@login_required(login_url="error")
def update(request):

    user = request.user
    user = userInfo.objects.get(user=user)

    pk = user.id

    Object = userInfo.objects.get(id=pk)
    form = userInfoForm(instance=Object)

    if request.method == "POST":
        form_data = userInfoForm(request.POST, instance=Object)

        if form_data.is_valid():
            form_data.save()
            return redirect("index")

        

    context = {"form": form, "flag": False}
    return render(request, "user/update.html", context)


@login_required(login_url="error")
def signout(request):
    logout(request)
    return redirect("index")


@login_required(login_url="error")
def doctorFormView(request):

    users = User.objects.all()
    doctor_form = doctorForm()

    if request.method == "POST":
        doctor_form = doctorForm(request.POST)

        if doctor_form.is_valid():
            doctor_form.save()

            return redirect("index")

        else:
            errors = doctor_form.errors

            

            context = {"doctor_form": doctor_form, "errors": errors, "users": users}

            return render(request, "forms/doctorForm.html", context)

    context = {"doctor_form": doctor_form, "users": users}

    return render(request, "forms/doctorForm.html", context)


@login_required(login_url="error")
def doctor_update(request):

    user = request.user

    user = Doctor.objects.get(doctor=user)

    pk = user.id

    Object = Doctor.objects.get(id=pk)
    form = doctorForm(instance=Object)
    users = User.objects.all()

    if request.method == "POST":
        form_data = doctorForm(request.POST, instance=Object)

        if form_data.is_valid():
            form_data.save()
            return redirect("index")

        

    context = {"form": form, "flag": False, "users": users}
    return render(request, "forms/doctorUpdateForm.html", context)


@login_required(login_url="error")
def tutorFormView(request):
    users = User.objects.all()
    tutor_form = tutorForm()

    if request.method == "POST":
        tutor_form = tutorForm(request.POST)

        if tutor_form.is_valid():
            tutor_form.save()

            return redirect("index")

        else:
            errors = tutor_form.errors

            context = {"tutor_form": tutor_form, "errors": errors, "users": users}

            return render(request, "forms/tutorForm.html", context)

    context = {"tutor_form": tutor_form, "users": users}

    return render(request, "forms/tutorForm.html", context)


@login_required(login_url="error")
def tutor_update(request):

    user = request.user
    user = Tutor.objects.get(tutor=user)

    users = User.objects.all()

    pk = user.id

    Object = Tutor.objects.get(id=pk)
    form = tutorForm(instance=Object)

    if request.method == "POST":
        form_data = tutorForm(request.POST, instance=Object)

        if form_data.is_valid():
            form_data.save()
            return redirect("index")


    context = {"form": form, "flag": False, "users": users}
    return render(request, "forms/tutorUpdateForm.html", context)


@login_required(login_url="error")
def service_providerFormView(request):
    users = User.objects.all()

    service_provider_form = service_providerForm()

    if request.method == "POST":
        service_provider_form = service_providerForm(request.POST)

        if service_provider_form.is_valid():
            service_provider_form.save()

            return redirect("index")

        else:
            errors = service_provider_form.errors

            context = {
                "service_provider_form": service_provider_form,
                "errors": errors,
                "users": users,
            }

            return render(request, "forms/service_providerForm.html", context)

    context = {"service_provider_form": service_provider_form, "users": users}

    return render(request, "forms/service_providerForm.html", context)


@login_required(login_url="error")
def service_provide_update(request):

    user = request.user
    user = Service_Provider.objects.get(service_provider=user)

    users = User.objects.all()

    pk = user.id

    Object = Service_Provider.objects.get(id=pk)
    form = service_providerForm(instance=Object)

    if request.method == "POST":
        form_data = service_providerForm(request.POST, instance=Object)

        if form_data.is_valid():
            form_data.save()
            return redirect("index")


    context = {"form": form, "flag": False, "users": users}
    return render(request, "forms/service_providerUpdateForm.html", context)


@login_required(login_url="error")
def logisticFormView(request):
    users = User.objects.all()
    logistic_form = logisticForm()

    if request.method == "POST":
        logistic_form = logisticForm(request.POST)

        if logistic_form.is_valid():
            logistic_form.save()

            return redirect("index")

        else:
            errors = logistic_form.errors

            context = {"logistic_form": logistic_form, "errors": errors, "users": users}

            return render(request, "forms/logisticForm.html", context)

    context = {"logistic_form": logistic_form, "users": users}

    return render(request, "forms/logisticForm.html", context)


@login_required(login_url="error")
def logistic_update(request):

    user = request.user
    user = Logistic.objects.get(logistic=user)

    users = User.objects.all()

    pk = user.id

    Object = Logistic.objects.get(id=pk)
    form = logisticForm(instance=Object)

    if request.method == "POST":
        form_data = logisticForm(request.POST, instance=Object)

        if form_data.is_valid():
            form_data.save()
            return redirect("index")


    context = {"form": form, "flag": False, "users": users}
    return render(request, "forms/logisticUpdateForm.html", context)


@login_required(login_url="error")
def otherFormView(request):
    users = User.objects.all()

    other_form = otherForm()

    if request.method == "POST":
        other_form = otherForm(request.POST)

        if other_form.is_valid():
            other_form.save()

            return redirect("index")

        else:
            errors = other_form.errors

            context = {"other_form": other_form, "errors": errors, "users": users}

            return render(request, "forms/logisticForm.html", context)

    context = {"other_form": other_form, "users": users}

    return render(request, "forms/otherForm.html", context)


@login_required(login_url="error")
def other_update(request):

    user = request.user
    user = Other.objects.get(other=user)

    users = User.objects.all()

    pk = user.id

    Object = Other.objects.get(id=pk)
    form = otherForm(instance=Object)

    if request.method == "POST":
        form_data = otherForm(request.POST, instance=Object)

        if form_data.is_valid():
            form_data.save()
            return redirect("index")

    context = {"form": form, "flag": False, "users": users}
    return render(request, "forms/otherUpdateForm.html", context)


@login_required(login_url="error")
def verify(request):

    user = request.user
    user = userInfo.objects.get(user=user)

    mobile_number = user.mobile_number

    if request.method == "POST":
        call = request.POST.get("call")
        sms = request.POST.get("sms")
        client = Client(account_sid, auth_token)

        if call:
            verification = client.verify.services(
                "Twilio_service_number"
            ).verifications.create(to="+91 {}".format(mobile_number), channel="call")

        else:
            verification = client.verify.services(
                "Twilio_service_number"
            ).verifications.create(to="+91 {}".format(mobile_number), channel="sms")

        return redirect("check_otp")
    context = {"mobile_number": mobile_number[8:]}

    return render(request, "otp/verify.html", context)


@login_required(login_url="error")
def check_otp(request):

    user = request.user
    user = userInfo.objects.get(user=user)

    mobile_number = user.mobile_number

    if request.method == "POST":
        otp = request.POST.get("otp")
        client = Client(account_sid, auth_token)

        verification_check = client.verify.services(
            "Twilio_service_number"
        ).verification_checks.create(to="+91 {}".format(mobile_number), code=otp)

        if verification_check.status == "approved":
            user.verified = True
            user.save()
            return render(request, "otp/success.html")

    return render(request, "otp/check_otp.html")


@login_required(login_url="error")
def create_profile(request):

    user = request.user
    user = userInfo.objects.get(user=user)

    occ = user.occupation

    chk = user.verified
    context = {"chk": chk}

    if chk:

        if occ == "Doctor":
            try:
                Doctor.objects.get(doctor=request.user)
                return redirect(doctor_update)
            except:
                return redirect(doctorFormView)

        elif occ == "Tutor":
            try:
                Tutor.objects.get(tutor=request.user)
                return redirect(tutor_update)
            except:
                return redirect(tutorFormView)

        elif occ == "Service Provider":
            try:
                Service_Provider.objects.get(service_provider=request.user)
                return redirect(service_provider_update)
            except:
                return redirect(service_providerFormView)

        elif occ == "Logistic":
            try:
                Logistic.objects.get(logistic=request.user)
                return redirect(logistic_update)
            except:
                return redirect(logisticFormView)

        elif occ == "Other":
            try:
                Other.objects.get(other=request.user)
                return redirect(other_update)
            except:
                return redirect(otherFormView)

    return render(request, "user/createProfile.html", context)


@login_required(login_url="error")
def find_doctor(request, pk):

    doctor = Doctor.objects.get(id=pk)

    username = userInfo.objects.get(user=doctor.doctor)

    doctors = []
    doctorsinfo = []

    doctorsinfo.append(doctor)
    doctors.append(username)

    fin_ans = zip(doctors, doctorsinfo)
    fin_ans = list(fin_ans)

    context = {"fin_ans": fin_ans}

    return render(request, "details/doctorDetails.html", context)


@login_required(login_url="error")
def find_tutor(request, pk):

    tutor = Tutor.objects.get(id=pk)
    username = userInfo.objects.get(user=tutor.tutor)

    tutors = []
    tutorsinfo = []

    tutorsinfo.append(tutor)
    tutors.append(username)

    fin_ans = zip(tutors, tutorsinfo)
    fin_ans = list(fin_ans)

    context = {"fin_ans": fin_ans}

    return render(request, "details/tutorDetails.html", context)


@login_required(login_url="error")
def find_service_provider(request, pk):

    service_provider = Service_Provider.objects.get(id=pk)
    username = userInfo.objects.get(user=service_provider.service_provider)

    service_providers = []
    service_providersinfo = []

    service_providersinfo.append(service_provider)
    service_providers.append(username)

    fin_ans = zip(service_providers, service_providersinfo)
    fin_ans = list(fin_ans)

    context = {"fin_ans": fin_ans}

    return render(request, "details/service_providerDetails.html", context)


@login_required(login_url="error")
def find_logistic(request, pk):

    logistic = Logistic.objects.get(id=pk)
    username = userInfo.objects.get(user=logistic.logistic)

    logistics = []
    logisticsinfo = []

    logisticsinfo.append(logistic)
    logistics.append(username)

    fin_ans = zip(logistics, logisticsinfo)
    fin_ans = list(fin_ans)

    context = {"fin_ans": fin_ans}

    return render(request, "details/logisticDetails.html", context)


@login_required(login_url="error")
def find_other(request):

    all_others = userInfo.objects.filter(occupation="Other")

    others = []
    othersinfo = []

    for i in all_others:
        try:
            obj = Other.objects.get(other=i.user)
            othersinfo.append(obj)
            others.append(i)
        except:
            pass

    fin_ans = zip(others, othersinfo)
    fin_ans = list(fin_ans)

    context = {"fin_ans": fin_ans}

    return render(request, "details/otherDetails.html", context)
