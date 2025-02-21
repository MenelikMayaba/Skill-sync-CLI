from Authentication import *

@click.command()
def view_mentors():
    try:
        mentor = db.child('user').order_by_child('role').equal_to('mentor').get()
        click.echo('\n avaiable mentors: ')
        for mentor in mentor.each():
            click.echo(f"{mentor.val()['name']} (expertise: {mentor.val()['expertise']})")
    except Exception as e:
        click.echo(f"Error fetching mentor: {e}")


@click.command()
def view_peers():
    try:
        peer = db.child('user').order_by_child('role').equal_to('peer').get()
        click.echo('\n available peers: ')
        for peer in peer.each():
            click.echo(f"{peer.val()['name']} (expertise: {peer.val()['expertise']}")
    except Exception as e:
        click.echo(f"Error fetching peer: {e}")

