import json
import os
import threading
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv
from main import EtherNetIPToMQTT, load_config

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SESSION_SECRET', 'dev-secret-key')

bridge_instance = None
bridge_thread = None
bridge_lock = threading.Lock()


def get_bridge_status():
    """Get the current status of the bridge."""
    with bridge_lock:
        if bridge_instance is None:
            return {
                'status': 'stopped',
                'running': False,
                'mqtt_connected': False,
                'plc_connected': False
            }
        
        return {
            'status': 'running' if bridge_instance.running else 'stopped',
            'running': bridge_instance.running,
            'mqtt_connected': bridge_instance.mqtt_client and bridge_instance.mqtt_client.is_connected() if bridge_instance.mqtt_client else False,
            'plc_connected': bridge_instance.plc is not None
        }


@app.route('/')
def index():
    """Main dashboard page."""
    status = get_bridge_status()
    try:
        config = load_config()
    except:
        config = {
            'mqtt': {
                'broker': '',
                'port': 1883,
                'client_id': 'ethernetip_bridge',
                'topic_base': 'ethernetip',
                'qos': 1,
                'retain': False,
                'username': '',
                'password': ''
            },
            'ethernetip': {
                'ip_address': '',
                'tags': []
            },
            'poll_interval': 5
        }
    
    return render_template('index.html', config=config, status=status)


@app.route('/config', methods=['GET', 'POST'])
def config_page():
    """Configuration page."""
    if request.method == 'POST':
        try:
            config_data = {
                'mqtt': {
                    'broker': request.form.get('mqtt_broker', ''),
                    'port': int(request.form.get('mqtt_port', 1883)),
                    'client_id': request.form.get('mqtt_client_id', 'ethernetip_bridge'),
                    'topic_base': request.form.get('mqtt_topic_base', 'ethernetip'),
                    'qos': int(request.form.get('mqtt_qos', 1)),
                    'retain': request.form.get('mqtt_retain') == 'on',
                    'username': request.form.get('mqtt_username', ''),
                    'password': request.form.get('mqtt_password', '')
                },
                'ethernetip': {
                    'ip_address': request.form.get('plc_ip_address', ''),
                    'tags': [tag.strip() for tag in request.form.get('plc_tags', '').split(',') if tag.strip()]
                },
                'poll_interval': int(request.form.get('poll_interval', 5))
            }
            
            with open('config.json', 'w') as f:
                json.dump(config_data, f, indent=2)
            
            return jsonify({'success': True, 'message': 'Configuration saved successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 400
    
    try:
        config = load_config()
    except:
        config = {
            'mqtt': {
                'broker': '',
                'port': 1883,
                'client_id': 'ethernetip_bridge',
                'topic_base': 'ethernetip',
                'qos': 1,
                'retain': False,
                'username': '',
                'password': ''
            },
            'ethernetip': {
                'ip_address': '',
                'tags': []
            },
            'poll_interval': 5
        }
    
    return render_template('config.html', config=config)


@app.route('/api/start', methods=['POST'])
def start_bridge():
    """Start the bridge."""
    global bridge_instance, bridge_thread
    
    with bridge_lock:
        if bridge_instance and bridge_instance.running:
            return jsonify({'success': False, 'message': 'Bridge is already running'})
        
        try:
            config = load_config()
            bridge_instance = EtherNetIPToMQTT(config)
            
            bridge_thread = threading.Thread(target=bridge_instance.run, daemon=True)
            bridge_thread.start()
            
            return jsonify({'success': True, 'message': 'Bridge started successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Failed to start bridge: {str(e)}'}), 500


@app.route('/api/stop', methods=['POST'])
def stop_bridge():
    """Stop the bridge."""
    global bridge_instance
    
    with bridge_lock:
        if not bridge_instance or not bridge_instance.running:
            return jsonify({'success': False, 'message': 'Bridge is not running'})
        
        try:
            bridge_instance.running = False
            bridge_instance.cleanup()
            
            return jsonify({'success': True, 'message': 'Bridge stopped successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Failed to stop bridge: {str(e)}'}), 500


@app.route('/api/status', methods=['GET'])
def status():
    """Get the current status of the bridge."""
    return jsonify(get_bridge_status())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
