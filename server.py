import socket
import threading
import logging

# Server Configuration
HOST = '0.0.0.0'
PORT = 12345

# List to keep track of all connected clients and usernames
clients = []
usernames = {}

# Logging configuration
LOG_FILE = 'chat.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# Broadcast messages to all connected clients
def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            client.send(message)

# Format messages for command responses
def format_command_response(message):
    return f"*** {message} ***\n".encode('utf-8')

# Handle individual client connections
def handle_client(client_socket):
    username = None

    try:
        # Prompt the user for their name
        client_socket.send("Enter your name: ".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8').strip()
        logging.info(f"User connected with name: {username}")

        # Add the client to connected lists
        usernames[client_socket] = username
        clients.append(client_socket)

        # Notify others
        broadcast(f"[Notification]: {username} has joined the chat!\n".encode('utf-8'))
        client_socket.send(format_command_response("Welcome to the chat! Type /help for available commands."))
        logging.info(f"{username} has joined the chat.")

        while True:
            # Receive messages from the client
            message = client_socket.recv(1024)
            if not message:
                break

            decoded_msg = message.decode('utf-8').strip()

            # Handle commands
            if decoded_msg.startswith('/'):
                if decoded_msg == '/list':
                    # Send list of connected users
                    user_list = "Online Users:\n" + "\n".join(usernames.values())
                    client_socket.send(format_command_response(user_list))
                elif decoded_msg == '/help':
                    # Show available commands
                    help_message = (
                        "Available commands:\n"
                        "/list - Show online users\n"
                        "/help - Show this help message\n"
                        "Type any message to chat publicly.\n"
                    )
                    client_socket.send(format_command_response(help_message))
                else:
                    # Unknown command
                    client_socket.send(format_command_response("Unknown command. Type /help for a list of commands."))
            else:
                # Broadcast the message to other clients
                broadcast(f"{username}: {decoded_msg}\n".encode('utf-8'), client_socket)
                logging.info(f"{username}: {decoded_msg}")

    except ConnectionResetError:
        logging.info(f"Connection reset by {username if username else 'unknown user'}.")
    except Exception as e:
        logging.error(f"Error handling client {username if username else 'unknown'}: {e}")
    finally:
        # Cleanup when a client disconnects
        if client_socket in clients:
            clients.remove(client_socket)
        if client_socket in usernames:
            broadcast(f"[Notification]: {usernames[client_socket]} has left the chat.\n".encode('utf-8'))
            del usernames[client_socket]
        client_socket.close()

# Main function to start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server started on {HOST}:{PORT}")

    while True:
        # Accept new client connections
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")

        # Start a new thread to handle the client
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
