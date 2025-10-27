# EtherNet/IP to MQTT Bridge

A Python application that reads data from EtherNet/IP devices (PLCs) and publishes it to an MQTT broker. This enables integration of industrial automation data with IoT platforms and other MQTT-based systems.

## Features

- **Web-based Dashboard**: Configure and monitor the bridge through a user-friendly web interface
- **Real-time Status Monitoring**: View connection status for MQTT and PLC in real-time
- Connect to Allen-Bradley and other EtherNet/IP compatible PLCs
- Read multiple tags from PLC at configurable intervals
- Publish data to MQTT broker in JSON format with timestamp
- Support for MQTT authentication
- Automatic reconnection handling with exponential backoff
- Comprehensive logging
- Environment variable support for sensitive configuration
- Start/Stop bridge control from web interface

## Requirements

- Python 3.11+
- Flask (Web interface)
- pycomm3 (EtherNet/IP communication)
- paho-mqtt (MQTT client)
- python-dotenv (configuration management)

## Configuration

### config.json

The main configuration file defines:

```json
{
  "mqtt": {
    "broker": "mqtt.example.com",
    "port": 1883,
    "client_id": "ethernetip_bridge",
    "topic_base": "ethernetip",
    "qos": 1,
    "retain": false,
    "username": "",
    "password": ""
  },
  "ethernetip": {
    "ip_address": "192.168.1.100",
    "tags": [
      "Temperature",
      "Pressure",
      "FlowRate",
      "Status"
    ]
  },
  "poll_interval": 5
}
```

### Environment Variables

You can override configuration values using environment variables:

- `MQTT_BROKER` - MQTT broker hostname
- `MQTT_PORT` - MQTT broker port
- `MQTT_USERNAME` - MQTT authentication username
- `MQTT_PASSWORD` - MQTT authentication password
- `PLC_IP_ADDRESS` - PLC IP address

Copy `.env.example` to `.env` and configure as needed.

## Usage

### Web Interface (Recommended)

1. Run the Flask web application:

```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`
3. Use the web dashboard to:
   - View real-time status of MQTT and PLC connections
   - Start/Stop the bridge
   - Configure all settings through the web interface
   - Monitor the current configuration

### Command Line Interface (Alternative)

1. Edit `config.json` with your PLC IP address and tags to monitor
2. Configure MQTT broker settings
3. (Optional) Set environment variables in `.env` file
4. Run the application directly:

```bash
python main.py
```

## Web Interface Features

### Dashboard
- Real-time connection status indicators
- Start/Stop bridge controls
- View current configuration at a glance
- Auto-refreshing status updates every 3 seconds

### Configuration Page
- Edit MQTT broker settings (host, port, credentials)
- Configure PLC connection (IP address, tags to monitor)
- Set poll interval
- Adjust MQTT QoS and retain settings
- Save configuration without restarting the application

## MQTT Message Format

Messages are published to `{topic_base}/data` with the following JSON structure:

```json
{
  "timestamp": "2025-10-27T12:34:56.789012",
  "device": "192.168.1.100",
  "data": {
    "Temperature": 72.5,
    "Pressure": 14.7,
    "FlowRate": 125.3,
    "Status": 1
  }
}
```

## Supported PLC Types

The application uses pycomm3 and supports:
- Allen-Bradley CompactLogix
- Allen-Bradley ControlLogix
- Allen-Bradley Micro800
- Other EtherNet/IP compatible devices

## Error Handling

- **Automatic Reconnection**: Both MQTT and PLC connections automatically reconnect with exponential backoff
- Connection failures are logged and the application will attempt to reconnect
- Tag read errors are logged, and null values are sent for failed reads
- MQTT publish failures are logged but don't stop the polling loop
- Maximum reconnection delay capped at 60 seconds
- Connection recovery detection triggers immediate reconnection attempts

## Logging

All operations are logged with timestamps. Log levels:
- INFO: Successful operations, connections, data flow
- WARNING: Connection issues, publish skips
- ERROR: Failed operations, exceptions
- DEBUG: Detailed tag read information

## Customization

### Using the Web Interface

1. Navigate to the Configuration page
2. Update any settings through the web form
3. Click "Save Configuration"
4. Restart the bridge if it's currently running

### Manually Editing config.json

#### Adding More Tags

Edit the `tags` array in `config.json`:

```json
"tags": [
  "YourTag1",
  "YourTag2",
  "Array[0]",
  "Struct.Member"
]
```

#### Changing Poll Interval

Modify `poll_interval` in `config.json` (value in seconds):

```json
"poll_interval": 10
```

#### MQTT QoS and Retain

Adjust MQTT publish settings:

```json
"qos": 2,
"retain": true
```

## Troubleshooting

**Cannot connect to PLC:**
- Verify PLC IP address is correct
- Check network connectivity
- Ensure PLC has EtherNet/IP enabled
- Verify firewall settings

**Cannot connect to MQTT broker:**
- Verify broker hostname and port
- Check authentication credentials
- Ensure broker is accessible from your network

**Tag read errors:**
- Verify tag names match exactly (case-sensitive)
- Check that tags exist in the PLC program
- Ensure proper data type compatibility

## License

This project is open source and available for use in industrial automation applications.
