# EtherNet/IP to MQTT Bridge

## Overview
This project is a Python-based data bridge that connects EtherNet/IP industrial devices (PLCs) to MQTT brokers. It reads tag values from Allen-Bradley and compatible PLCs at configurable intervals and publishes the data to an MQTT broker in JSON format.

## Project Purpose
- Enable integration of industrial automation data with IoT platforms
- Bridge OT (Operational Technology) and IT systems via MQTT
- Provide real-time data streaming from PLCs to cloud or local MQTT brokers

## Current State
- Core functionality implemented (EtherNet/IP reading + MQTT publishing)
- Configuration via JSON file with environment variable overrides
- Error handling and reconnection logic
- Comprehensive logging

## Recent Changes
- **2025-10-27**: Initial project setup
  - Created main application with EtherNetIPToMQTT class
  - Implemented PLC connection using pycomm3
  - Implemented MQTT publishing using paho-mqtt
  - Added configuration system with JSON and environment variables
  - Created documentation and example configuration

## Project Architecture

### Structure
```
.
├── main.py              # Main application and bridge logic
├── config.json          # Configuration file (user editable)
├── .env.example         # Example environment variables
├── README.md            # User documentation
└── replit.md           # Project memory and documentation
```

### Dependencies
- **pycomm3**: EtherNet/IP protocol communication
- **paho-mqtt**: MQTT client library
- **python-dotenv**: Environment variable management

### Key Components
1. **EtherNetIPToMQTT Class**: Main bridge logic
   - PLC connection management
   - MQTT client setup
   - Tag polling loop
   - Data publishing

2. **Configuration System**:
   - JSON-based configuration
   - Environment variable overrides for sensitive data
   - Flexible tag list configuration

3. **Error Handling**:
   - Connection retry logic
   - Graceful degradation on read failures
   - Comprehensive logging

## Configuration

### Required Settings
- MQTT broker hostname/IP and port
- PLC IP address
- List of tags to monitor
- Poll interval (seconds)

### Optional Settings
- MQTT authentication (username/password)
- MQTT QoS and retain settings
- Custom topic base

## User Preferences
None documented yet.

## Notes
- Application runs in console mode with continuous polling
- Data is published with UTC timestamps
- Supports both authenticated and unauthenticated MQTT connections
