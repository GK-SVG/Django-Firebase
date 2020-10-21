from django.shortcuts import render, HttpResponse, redirect
import pyrebase
from django.contrib import auth
from datetime import datetime
#--------------------------------------Firebase Configuration-------------------------------------     
firebaseConfig = {
    'apiKey': "AIzaSyDWLEJLHfKX-z37aW1l8B1M5AMuVyNwrRU",
    'authDomain': "high-life-281103.firebaseapp.com",
    'databaseURL': "https://high-life-281103.firebaseio.com",
    'projectId': "high-life-281103",
    'storageBucket': "high-life-281103.appspot.com",
    'messagingSenderId': "322595235555",
    'appId': "1:322595235555:web:7c78701c27ebbf14cb07d6",
    'measurementId': "G-SHHW9MZKGW"
}

firebase = pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()
database = firebase.database()


#---------------------------authenticating user---------------------------------------------
def authenticate(request):
    if request.method == "POST":
        email = request.POST['email']
        passw = request.POST['password']
        try:
            user = authe.sign_in_with_email_and_password(email, passw)
            print('user==', user)
            request.session['uid']=str(user['idToken'])
            return render(request, 'welcome.html', {'email': email})
        except:
            msg = 'Invalid credencials'
            return render(request, 'signin.html', {'msg': msg})


def signin(request):
    return render(request, 'signin.html')


#------------------------------------Sign-Up user and sending user data into firebase------------------
def signup(request):
    if request.method=='POST':
      name=request.POST['name']
      email=request.POST['email']
      passw=request.POST['password']
      try:
        user=authe.create_user_with_email_and_password(email,passw)
        #print(user)
        uid = user['localId']
      except:
        msg = 'Unable to create account'
        return render(request, 'signup.html',{'msg':msg})
      data={'name':name,'status':"1"}
      database.child("users").child(uid).child('details').push(data)
      return render(request, 'signin.html')
    return render(request, 'signup.html')


def logout(request):
  del request.session['uid']
  return render(request, 'signin.html')


#--------------------------------------creating form and json data into firebase DB--------------------
def create_report(request):
  import time
  from datetime import datetime,timezone
  import pytz
  if request.method=='POST':
    title=request.POST['title']
    text=request.POST['text']
    time_zone = pytz.timezone('Asia/Kolkata')
    time_now= datetime.now(timezone.utc).astimezone(time_zone)
    milli_sec=int(time.mktime(time_now.timetuple()))
    try:
      id_token= request.session['uid']
      user_is=authe.get_account_info(id_token)
      print('user=====',user_is)
      data={
        'title':title,
        'text':text,
        }
      print('localId===',user_is['users'][0]['localId'])
      uid=user_is['users'][0]['localId']
      email=user_is['users'][0]['email']
      database.child('users').child(uid).child('reports').child(milli_sec).set(data)
      return render(request,'welcome.html',{'email':email})
    except KeyError:
      msg= 'Please SignIn first'
      return render(request, 'signin.html',{'msg':msg})
  return render(request,'create_report.html')



#----------------------------------Retrieving json data from firebase DB--------------------------
def retriew_report(request):
  import datetime
  id_token= request.session['uid']
  user_is=authe.get_account_info(id_token)
  uid=user_is['users'][0]['localId']
  all_timestamp=database.child('users').child(uid).child('reports').shallow().get().val()
  print(all_timestamp)
  time_list=[]
  for time in all_timestamp:
    time_list.append(time)
  time_list.sort(reverse=True)
  print(time_list)
  title = []
  text = []
  for time in time_list:
    tit=database.child('users').child(uid).child('reports').child(time).child('title').get().val()
    title.append(tit)
    tex=database.child('users').child(uid).child('reports').child(time).child('text').get().val()
    text.append(tex)
  print('title==',title)
  print('text==',text)
  date=[]
  for i in time_list:
    dat= datetime.datetime.fromtimestamp(float(i)).strftime('%H:%M %d-%m-%Y')
    date.append(dat)
  combined_data=zip(date,title,text)
  return render(request,'retriew.html',{'combined_data':combined_data})

      