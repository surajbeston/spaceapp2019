from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from network.forms import add_userinfo_form
from network.models import add_userinfo
from django.template.context_processors import csrf
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from twilio.rest import Client

@login_required
def home(request):
    user = request.user
    user_infom = add_userinfo.objects.get(user = user)
    print (user_infom.long)
    return render(request, 'network/home.html', {'username': user.username, 'user_info': user_infom})

def basic_info(request):

    return render(request, 'network/base.html', {'username': request.session['username']})


def signup(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        if request.method == 'POST':
            print (request.POST)
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                request.session['username'] = username
                request.session['password'] = raw_password

                return redirect('/add-info/')
            else:
                return HttpResponse(form.errors)
        else:
            form = UserCreationForm()
            dict = {'form': form}
            dict.update(csrf(request))
            return render(request, 'registration/signup.html', dict)


def add_info(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        if request.method == 'POST':
            form = add_userinfo_form(request.POST)
            if form.is_valid():
                a = form.save(commit = False)
                user = authenticate(username=request.session['username'], password=request.session['password'])
                a.user = user
                a.save()
                login(request, user)
                return redirect('/home/')
            else:
                return HttpResponse('Form not valid.')
        else:
            form = add_userinfo_form()
            dict = {'form': form, 'username': request.session['username']}
            dict.update(csrf(request))
            return render(request, 'registration/add-info.html', dict)

@login_required
def inform_neighbour(request):
    user = request.user
    username= add_userinfo.objects.get(user = user)
    send_sms('A house in' + username.local_address + ' Latitude: ' + str(username.lat) + ' Longitude: ' + str(username.long) + ' maybe in fire. ' + 'Location Link: http://www.google.com/maps/place/' + str(username.long) + ',' + str(username.lat) , '+9779819604815')
    return HttpResponse('Message sent.')


@csrf_exempt
def get_data(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        our_user = User.objects.get(username = body['username'])
        username = add_userinfo.objects.get(user = our_user)
        ppm = float(body['ppm'])
        print(ppm)
        if ppm > 5:
            send_sms('Your house in '+ username.local_address + ' Latitude: ' + str(username.lat) + ' Longitude: ' + str(username.long) + ' maybe in fire. ' + str(ppm) + ' is the smoke ppm value.' + 'Location Link: http://www.google.com/maps/place/' + str(username.long) + ',' + str(username.lat) , '+9779819604815')
            send_sms('Your neighbour, ' +  body['username'] + ' house in '+ username.local_address + ' Latitude: ' + str(username.lat) + ' Longitude: ' + str(username.long) + ' maybe in fire. ' + str(ppm) + ' is the smoke ppm value.' + 'Location Link: http://www.google.com/maps/place/' + str(username.long) + ',' + str(username.lat), '+9779863397356' )
            send_sms('A house in' + username.local_address + ' Latitude: ' + str(username.lat) + ' Longitude: ' + str(username.long) + ' maybe in fire. ' + str(ppm) + ' is the smoke ppm value.' + 'Location Link: http://www.google.com/maps/place/' + str(username.long) + ',' + str(username.lat) , '+9779819604815')
        if ppm > 10:
            send_sms('Your friend '+ body['username'] + ' is in life threatning risk. '+ str(ppm) + ' is the smoke ppm value.' + 'Location Link: http://www.google.com/maps/place/' + str(username.long) + ',' + str(username.lat) , '+9779819604815')
    else:
        print('GET request received.')
    return HttpResponse('GOtit.')

def water_map(request):
    return render(request, 'network/maps.html', {})

def send_sms(data, mobile):
    account_sid = 'AC8fcfcee9be89ccf25ba5f6a41b076983'
    auth_token = '3ab2f155d81921cabb035470ed424de9'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=data,
                         from_='+17126315392',
                         to= mobile
                     )
    print(message.sid)


def firefighter_console(request):
    return render(request, 'network/console.html', {})
