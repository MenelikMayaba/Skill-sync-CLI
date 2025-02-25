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
            print(f"{mentor.val()['name']} (expertise: {mentor.val()['expertise']})")
    except Exception as e:
        print(f"Error fetching mentors: {e}")


def view_peers(current_user):
    if not current_user:
        print("You need to log in first.")
        return
    try:
        id_token = current_user['idToken']
        peers = db.child('users').order_by_child('role').equal_to('peer').get(token=id_token)
        print('\n available peers: ')
        for peer in peers.each():
            print(f"{peer.val()['name']} (expertise: {peer.val()['expertise']}")
    except Exception as e:
        print(f"Error fetching peer: {e}")