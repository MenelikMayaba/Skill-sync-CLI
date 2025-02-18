import pyrebase
import re

firebaseConfig = {

  "apiKey": "AIzaSyBI8cLQei5DiNAdNqI4tHKqDEmK2zRTNNY",

  "authDomain": "skill-sync-cli.firebaseapp.com",

  "projectId": "skill-sync-cli",

  "storageBucket": "skill-sync-cli.firebasestorage.app",

  "messagingSenderId": "280182390752",

  "appId": "1:280182390752:web:637d7d746129658fb27585",

  "measurementId": "G-HP8LXVM2ME",
  "databaseURL": ""}
firebase = pyrebase.initialize_app(firebaseConfig)


def sign_up():
  auth = firebase.auth()
  email = input("please enter your email: ")

  password = input("please enter a password: ")

  if len(password) < 8:
    return

  #check if password contains at least one uppercase letter
  if not re.search("[A-Z]", password):
    return

  #check if password contains at least one lowercase letter
  if not re.search("[a-z]", password):
    return

  #check if password contains at least one digit
  if not re.search("[0-9]", password):
    return

  #check if password contains at least one special character
  if not re.search("[^A-Za-z0-9]", password):
    return 
  
  
  
  try:
    auth.create_user_with_email_and_password(email, password)
    print("User created successfully")
  except Exception as e:
    print("Error: ", str(e)) 
 

def log_in():
    auth = firebase.auth()
    email = input("Please enter your email: ")
    password = input("Please enter your password: ")
    
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print("Login successful! Welcome,", email)
    except Exception as e:
        print("Error: Incorrect password or email.", str(e))


if __name__ == "__main__":
    while True:
        choice = input("\n1. Sign Up\n2. Log In\n3. Exit\nChoose an option: ")
        if choice == "1":
            sign_up()
        elif choice == "2":
            log_in()
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid option, please try again.")

