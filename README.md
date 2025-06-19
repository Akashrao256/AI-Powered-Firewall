# AI-Powered Network Firewall

A Python-based network firewall implementation with AI-driven threat detection, rate limiting, and IP whitelisting capabilities.

## Features

- AI-based traffic analysis using Random Forest classifier
- Rate limiting to prevent DDoS attacks
- IP whitelisting
- Real-time traffic monitoring and logging
- Multi-threaded connection handling

## Components

- [server.py](server.py) - Main firewall server implementation
- [client.py](client.py) - Test client for normal connections
- [firewall_ai_model.pkl.py](firewall_ai_model.pkl.py) - AI model training script
- [Rate Limiting.py](Rate%20Limiting.py) - Rate limiting test script
- [Normal Traffic.py](Normal%20Traffic.py) - Normal traffic simulation
- [Malicious Traffic.py](Malicious%20Traffic.py) - Malicious traffic simulation

## Setup

1. Train the AI model first:
```python
python firewall_ai_model.pkl.py
```

2. Start the firewall server:
```python
python server.py
```

3. Test connections using the client:
```python
python client.py
```

## Configuration

Default settings in [server.py](server.py):
- Host: 127.0.0.1
- Port: 65432
- Rate limit: 5 requests per 60 seconds
- Allowed IPs: ['127.0.0.1', '192.168.1.100']

## Testing

You can test different scenarios using the provided scripts:

- Normal traffic:
```python
python "Normal Traffic.py"
```

- Rate limiting:
```python
python "Rate Limiting.py"
```

- Malicious traffic:
```python
python "Malicious Traffic.py"
```

## Logging

All events are logged to `firewall_log.txt` with timestamps for monitoring and debugging.

## Requirements

- Python 3.x
- scikit-learn
- numpy
