import pyrebase
import re

firebaseConfig = {

  "apiKey": "AIzaSyBI8cLQei5DiNAdNqI4tHKqDEmK2zRTNNY",

  "authDomain": "skill-sync-cli.firebaseapp.com",

  "projectId": "skill-sync-cli",

  "storageBucket": "skill-sync-cli.firebasestorage.app",

  "messagingSenderId": "280182390752",

  "appId": "1:280182390752:web:637d7d746129658fb27585",

  "measurementId": "G-HP8LXVM2ME"}
firebase = pyrebase.initialize_app(firebaseConfig)


def sing_up():
  auth = firebase.auth()
  email = input("please enter your email: ")

  password = input("please enter a password")

  if len(password)>=8 and re.search("[A-Z]", password) and re.search("[a-z]", password) and re.search("[0-9]", password) and re.search("[^A-Za-z0-9]", password):
    return True
    #check if password is at least 8 characters long
  if len(password) < 8:
    return False
    #check if password contains at least one uppercase letter
  if not re.search("[A-Z]", password):
    return False
    #check if password contains at least one lowercase letter
  if not re.search("[a-z]", password):
    return False
    #check if password contains at least one digit
  if not re.search("[0-9]", password):
    return False
    #check if password contains at least one special character
  if not re.search("[^A-Za-z0-9]", password):
    return False
  
  try:
    auth.create_user_with_email_and_password(email, password)
    print("User created successfully")
  except Exception as e:
    print("Error: ", str(e))
  
  
 

def log_in():
  auth = firebase.auth()
  email = input("please enter your email: ")
  password = input("please enter your password: ")
  try:
    auth.sign_in_with_email_and_password(email, password)
  except Exception as e:
    print("Error: ", str(e))
