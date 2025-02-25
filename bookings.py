from Authentication import *
from peer_mentor import *
from calender_api import authenticate_google_calendar, create_event

@click.command()
@click.option("--mentor-id", prompt="Mentor ID", help="Enter the Mentor's ID")
@click.option("--time", prompt="Meeting Time (YYYY-MM-DD HH:MM)", help="Enter the desired meeting time")
@click.option('--current-user', required=True, help='Current logged-in user')
def request_meeting(mentor_id, time, current_user):
    if not current_user:
        click.echo("you need to log in first")
        return
    
    mentee_id = current_user['localId']
    meeting_data = {'mentor_id': mentor_id, 'mentee_id': mentee_id, 'time': time, 'status': 'pending'}
    db.child('meetings').push(meeting_data)
    click.echo("Meeting Request Sent")

    service = authenticate_google_calendar()
    start_time = f"{time}:00"
    end_time = f"{time}:00"
    timezone = "UTC"
    event_link = create_event(service, "Mentor Meeting", start_time, end_time, timezone, attendees=[current_user['email']])
    click.echo(f"Meeting Request Sent. Google Calendar event created: {event_link}")

@click.command()
@click.option('--current-user', required=True, help='Current logged-in user')
def view_bookings(current_user):
    if not current_user:
        click.echo("you need to login first")
        return
    
    bookings = db.child('meetings').order_by_child('mentee_id').equal_to(current_user['localId']).get()
    click.echo('\n your bookings: ')
    for booking in bookings.each():
        click.echo(f"- Mentor ID: {booking.val()['mentor_id']}, Time: {booking.val()['time']}, Status: {booking.val()['status']}")

@click.command()
@click.option("--meeting-id", prompt="Meeting ID", help="Enter the Meeting ID to cancel")
def cancel_booking(meeting_id):
    try:
        db.child("meetings").child(meeting_id).remove()
        click.echo("Meeting canceled successfully.")
    except Exception as e:
        click.echo(f"Error canceling meeting: {e}")