import time
import random
import logging
from cpppo.server.enip import client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EtherNetIPClient")

def write_tags():
    host = "127.0.0.1"  # Change if server runs elsewhere

    # Define tags and their value generation
    tags = {
        "Temperature": lambda: round(random.uniform(20.0, 35.0), 2),
        "Pressure": lambda: round(random.uniform(1.0, 10.0), 2),
        "MotorSpeed": lambda: random.randint(1000, 3000)
    }

    logger.info(f"Connecting to EtherNet/IP server at {host}...")
    with client.connector(host=host) as conn:
        logger.info("Connected successfully!")

        while True:
            for tag, value_gen in tags.items():
                value = value_gen()
                try:
                    conn.write(tag, value)
                    logger.info(f"Wrote {tag} = {value}")
                except Exception as e:
                    logger.error(f"Failed to write {tag}: {e}")
            time.sleep(2)

if __name__ == "__main__":
    write_tags()
