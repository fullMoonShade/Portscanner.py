import pyfiglet
import sys
import socket
from datetime import datetime
import threading

stop_event = threading.Event()


# Banner 
ascii_banner = pyfiglet.figlet_format("Port Scanner")
print(ascii_banner)

if len(sys.argv) == 2:
    target = socket.gethostbyname(sys.argv[1])  
else:
    print("Invalid argument. Please provide a valid hostname or IP address.")
    sys.exit()

print("-" * 50)
print("Scanning Target: " + target)
print("Scanning started at: " + str(datetime.now()))
print("-" * 50)

def scan_port(port):
    if stop_event.is_set():
        return
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.5)
        result = s.connect_ex((target, port))
        if result == 0:
            print(f"Port {port} is open")
        s.close()
    except Exception as e:
        pass

try:
    threads = []
    for port in range(1, 65535):
        if stop_event.is_set():
            break
        thread = threading.Thread(target=scan_port, args=(port,))
        threads.append(thread)
        thread.start()

        if len(threads) >= 200: # Adjust Threads
            for thread in threads:
                thread.join()
            threads = []

    for thread in threads:
        thread.join()

except KeyboardInterrupt:
    print("\nExiting Program!!!")
    stop_event.set()
    for thread in threads:
        thread.join()
    sys.exit()

except socket.gaierror:
    print("\nHostname Could Not Be Resolved!!!")
    sys.exit()
except socket.error:
    print("\nServer not responding!!!")
    sys.exit()
