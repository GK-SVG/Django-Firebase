from django.shortcuts import render, HttpResponse, redirect
import pyrebase

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
# Initialize Firebase
# firebase.initializeApp(firebaseConfig)
# firebase.analytics()

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
database= firebase.database()

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
      user=auth.create_user_with_email_and_password(email,passw)
      uid = user['localId']
      data={'name':name,'status':"1"}
      database.child("users").child(uid).child('details').child(data)
      return render(request, 'signin.html')
    return render(request, 'signup.html')
