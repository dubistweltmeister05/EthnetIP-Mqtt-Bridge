import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Any
from pycomm3 import LogixDriver
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EtherNetIPToMQTT:
    """Bridge between EtherNet/IP devices and MQTT broker."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the bridge with configuration."""
        self.config = config
        self.mqtt_client = None
        self.plc = None
        self.running = False
        
    def setup_mqtt(self):
        """Set up MQTT client connection."""
        mqtt_config = self.config['mqtt']
        
        def on_connect(client, userdata, flags, rc, properties=None):
            if rc == 0:
                logger.info(f"Connected to MQTT broker at {mqtt_config['broker']}:{mqtt_config['port']}")
            else:
                logger.error(f"Failed to connect to MQTT broker, return code: {rc}")
        
        def on_disconnect(client, userdata, rc, properties=None):
            logger.warning(f"Disconnected from MQTT broker, return code: {rc}")
            if rc != 0 and self.running:
                logger.info("Attempting to reconnect...")
        
        def on_publish(client, userdata, mid, properties=None):
            logger.debug(f"Message {mid} published successfully")
        
        self.mqtt_client = mqtt.Client(
            client_id=mqtt_config.get('client_id', 'ethernetip_bridge'),
            protocol=mqtt.MQTTv5
        )
        
        if mqtt_config.get('username') and mqtt_config.get('password'):
            self.mqtt_client.username_pw_set(
                mqtt_config['username'],
                mqtt_config['password']
            )
        
        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.on_disconnect = on_disconnect
        self.mqtt_client.on_publish = on_publish
        
        try:
            self.mqtt_client.connect(
                mqtt_config['broker'],
                mqtt_config['port'],
                60
            )
            self.mqtt_client.loop_start()
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            return False
    
    def setup_plc(self):
        """Set up connection to EtherNet/IP PLC."""
        plc_config = self.config['ethernetip']
        
        try:
            self.plc = LogixDriver(plc_config['ip_address'])
            self.plc.open()
            logger.info(f"Connected to PLC at {plc_config['ip_address']}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to PLC: {e}")
            return False
    
    def read_tags(self) -> Dict[str, Any]:
        """Read configured tags from PLC."""
        tags = self.config['ethernetip']['tags']
        results = {}
        
        if not self.plc:
            logger.error("PLC connection not established")
            return results
        
        for tag in tags:
            try:
                response = self.plc.read(tag)
                if hasattr(response, 'error') and response.error:
                    logger.error(f"Error reading tag {tag}: {response.error}")
                    results[tag] = None
                elif hasattr(response, 'value'):
                    results[tag] = response.value
                    logger.debug(f"Read {tag}: {response.value}")
                else:
                    results[tag] = None
            except Exception as e:
                logger.error(f"Exception reading tag {tag}: {e}")
                results[tag] = None
        
        return results
    
    def publish_to_mqtt(self, data: Dict[str, Any]):
        """Publish data to MQTT broker."""
        if not self.mqtt_client or not self.mqtt_client.is_connected():
            logger.warning("MQTT client not connected, skipping publish")
            return
        
        mqtt_config = self.config['mqtt']
        topic_base = mqtt_config.get('topic_base', 'ethernetip')
        
        payload = {
            'timestamp': datetime.utcnow().isoformat(),
            'device': self.config['ethernetip']['ip_address'],
            'data': data
        }
        
        topic = f"{topic_base}/data"
        
        try:
            result = self.mqtt_client.publish(
                topic,
                json.dumps(payload),
                qos=mqtt_config.get('qos', 1),
                retain=mqtt_config.get('retain', False)
            )
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.info(f"Published to {topic}: {len(data)} tags")
            else:
                logger.error(f"Failed to publish: {result.rc}")
        except Exception as e:
            logger.error(f"Exception publishing to MQTT: {e}")
    
    def run(self):
        """Main loop to read tags and publish to MQTT."""
        poll_interval = self.config.get('poll_interval', 5)
        
        if not self.setup_mqtt():
            logger.error("Failed to set up MQTT connection")
            return
        
        if not self.setup_plc():
            logger.error("Failed to set up PLC connection")
            self.mqtt_client.loop_stop()
            return
        
        self.running = True
        logger.info(f"Starting polling loop (interval: {poll_interval}s)")
        
        try:
            while self.running:
                try:
                    data = self.read_tags()
                    self.publish_to_mqtt(data)
                except Exception as e:
                    logger.error(f"Error in polling loop: {e}")
                
                time.sleep(poll_interval)
        
        except KeyboardInterrupt:
            logger.info("Received interrupt signal, shutting down...")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up connections."""
        self.running = False
        
        if self.plc:
            try:
                self.plc.close()
                logger.info("Closed PLC connection")
            except Exception as e:
                logger.error(f"Error closing PLC connection: {e}")
        
        if self.mqtt_client:
            try:
                if hasattr(self.mqtt_client, 'loop_stop'):
                    self.mqtt_client.loop_stop()
                self.mqtt_client.disconnect()
                logger.info("Disconnected from MQTT broker")
            except Exception as e:
                logger.error(f"Error disconnecting from MQTT: {e}")


def load_config(config_file: str = 'config.json') -> Dict[str, Any]:
    """Load configuration from JSON file."""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        mqtt_broker = os.getenv('MQTT_BROKER')
        mqtt_port = os.getenv('MQTT_PORT')
        mqtt_username = os.getenv('MQTT_USERNAME')
        mqtt_password = os.getenv('MQTT_PASSWORD')
        plc_ip = os.getenv('PLC_IP_ADDRESS')
        
        if mqtt_broker:
            config['mqtt']['broker'] = mqtt_broker
        if mqtt_port:
            config['mqtt']['port'] = int(mqtt_port)
        if mqtt_username:
            config['mqtt']['username'] = mqtt_username
        if mqtt_password:
            config['mqtt']['password'] = mqtt_password
        if plc_ip:
            config['ethernetip']['ip_address'] = plc_ip
        
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file {config_file} not found")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in configuration file: {e}")
        raise


if __name__ == "__main__":
    logger.info("EtherNet/IP to MQTT Bridge starting...")
    
    config = load_config()
    bridge = EtherNetIPToMQTT(config)
    bridge.run()
