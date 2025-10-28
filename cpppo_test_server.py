import logging
import threading
import time
from cpppo.server.enip.server import enip_server  # ✅ fixed import

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cpppo_test_server")

def start_cpppo_server(ip="0.0.0.0", port=44818, tags=None):
    if tags is None:
        tags = {
            "Temperature": {"type": "REAL", "value": 25.0},
            "Pressure": {"type": "REAL", "value": 1.0},
            "FlowRate": {"type": "REAL", "value": 10.0},
            "Status": {"type": "DINT", "value": 1},
        }

    logger.info(f"Starting cpppo ENIP server on {ip}:{port} with tags: {tags}")

    # Create and start ENIP server
    with enip_server(address=(ip, port), tags=tags) as server:
        logger.info("cpppo ENIP server running.")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            logger.info("Shutting down cpppo ENIP server.")

if __name__ == "__main__":
    t = threading.Thread(target=start_cpppo_server, kwargs={"ip": "127.0.0.1", "port": 44818})
    t.daemon = True
    t.start()
    logger.info("cpppo test server running. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down cpppo test server.")
