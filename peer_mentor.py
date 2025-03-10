from Authentication import *

def view_mentors(current_user):
    """
Displays a list of available mentors for the current user.

This function checks if the user is logged in by verifying the presence
of a valid `current_user`. If the user is logged in, it retrieves and
prints a list of mentors from the database, displaying each mentor's ID,
name, and expertise. If an error occurs during the retrieval process,
an error message is printed.

Parameters:
    current_user (dict): A dictionary containing the current user's
    authentication details, including the 'idToken'.

Returns:
    None
"""
    if not current_user:
        print("You need to log in first.")
        return
    
    try:
        id_token = current_user['idToken']
        mentors = db.child('users').order_by_child('role').equal_to('mentor').get(token=id_token)
        print('\nAvailable mentors:')
        for mentor in mentors.each():
            mentor_data = mentor.val()
            print(f"ID: {mentor.key()}, Name: {mentor_data['name']} (expertise: {mentor_data.get('expertise', 'None')})")
    except Exception as e:
        print(f"Error fetching mentors: {e}")


def view_peers(current_user):
    """
Displays a list of available peers for the current user.

This function checks if the user is logged in by verifying the presence
of a valid `current_user`. If the user is logged in, it retrieves and
displays peers with the role 'peer' from the database using the user's
ID token for authentication. Each peer's ID, name, and expertise are
printed. If an error occurs during data retrieval, an error message is
displayed.

Parameters:
    current_user (dict): A dictionary containing the current user's
    authentication details, including the 'idToken'.

Returns:
    None
"""
    if not current_user:
        print("You need to log in first.")
        return
    try:
        id_token = current_user['idToken']
        peers = db.child('users').order_by_child('role').equal_to('peer').get(token=id_token)
        print('\nAvailable peers:')
        for peer in peers.each():
            peer_data = peer.val()
            print(f"ID: {peer.key()}, Name: {peer_data['name']} (expertise: {peer_data.get('expertise', 'None')})")
    except Exception as e:
        print(f"Error fetching peer: {e}")