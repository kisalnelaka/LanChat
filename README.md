---
##As seen on https://medium.com/@kisalnelaka6/building-a-blockchain-powered-encrypted-chat-application-with-python-103f116fad34

# Blockchain-Based Encrypted LAN Chat Application

A unique Python-based LAN chat application that combines **blockchain** technology for secure message storage, **end-to-end encryption** for privacy, and a **crypto-reward system** that simulates mining for each message sent.

## Features

- **Blockchain-Powered Messaging**: Each message is stored as a block on a local blockchain, ensuring tamper-proof and immutable chat history.
- **End-to-End Encryption**: Messages are encrypted using RSA keys, so only the intended recipient can decrypt and read them.
- **Crypto Rewards**: Each message sent simulates mining, earning the sender a small reward in their wallet.
- **Decentralized and Private**: Messages are stored and encrypted locally, with no reliance on a central server for message storage.

## Project Structure

- `blockchain.py`: Contains the `Block` and `Blockchain` classes for creating and managing the blockchain.
- `crypto_utils.py`: Manages RSA encryption/decryption and simulates a simple crypto wallet.
- `chat_client.py`: The main chat client for sending and receiving encrypted messages, mining rewards, and adding messages to the blockchain.
- `chat_server.py`: A simple server to broadcast messages between clients over the LAN.

## Getting Started

### Prerequisites

- **Python 3.x**
- Install the required libraries:
  ```bash
  pip install cryptography
  ```

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/blockchain-encrypted-chat.git
   cd blockchain-encrypted-chat
   ```

2. Make sure the following files are present:
   - `blockchain.py`
   - `crypto_utils.py`
   - `chat_client.py`
   - `chat_server.py`

### Running the Server

The server handles broadcasting messages to connected clients. Run this on one machine within the LAN:

```bash
python chat_server.py
```

You should see:
```
Server is running...
```

### Running the Client

1. Start the client on any machine within the same LAN as the server:
   ```bash
   python chat_client.py
   ```
2. Enter the server’s IP address and port when prompted:
   ```
   Enter server IP: 192.168.1.10  # Replace with actual server IP
   Enter port: 5555
   ```
3. Begin chatting! Type your message and press `Enter` to send.

4. To exit the chat, type:
   ```
   exit
   ```

## How It Works

### 1. Blockchain-Based Storage
   - Each message is stored as a block in a local blockchain.
   - Each block includes the encrypted message, timestamp, and sender information.
   - This structure ensures that the chat history is immutable and tamper-proof.

### 2. End-to-End Encryption
   - Each client generates an RSA key pair for encryption.
   - Messages are encrypted with the recipient's public key and decrypted with their private key.
   - This approach ensures that only the intended recipient can read the message.

### 3. Crypto Rewards
   - For every message sent, the client simulates "mining" by adding 1 coin to their local wallet balance.
   - This reward mechanism acts as an incentive for sending messages, though it's simulated and not a real cryptocurrency.

## File Breakdown

- **`blockchain.py`**: Implements a simplified blockchain structure.
  ```python
  class Block:
      # Initializes each message block, hashes and timestamps the message data.

  class Blockchain:
      # Manages the chain of blocks, adds new blocks, and ensures chain validity.
  ```

- **`crypto_utils.py`**: Handles encryption and mining rewards.
  ```python
  class CryptoWallet:
      # Manages the simulated crypto balance for each client.

  class EncryptionManager:
      # Generates RSA keys and encrypts/decrypts messages.
  ```

- **`chat_client.py`**: Connects to the server, handles encryption, and sends messages.
  ```python
  def mine_and_send_message(client_socket, message, recipient_public_key):
      # Encrypts the message, adds it to the blockchain, and mines a reward.

  def receive_messages(client_socket):
      # Continuously listens for and decrypts incoming messages.
  ```

- **`chat_server.py`**: Broadcasts messages between connected clients.

## Example Usage

1. **Starting the Server**:
   ```bash
   python chat_server.py
   ```
   Output:
   ```
   Server is running...
   ```

2. **Starting the Client**:
   ```bash
   python chat_client.py
   ```
   - Enter the server IP and port to connect.
   - Start sending encrypted messages.

3. **Sample Output for Mining**:
   Each time you send a message, a coin is mined, and your balance increases:
   ```
   Mined 1 coin. New balance: 1
   ```

## Security Notes

This project is a proof-of-concept for educational purposes:
- **Simplified Blockchain**: This blockchain does not implement consensus algorithms or P2P synchronization.
- **Mock Mining**: The mining reward is simulated and does not represent actual cryptocurrency mining.
- **Public Key Management**: In a real-world application, you'd need a secure method to distribute and verify public keys.

## Future Improvements

1. **Distributed Consensus**: Implement a consensus algorithm to make the blockchain truly decentralized.
2. **Real Cryptocurrency Integration**: Use APIs for actual cryptocurrencies, like Monero or Ethereum, to reward users.
3. **Enhanced Peer-to-Peer Network**: Implement a P2P network to eliminate the need for a central server.

## Contributing

Feel free to fork this repository, make changes, and create pull requests. Contributions are welcome!

## License

This project is licensed under the BSL-1.0 license.

---

With this setup, you're ready to explore blockchain, encryption, and reward-based communication in a simple Python application. Happy coding, and enjoy your journey into decentralized chat systems!

---
