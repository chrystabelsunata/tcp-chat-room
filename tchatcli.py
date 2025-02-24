import sys
import threading
import socket
import time

# client_connected = "Connected to {} on port {}".format(server_ip, port) DONE
# connection_failed_username_taken = "Connection Failed: Username Taken" DONE
# subscribe_added = "subscribe: {} added".format(hashtag) DONE
# subscribe_too_many = "subscribe: Too many Subscriptions" DONE
# message_sent = "{}: {} {} sent".format(username, hashtag, message) DONE
# message_illegal = "Message: Illegal Message" DONE
# unsubscribe_removed = "unsubscribe: {} removed".format(hashtag) DONE
# timeline_no_messages = "timeline: No Messages Available" DONE
# timeline_message = "{}: {} {}".format(sender_username, origin_hashtag, message) DONE
# exit_message = "Exiting client"DONE

server_name = 'localhost'
server_ip = str(sys.argv[1])
server_port = int(sys.argv[2])
username = str(sys.argv[3])

def start_client(host=server_name, port=server_port):
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_name, server_port))

    # send username
    client_socket.send(username.encode())
    

    server_listener = threading.Thread(target=receive_message, args = (client_socket, ))
    server_listener.start()
    
    while True:
        command = input(">> ").strip()
        if command.startswith("message"):
            parts = command.split(" ")
            hashtag, message = parts[1], " ".join(parts[2:])
            if 1 <= len(message) <= 150:
                message_sent = "{}: {} {} sent".format(username, hashtag, message)
                print(message_sent, flush=True)
        client_socket.send(command.encode())

        if command == 'exit':
            break


def receive_message(client_socket):
    while True:
        response = client_socket.recv(1024).decode()
        if response:
            print(f"\r{response.strip()}\n>> ", end="", flush=True)

if __name__ == "__main__":
    start_client()











