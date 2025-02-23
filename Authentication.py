import pyrebase
import re
import click

firebaseConfig = {

  "apiKey": "AIzaSyBI8cLQei5DiNAdNqI4tHKqDEmK2zRTNNY",

  "authDomain": "skill-sync-cli.firebaseapp.com",

  "projectId": "skill-sync-cli",

  "databaseURL": "https://skill-sync-cli-default-rtdb.firebaseio.com/",
  
  "storageBucket": "skill-sync-cli.firebasestorage.app",

  "messagingSenderId": "280182390752",

  "appId": "1:280182390752:web:637d7d746129658fb27585",

  "measurementId": "G-HP8LXVM2ME"}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

current_user= 0

@click.command()
@click.option('--email', prompt='Email', help='Email to use for signup')
@click.option('--password', prompt= True, hide_input = True, confirmation_prompt = True, help='Password to use for signup')
@click.option('--name', prompt='full name', help='Name to use for signup')
@click.option('--role', type=click.Choice(['peer', 'mentor']), prompt ='role', help='Role to use for signup')
@click.option("--expertise", prompt="Expertise (if mentor)", default="", help="Enter expertise (optional for peers)")
def sign_up(name, email, password, role, expertise):

  if role not in ["mentor", "peer"]:
        print("Invalid role. Please enter 'mentor' or 'peer'.")
        return
  
  #validating password
  if len(password) < 8:
    print("password must be at least 8 characters long")
    return
  #check if password contains at least one uppercase letter
  if not re.search("[A-Z]", password):
    print("password must contain  uppercase letter")
    return
  #check if password contains at least one lowercase letter
  if not re.search("[a-z]", password):
    print("password must contain  lowercase letter")
    return
  #check if password contains at least one digit
  if not re.search("[0-9]", password):
    print("password must contain  digit")
    return
  #check if password contains at least one special character
  if not re.search("[^A-Za-z0-9]", password):
    print("password must contain  special character")
    return 
  
  try:
    user = auth.create_user_with_email_and_password(email, password)
  
    uid = user["localId"]
    user_data = {"name": name,
                "role": role,
                "email": email,
                "expertise": expertise}
    
    db.child("users").child(uid).set(user_data, user["idToken"])

    click.echo("User created successfully")
  except Exception as e:
    click.echo(f"Error: {str(e)}") 

 
@click.command()
@click.option('--username', prompt='email', help='enter your email')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='enter your password')
def log_in():
    global current_user
    auth = firebase.auth()
    email = input("Please enter your email: ")
    password = input("Please enter your password: ")
    
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        current_user = user
        click.echo("Login successful! Welcome,", email)
    except Exception as e:
        click.echo(f"Error: Incorrect password or email: {str(e)}")


@click.command()
@click.option('--email', prompt='enter your email', help='email to reset your passwrod')
def forgot_password():
  auth = firebase.auth()
  email = input("Please enter your email: ")
  try:
    auth.send_password_reset_email(f"email:{email}")
    click.echo("Password reset email sent to your email")
  except Exception as e:
      click.echo(f"Error: {str(e)}")

    

