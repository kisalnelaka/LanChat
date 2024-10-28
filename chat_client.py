import socket
import threading
import time
from blockchain import Blockchain, Block
from crypto_utils import CryptoWallet, EncryptionManager

# Initialize components
blockchain = Blockchain()
wallet = CryptoWallet()
encryption_manager = EncryptionManager()

def mine_and_send_message(client_socket, message, recipient_public_key):
    # Encrypt message
    encrypted_message = encryption_manager.encrypt_message(message, recipient_public_key)
    
    # Add encrypted message to blockchain as a new block
    new_block = Block(len(blockchain.chain), blockchain.get_latest_block().hash, time.time(), encrypted_message)
    blockchain.add_block(new_block)
    
    # Simulate mining reward
    wallet.mine(amount=1)
    
    # Send message
    client_socket.sendall(encrypted_message)

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            # Decrypt and print the message
            decrypted_message = encryption_manager.decrypt_message(data)
            print(f"Received message: {decrypted_message}")
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

# Main client function
def start_client():
    server_address = input("Enter server IP: ")
    port = int(input("Enter port: "))
    
    # Connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, port))

    # Start receiving messages in a separate thread
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    print("Connected! Type your messages below.")
    while True:
        message = input("> ")
        if message.lower() == "exit":
            break
        
        # In this example, we assume the server distributes the recipient's public key
        recipient_public_key = encryption_manager.get_public_key()  # Replace with actual recipient's key
        mine_and_send_message(client_socket, message, recipient_public_key)

    client_socket.close()

if __name__ == "__main__":
    start_client()
