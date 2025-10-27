# EtherNet/IP to MQTT Bridge

## Overview
This project is a Python-based data bridge that connects EtherNet/IP industrial devices (PLCs) to MQTT brokers. It reads tag values from Allen-Bradley and compatible PLCs at configurable intervals and publishes the data to an MQTT broker in JSON format.

## Project Purpose
- Enable integration of industrial automation data with IoT platforms
- Bridge OT (Operational Technology) and IT systems via MQTT
- Provide real-time data streaming from PLCs to cloud or local MQTT brokers

## Current State
- Core functionality implemented (EtherNet/IP reading + MQTT publishing)
- Flask web interface for configuration and monitoring
- Real-time status dashboard
- Configuration via JSON file with environment variable overrides
- Robust error handling and automatic reconnection logic with exponential backoff
- Comprehensive logging

## Recent Changes
- **2025-10-27**: Initial project setup
  - Created main application with EtherNetIPToMQTT class
  - Implemented PLC connection using pycomm3
  - Implemented MQTT publishing using paho-mqtt
  - Added configuration system with JSON and environment variables
  - Created documentation and example configuration
  - Added automatic reconnection logic for both MQTT and PLC connections
  
- **2025-10-27**: Flask Web Interface Addition
  - Installed Flask framework
  - Created Flask web application (app.py)
  - Built web dashboard with real-time status monitoring
  - Added configuration page for web-based settings management
  - Implemented Start/Stop bridge controls via web interface
  - Created responsive CSS styling and JavaScript for auto-refreshing status
  - Updated workflow to run Flask app on port 5000
  - Updated documentation to reflect web interface features
  
- **2025-10-27**: Migration to cpppo Library
  - Replaced pycomm3 with cpppo for EtherNet/IP communication
  - Updated PLC connection handling to use cpppo's client.connector API
  - Modified tag reading to use cpppo's synchronous operations
  - Improved support for various CIP devices beyond just Logix controllers
  - Better handling of high-latency industrial network connections

## Project Architecture

### Structure
```
.
├── app.py                    # Flask web application
├── main.py                   # Core bridge logic and EtherNetIPToMQTT class
├── config.json               # Configuration file (user editable)
├── .env.example              # Example environment variables
├── templates/                # Flask HTML templates
│   ├── base.html             # Base template with navigation
│   ├── index.html            # Dashboard page
│   └── config.html           # Configuration page
├── static/                   # Static assets
│   ├── css/style.css         # Styling
│   └── js/main.js            # JavaScript
├── README.md                 # User documentation
└── replit.md                 # Project memory and documentation
```

### Dependencies
- **Flask**: Web framework for configuration interface
- **cpppo**: EtherNet/IP CIP protocol communication library
- **paho-mqtt**: MQTT client library
- **python-dotenv**: Environment variable management

### Key Components
1. **Flask Web Application (app.py)**:
   - Dashboard with real-time status monitoring
   - Configuration page for settings management
   - REST API endpoints for bridge control (/api/start, /api/stop, /api/status)
   - Threading support to run bridge in background
   - Thread-safe bridge instance management

2. **EtherNetIPToMQTT Class (main.py)**: Main bridge logic
   - PLC connection management using cpppo's client.connector API
   - Automatic reconnection with exponential backoff
   - MQTT client setup with MQTTv5 support
   - Tag polling loop using cpppo's synchronous operations
   - Data publishing with timestamp
   - Exponential backoff reconnection strategy (max 60s delay)
   - Connection health detection and recovery
   - Support for various CIP data types (INT, DINT, REAL, SSTRING, etc.)

3. **Configuration System**:
   - JSON-based configuration (config.json)
   - Environment variable overrides for sensitive data
   - Flexible tag list configuration
   - Web-based configuration editor

4. **Error Handling**:
   - Automatic reconnection for MQTT with exponential backoff
   - Automatic reconnection for PLC with exponential backoff
   - Connection loss detection via ConnectionError exceptions
   - Graceful degradation on read failures
   - Comprehensive logging at all levels

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
- Application runs as Flask web server on port 5000
- Bridge operates in background thread when started via web interface
- Data is published with UTC timestamps
- Supports both authenticated and unauthenticated MQTT connections
- Web dashboard auto-refreshes status every 3 seconds
- Configuration can be edited via web interface or directly in config.json
- Bridge can be controlled (start/stop) via web interface or run standalone with main.py
