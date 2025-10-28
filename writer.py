from cpppo.server.enip import client
import time

host = "127.0.0.1"  # Change if server runs remotely (e.g., "192.168.1.86")

def tags():
    # Write values first
    yield f"Temperature=(REAL) {25.0  + (time.time() % 5):.2f}"
    yield f"Pressure=(REAL) {42.0  + (time.time() % 5):.2f}"
    yield f"MotorSpeed=(DINT){int(time.time() * 100 % 3000)}"

    # Then read them back
    # yield "Temperature"
    # yield "Pressure"
    # yield "MotorSpeed"

with client.connector(host=host) as conn:
    for depth in (1, 3):
        start = time.time()
        for index, descr, op, reply, status, value in conn.pipeline(
            operations=client.parse_operations(tags()), depth=depth
        ):
            if value is True:
                continue  # Skip writes
            print(f"{index:02d}: {descr:20s} → {value}")
        dur = time.time() - start
        print(f"Depth {depth}: Completed {index + 1} ops in {dur:.3f}s\n")
