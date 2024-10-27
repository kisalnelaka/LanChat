import socket
import threading
import os
from colorama import init, Fore, Style
from termcolor import colored

# Initialize colorama for Windows compatibility
init(autoreset=True)

# Global flags and variables
running = True
online_users = []

# Function to receive messages from the server
def receive_messages(client_socket):
    global running
    while running:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith("[UserList]"):
                # Update the list of online users
                global online_users
                online_users = message[len("[UserList]"):].split(",")
                print(colored("[System]: Updated user list.", 'cyan'))
            elif message:
                # Display the received message
                print(colored(message, 'green'))
            else:
                break
        except (ConnectionResetError, OSError):
            if running:
                print(colored("[Error]: Disconnected from the server.", 'red'))
            break

# Function to display the list of online users
def display_user_list():
    global online_users
    print(colored("[System]: Online users:", 'cyan'))
    for user in online_users:
        print(colored(f"- {user}", 'cyan'))

# Function to display help
def display_help():
    help_text = """
    [System]: Available commands:
    /help           - Show this help message
    /list           - Show online users
    /whisper <user> - Send a private message to a user
    /exit           - Leave the chat
    """
    print(colored(help_text, 'cyan'))

# Function to send private messages
def send_private_message(client_socket, username, recipient, message):
    private_message = f"[Whisper from {username} to {recipient}]: {message}"
    client_socket.send(f"/whisper {recipient} {message}".encode('utf-8'))
    # Display the private message locally
    print(colored(private_message, 'magenta'))

# Main function to start the client
def start_client():
    global running
    # Get the server URL, port, and username from the user
    server_url = input(Fore.YELLOW + "Enter server IP address or URL: " + Style.RESET_ALL).strip()
    port = int(input(Fore.YELLOW + "Enter server port: " + Style.RESET_ALL).strip())
    username = input(Fore.YELLOW + "Enter your name: " + Style.RESET_ALL).strip()

    # Attempt to connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_url, port))
    except (ConnectionRefusedError, socket.gaierror):
        print(colored("[Error]: Unable to connect to the server.", 'red'))
        return

    # Send the username to the server
    client_socket.send(username.encode('utf-8'))

    # Start a thread to listen for incoming messages from the server
    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.daemon = True
    thread.start()

    # Display a welcome message
    print(colored(f"[System]: Welcome {username}! Type '/help' to see available commands.", 'cyan'))

    # Main loop for sending messages
    while True:
        # Get user input
        message = input(Fore.YELLOW + "> " + Style.RESET_ALL).strip()

        # Process commands
        if message.lower() == "/exit":
            running = False
            client_socket.close()
            break
        elif message.lower() == "/help":
            display_help()
        elif message.lower() == "/list":
            display_user_list()
        elif message.startswith("/whisper"):
            try:
                parts = message.split(" ", 2)
                recipient = parts[1]
                private_message = parts[2]
                send_private_message(client_socket, username, recipient, private_message)
            except IndexError:
                print(colored("[Error]: Usage: /whisper <user> <message>", 'red'))
        else:
            # Send the message to the server
            client_socket.send(message.encode('utf-8'))
            # Display the user's message locally
            print(colored(f"{username}: {message}", 'cyan'))

    # Wait for the receive thread to finish
    thread.join()

    # Clean up and close the connection
    client_socket.close()

if __name__ == "__main__":
    start_client()
