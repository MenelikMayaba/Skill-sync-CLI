from Authentication import *
from peer_mentor import *
from calender_api import authenticate_google_calendar, create_event
import click

@click.command()
@click.option("--mentor-id", prompt="Mentor ID", help="Enter the Mentor's ID")
@click.option("--time", prompt="Meeting Time (YYYY-MM-DD HH:MM)", help="Enter the desired meeting time")
@click.option('--current-user', required=True, help='Current logged-in user')
def request_meeting(mentor_id, time, current_user):
    if not current_user:
        click.echo("You need to log in first.")
        return
    
    mentee_id = current_user['localId']
    meeting_data = {'mentor_id': mentor_id, 'mentee_id': mentee_id, 'time': time, 'status': 'pending'}
    db.child('meetings').push(meeting_data)
    
    try:
        service = authenticate_google_calendar()
        
   
        year, month_day, hour_minute = time.split(' ')
        year, month, day = year.split('-')
        hour, minute = hour_minute.split(':')

        year = int(year)
        month = int(month)
        day = int(day)
        hour = int(hour)
        minute = int(minute)

        #Create start time in the format Google Calendar expects
        start_time = f"{year}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:00"

        #Create end time (1 hour later)
        end_hour = hour + 1
        # Handle hour rollover if needed
        if end_hour >= 24:
            end_hour = end_hour - 24

        #Create end time string
        end_time = f"{year}-{month:02d}-{day:02d}T{end_hour:02d}:{minute:02d}:00"
        
        timezone = "RSA/cape_town"
        
        attendees = [{'email': current_user['email']}]
        event_link = create_event(service, start_time, end_time, timezone, attendees)
        click.echo(f"Meeting Request Sent. Google Calendar event created: {event_link}")
    except Exception as e:
        click.echo(f"Meeting Request Sent, but calendar creation failed: {str(e)}")

@click.command()
@click.option('--current-user', required=True, help='Current logged-in user')
def view_bookings(current_user):
    """
Command-line interface command to view bookings for the current user.

This command retrieves and displays all bookings associated with the
currently logged-in user from the Firebase database. It requires the
user to be logged in and provides details such as meeting ID, mentor ID,
time, and status for each booking. If an error occurs during retrieval,
an error message is displayed.

Parameters:
    current_user (dict): The current logged-in user's information, 
    including their unique local ID.

Raises:
    Exception: If there is an error retrieving bookings from the database.
"""
    if not current_user:
        click.echo("You need to log in first.")
        return
    
    try:
        bookings = db.child('meetings').order_by_child('mentee_id').equal_to(current_user['localId']).get()
        click.echo('\nYour bookings: ')
        for booking in bookings.each():
            click.echo(f"- Meeting ID: {booking.key()}, Mentor ID: {booking.val()['mentor_id']}, Time: {booking.val()['time']}, Status: {booking.val()['status']}")
    except Exception as e:
        click.echo(f"Error viewing bookings: {str(e)}")

@click.command()
@click.option("--meeting-id", prompt="Meeting ID", help="Enter the Meeting ID to cancel")
@click.option('--current-user', required=True, help='Current logged-in user')
def cancel_booking(meeting_id, current_user):
    """
Cancels a booking for a meeting.

This command-line function allows a user to cancel a meeting by providing
the meeting ID. It verifies that the current user is logged in and is the
owner of the meeting before proceeding with the cancellation. If the meeting
is successfully canceled, a confirmation message is displayed. Otherwise,
appropriate error messages are shown.

Parameters:
    meeting_id (str): The ID of the meeting to be canceled.
    current_user (dict): The currently logged-in user information.

Raises:
    Exception: If an error occurs during the cancellation process.
"""
    if not current_user:
        click.echo("You need to log in first.")
        return
    
    try:
        # Fetch the meeting to ensure it belongs to the current user
        meeting = db.child("meetings").child(meeting_id).get()
        if not meeting.val():
            click.echo("Meeting not found.")
            return
        
        if meeting.val()['mentee_id'] != current_user['localId']:
            click.echo("You can only cancel your own meetings.")
            return
        
        # Cancel the meeting
        db.child("meetings").child(meeting_id).remove()
        click.echo("Meeting canceled successfully.")
    except Exception as e:
        click.echo(f"Error canceling meeting: {e}")