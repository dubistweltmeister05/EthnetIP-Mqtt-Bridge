import time
import random
import logging
from cpppo.server.enip import main

logging.basicConfig(level=logging.INFO)

def run_server():
    logging.info("Starting EtherNet/IP simulation server on 0.0.0.0:44818 with tag 'Temperature'")

    # Run the cpppo server directly using its main loop API
    # This exposes the 'Temperature' tag of type REAL
    try:
        main.main(
            argv=[
                "--address", "0.0.0.0",
                "Temperature=REAL",
                "Pressure=REAL",
                "MotorSpeed=DINT",
                "--print"
            ]
        )
    except KeyboardInterrupt:
        logging.info("Server shutting down...")

if __name__ == "__main__":
    run_server()
