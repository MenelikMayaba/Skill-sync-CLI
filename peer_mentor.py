from Authentication import *

def view_mentors(current_user):
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