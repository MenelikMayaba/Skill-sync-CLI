from Authentication import *
from peer_mentor import *
from bookings import *
from calender_api import *

@click.group()
def cli():
    
     while True:
          choices = input("\n1. Sign Up\n2. Log In\n 3. forgot password?\n4. View mentor\n5. view peer\n6. view bookings\n7. cancel bookings\n8. Exit\nChoose an option: ")
          choice = int(choices)
          if choice == "1":
               cli.add_command(sign_up)

          if choice == '2':
               cli.add_command(log_in)

          if choice == '3':
               cli.add_command(forgot_password)
          
          if choice == '4':
               cli.add_command(view_mentors)

          if choice == '5':
               cli.add_command(view_peers)
          
          if choice == '6':
               cli.add_command(view_bookins)

          if choice == '7':
               cli.add_command(cancel_booking)

          if choice == '8':
               print('exiting, goodbye')
          
          break
if __name__ == "__main__":
     cli()

