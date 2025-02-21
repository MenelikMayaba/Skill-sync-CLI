from Authentication import *
from peer_mentor import *
from bookings import *

@click.group()
def cli():
    
    while True:
         choices = input("\n1. Sign Up\n2. Log In\n 3. forgot password?\n4. View mentor\n5. view peer\n6. view bookings\n7. cancel bookings\n8. Exit\nChoose an option: ")
         choice = int(choices)
         if choice == "1":
    
    #cli.add_command(sign_up)