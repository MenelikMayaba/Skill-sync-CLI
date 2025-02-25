from Authentication import sign_up, log_in, forgot_password
from peer_mentor import view_mentors, view_peers
from bookings import request_meeting, view_bookings, cancel_booking
import click

@click.group()
def cli():
    pass

cli.add_command(sign_up)
cli.add_command(log_in)
cli.add_command(forgot_password)
cli.add_command(request_meeting)
cli.add_command(view_bookings)
cli.add_command(cancel_booking)

def main():
    """This is the main entry point of the program.
    It contains an infinite loop that keeps showing the main menu to the user
    until the user chooses to exit.
    """
    current_user = None  # Initialize current_user to None
    
    while True:
        """Print the main menu options to the user.
        The options are:
        1. Sign Up
        2. Log In
        3. Forgot Password
        4. View Mentors
        5. View Peers
        6. View Bookings
        7. Cancel Bookings
        8. Request meeting
        9. Exit
        """
        print("\n1. Sign Up\n2. Log In\n3. Forgot Password\n4. View Mentors\n5. View Peers\n6. View Bookings\n7. Cancel Bookings\n8. Request meeting\n9. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            sign_up.main(standalone_mode=False)
        elif choice == "2":
            current_user = log_in.main(standalone_mode=False)
        elif choice == "3":            
            forgot_password.main(standalone_mode=False)
        elif choice == "4":
            if current_user:
                view_mentors(current_user)
            else:
                print("You need to log in first.")
        elif choice == "5":
            if current_user:
                view_peers(current_user)
            else:
                print("You need to log in first.")
        elif choice == "6":
            if current_user:
                view_bookings(current_user=current_user, standalone_mode=False)
            else:
                print("You need to log in first.")
        elif choice == "7":
            if current_user:
                meeting_id = input("Enter meeting ID to cancel: ")
                cancel_booking.main(meeting_id=meeting_id)
            else:
                print("You need to log in first.")
        elif choice == "8":
            if current_user:
                mentor_id = input("Enter mentor ID: ")
                time = input("Enter meeting time (YYYY-MM-DD HH:MM): ")
                request_meeting(mentor_id=mentor_id, time=time, current_user=current_user)
            else:
                print("You need to log in first.")
        elif choice == "9":
            print("Exiting, goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()