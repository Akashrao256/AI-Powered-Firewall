import socket

# Define host and port
HOST = '127.0.0.1'
PORT = 65432

# Create a socket and set a timeout
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(20)  # 20-second timeout

try:
    # Connect to the firewall server
    client.connect((HOST, PORT))

    # Send a message
    message = "Hello, Firewall!"
    client.send(f"{len(message):<64}".encode('utf-8'))  # Send message length first
    client.send(message.encode('utf-8'))

    # Receive response
    response = client.recv(1024).decode('utf-8')
    print(f"Server response: {response}")

    # If no response was received, indicate an issue
    if not response:
        print("No response received from server.")
except socket.timeout:
    print("Error: Connection timed out.")
except socket.error as e:
    print(f"Error connecting to the server: {e}")
finally:
    # Close connection
    client.close()
