from Authentication import *
from peer_mentor import *
from bookings import *
from calender_api import *

@click.group()
def cli():
    pass

# Register all commands
cli.add_command(sign_up)
cli.add_command(log_in)
cli.add_command(forgot_password)
cli.add_command(view_mentors)
cli.add_command(view_peers)
cli.add_command(view_bookins)
cli.add_command(cancel_booking)

def main():
    while True:
        print("\n1. Sign Up\n2. Log In\n3. Forgot Password\n4. View Mentors\n5. View Peers\n6. View Bookings\n7. Cancel Bookings\n8. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            sign_up()
        elif choice == "2":
            log_in()
        elif choice == "3":
            forgot_password()
        elif choice == "4":
            view_mentors()
        elif choice == "5":
            view_peers()
        elif choice == "6":
            view_bookins()
        elif choice == "7":
            cancel_booking()
        elif choice == "8":
            print("Exiting, goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
