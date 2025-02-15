import socket
import threading
import time
from datetime import datetime
from collections import defaultdict
import joblib
import numpy as np
import os

# Define host and port
HOST = '127.0.0.1'
PORT = 65432

# Define allowed IP addresses
ALLOWED_IPS = ['127.0.0.1', '192.168.1.100']

# Constants
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# Rate limiting configuration
RATE_LIMIT_TIMEFRAME = 60  # seconds
RATE_LIMIT_THRESHOLD = 5   # max requests per IP in the timeframe

# Rate limiting tracker
connection_attempts = defaultdict(list)

# Path to model file
MODEL_PATH = r"d:\Python\firewall_ai_model.pkl"

# Check if the model file exists
if os.path.exists(MODEL_PATH):
    model_data = joblib.load(MODEL_PATH)  # Load the dictionary containing the model and scaler
    ai_model = model_data['model']        # Extract the model from the dictionary
    scaler = model_data['scaler']         # Extract the scaler from the dictionary
    print(f"Model loaded successfully from {MODEL_PATH}")
else:
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

# Logging
def log_event(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("firewall_log.txt", "a") as log_file:
        log_file.write(f"{timestamp} - {message}\n")
    print(message)

# Rate limiting check
def is_rate_limited(ip):
    current_time = time.time()
    connection_attempts[ip] = [t for t in connection_attempts[ip] if current_time - t < RATE_LIMIT_TIMEFRAME]
    if len(connection_attempts[ip]) >= RATE_LIMIT_THRESHOLD:
        return True
    connection_attempts[ip].append(current_time)
    return False

# Feature extraction (you can enhance this to match your model's expected features)
def extract_features(ip, msg):
    request_rate = len(connection_attempts[ip])
    payload_size = len(msg)
    header_anomalies = 0  # Placeholder for header anomaly logic
    return np.array([request_rate, payload_size, header_anomalies])

# Connection handler
def handle_connection(conn, addr):
    log_event(f"[NEW CONNECTION] {addr} connected.")
    with conn:
        while True:
            try:
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(FORMAT)

                    log_event(f"[RECEIVED MESSAGE] {msg} from {addr[0]}")

                    # Rate limiting check
                    if is_rate_limited(addr[0]):
                        log_event(f"[RATE LIMIT] {addr[0]} exceeded rate limit.")
                        conn.send("Rate limit exceeded. Try again later.".encode(FORMAT))
                        return

                    # Check if IP is allowed
                    if addr[0] not in ALLOWED_IPS:
                        log_event(f"[DENIED] Connection from {addr[0]} is not allowed.")
                        conn.send("Access Denied.".encode(FORMAT))
                        return

                    # Feature extraction and AI classification
                    features = extract_features(addr[0], msg)
                    features_scaled = scaler.transform([features])  # Scale features before prediction
                    prediction = ai_model.predict(features_scaled)[0]  # Predict using the AI model
                    if prediction == 1:
                        log_event(f"[BLOCKED] {addr[0]} classified as malicious by AI.")
                        conn.send("Blocked by AI.".encode(FORMAT))
                        return

                    # Log message and send confirmation
                    log_event(f"[MESSAGE] {addr[0]}: {msg}")
                    conn.send("Message Received.".encode(FORMAT))  # This sends the confirmation back to client
                else:
                    break
            except Exception as e:
                log_event(f"[ERROR] {addr[0]}: {e}")
                break

# Main function to start the server
if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        server.listen()
        log_event(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    except Exception as e:
        log_event(f"[ERROR] Failed to bind server: {e}")
        exit()

    try:
        while True:
            conn, addr = server.accept()
            log_event(f"[CONNECTION ESTABLISHED] {addr[0]}:{addr[1]} connected.")
            thread = threading.Thread(target=handle_connection, args=(conn, addr), daemon=True)
            thread.start()
            log_event(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    except KeyboardInterrupt:
        log_event("[SHUTDOWN] Server is shutting down.")
    finally:
        server.close()
