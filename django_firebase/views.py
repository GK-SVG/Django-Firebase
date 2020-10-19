from django.shortcuts import render, HttpResponse, redirect
import pyrebase

#--------------------------------------Firebase Configuration-------------------------------------     
firebaseConfig = {
    'apiKey': "Your Key",
    'authDomain': "------",
    'databaseURL': "--------",
    'projectId': "-----",
    'storageBucket': "-------",
    'messagingSenderId': "---",
    'appId': "---",
    'measurementId': "----"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
database = firebase.database()


def authenticate(request):
    if request.method == "POST":
        email = request.POST['email']
        passw = request.POST['password']
        try:
            user = auth.sign_in_with_email_and_password(email, passw)
            print('user==', user)
            return render(request, 'welcome.html', {'email': email})
        except:
            msg = 'Invalid credencials'
            return render(request, 'signin.html', {'msg': msg})


def signin(request):
    return render(request, 'signin.html')


def signup(request):
    if request.method=='POST':
      name=request.POST['name']
      email=request.POST['email']
      passw=request.POST['password']
      try:
        user=auth.create_user_with_email_and_password(email,passw)
        uid = user['localId']
      except:
        msg = 'Unable to create account'
        return render(request, 'signup.html',{'msg':msg})
      data={'name':name,'status':"1"}
      database.child("users").child(uid).child('details').child(data)
      return render(request, 'signin.html')
    return render(request, 'signup.html')
