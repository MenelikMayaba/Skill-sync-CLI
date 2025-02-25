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
  "measurementId": "G-HP8LXVM2ME"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

# Define a function for user signup with various input options
@click.command()
@click.option('--email', prompt='Email', help='Email to use for signup')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Password to use for signup')
@click.option('--name', prompt='full name', help='Name to use for signup')
@click.option('--role', type=click.Choice(['peer', 'mentor']), prompt='role', help='Role to use for signup')
@click.option("--expertise", prompt="Expertise (if mentor)", default="", help="Enter expertise (optional for peers)")
def sign_up(name, email, password, role, expertise):
    # Check if the role is valid
    if role not in ["mentor", "peer"]:
        print("Invalid role. Please enter 'mentor' or 'peer'.")
        return
  
    # Password validation criteria
    if len(password) < 8:
        print("Password must be at least 8 characters long")
        return
    if not re.search("[A-Z]", password):
        print("Password must contain uppercase letter")
        return
    if not re.search("[a-z]", password):
        print("Password must contain lowercase letter")
        return
    if not re.search("[0-9]", password):
        print("Password must contain digit")
        return
    if not re.search("[^A-Za-z0-9]", password):
        print("Password must contain special character")
        return 
  
    try:
        # Create user with provided email and password
        user = auth.create_user_with_email_and_password(email, password)
        
        # Extract the user ID from the response
        uid = user["localId"]
        
        # Prepare user data with name, role, email, and expertise
        user_data = {"name": name, "role": role, "email": email, "expertise": expertise}
        
        # Set the user data in the database under the user's ID
        db.child("users").child(uid).set(user_data, user["idToken"])
        
        # Display success message if user creation is successful
        click.echo("User created successfully")
    except Exception as e:
        # Handle any errors that occur during user creation
        click.echo(f"Error: str{e}") 

@click.command()
@click.option('--username', prompt='email', help='enter your email')
@click.option('--password', prompt=True, hide_input=True, help='enter your password')
def log_in(username, password):
    """
    This function is used to log in to the application.
    
    Parameters:
    username (string): The email address of the user
    password (string): The password of the user
    
    Returns:
    user (object): The user object if the login is successful, otherwise None
    """
    
    # Initialize the authentication module
    auth = firebase.auth()
    
    try:
        # Attempt to sign in with the provided email and password
        user = auth.sign_in_with_email_and_password(username, password)  
        click.echo(f"Login successful! Welcome, {username}")       
        # Return the user object
        return user
    except Exception as e:
        click.echo(f"Error: Incorrect password or email: {str(e)}")
        return None

@click.command()
@click.option('--email', prompt='enter your email', help='email to reset your passwrod')
def forgot_password(email):
    """
    This function will be used to reset a user's password.
    
    Parameters:
    email (string): The email address of the user
    
    Returns:
    None
    """
    auth = firebase.auth()
    
    # Get the email address from the user
    email = input("Please enter your email: ")
    
    try:
        auth.send_password_reset_email(f"email:{email}")
        click.echo("Password reset email sent to your email")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
