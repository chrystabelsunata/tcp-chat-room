import sys
import threading
import socket

# Formatted Print Statements for the Server Side.

# server_started = "Server started on port {}. Accepting connections".format(port) DONE
# user_logged_in = "{} logged in".format(username) DONE
# user_logged_out = "{} logged out".format(username)
# subscribe_confirm = "{}: subscribed {}".format(username, hashtag) DONE
# unsubscribe_confirm = "{}: unsubscribed {}".format(username, hashtag) DONE
# message_received_sent = "{}: {} {} sent".format(username, hashtag, message)DONE

lock = threading.Lock()

server_name = 'localhost'
server_port = int(sys.argv[1])

connected_clients = {} # {username: socket}
subscription = {} # {hashtag: list of users}
user_subscription = {} # {username: list of hashtags}
user_messages = {} # {username: messages received}

def start_server(host=server_name, port=server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("Server started on port {}. Accepting connections".format(server_port), flush=True)

    while True:
        client_socket, client_address = server_socket.accept()
        client_process = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_process.start()
    

def handle_client(client_socket, client_address):
    
    username = client_socket.recv(1024).decode()
    login(client_socket, username)
    while True:
        command = client_socket.recv(1024).decode()
        parts = command.split(" ")

        user_command = parts[0]
        
        if user_command == 'subscribe':
            hashtag = parts[1]
            subscribe(client_socket, username, hashtag)
        elif user_command == 'unsubscribe':
            hashtag = parts[1]
            unsubscribe(client_socket, username, hashtag)
        elif user_command == 'message':
            hashtag, message = parts[1], " ".join(parts[2:])
            broadcast_message(client_socket, hashtag, message, username)
        elif user_command == 'timeline':
            timeline(client_socket, username)
        elif user_command == 'exit':
            exit(client_socket, username)
        

def login(client_socket, username):
    if username in connected_clients:
        connection_failed_username_taken = "Connection Failed: Username Taken"
        client_socket.send(connection_failed_username_taken.encode())
        return
    
    client_connected = "Connected to {} on port {}".format('127.0.0.1', server_port)
    client_socket.send(client_connected.encode())
    user_logged_in = "{} logged in".format(username)
    print(user_logged_in, flush=True)
    connected_clients[username] = client_socket

    user_messages[username] = []


def broadcast_message(client_socket, hashtag, message, username):
    if len(message) > 150 or len(message) < 1:
        message_illegal = "Message: Illegal Message"
        client_socket.send(message_illegal.encode())
        return

    message_sent = "{}: {} {} sent".format(username, hashtag, message)
    print(message_sent, flush=True)

    if hashtag not in subscription:
        subscription[hashtag] = []

    subscribers_list = subscription[hashtag]

    if '#ALL' in subscription:
        subscribers_list = list(set(subscribers_list + subscription['#ALL']))

    for subscriber_username in subscribers_list:
        subscribed_client_socket = connected_clients[subscriber_username]

        message_sent_subscriber = "{}: {} {}".format(username, hashtag, message)
        subscribed_client_socket.send((message_sent_subscriber + "\n").encode())

        user_messages[subscriber_username].append((username, hashtag, message))


def subscribe(client_socket, username, hashtag):
    
    if hashtag not in subscription:
        subscription[hashtag] = []

    if username not in user_subscription:
        user_subscription[username] = []

    if len(user_subscription[username]) >= 5:
        subscribe_too_many = "subscribe: Too many Subscriptions"
        client_socket.send(subscribe_too_many.encode())
        return

    if hashtag not in user_subscription[username]:
        user_subscription[username].append(hashtag)
        if username not in subscription[hashtag]:
            subscription[hashtag].append(username)
    
    subscribe_confirm = "{}: subscribed {}".format(username, hashtag)
    print(subscribe_confirm, flush=True)

    subscribe_added = "subscribe: {} added".format(hashtag)
    client_socket.send(subscribe_added.encode())


def unsubscribe(client_socket, username, hashtag):
    
    subscription[hashtag].remove(username)
    user_subscription[username].remove(hashtag)

    unsubscribe_confirm = "{}: unsubscribed {}".format(username, hashtag)
    print(unsubscribe_confirm, flush=True)

    unsubscribe_removed = "unsubscribe: {} removed".format(hashtag)
    client_socket.send(unsubscribe_removed.encode())


def timeline(client_socket, username):
    if username not in user_messages or len(user_messages[username]) == 0:
        timeline_no_messages = "timeline: No Messages Available"
        client_socket.send(timeline_no_messages.encode())
        return

    messages_received_list = user_messages[username]
    for sender_username, origin_hashtag, message in messages_received_list:
        timeline_message = "{}: {} {}".format(sender_username, origin_hashtag, message)
        client_socket.send((timeline_message + "\n").encode())
    
    user_messages[username].clear()

def exit(client_socket, username):
    
    if username in connected_clients:
        del connected_clients[username]
    
    if username in user_subscription:
        for hashtag in user_subscription[username]:
            if hashtag in subscription and username in subscription[hashtag]:
                subscription[hashtag].remove(username)

        del user_subscription[username]
    
    if username in user_messages:
        del user_messages[username]


    user_logged_out = "{} logged out".format(username)
    print(user_logged_out, flush=True)
    exit_message = "Exiting client"
    client_socket.send(exit_message.encode())
    client_socket.close()

if __name__ == "__main__":
    start_server()









