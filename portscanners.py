from flask import Flask, request, render_template
import socket
import json
import threading
import time

app = Flask(__name__)

def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except OSError:
        return "Unknown"

def scan_ports(target, start_port, end_port, results):
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.1)
                result = sock.connect_ex((target, port))
                if result == 0:
                    service_name = get_service_name(port)
                    results.append((port, service_name))
        except KeyboardInterrupt:
            return ["Scan interrupted."]
        except socket.gaierror:
            return ["Hostname could not be resolved. Exiting"]
        except socket.error:
            return ["Couldn't connect to server"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan_ports', methods=['POST'])
def start_scan():
    data = json.loads(request.data)
    target = data['target']
    start_port = 0
    end_port = 65535
    results = []
    start_time = time.time()

    threads = []
    thread_count = 100  # Adjust the number of threads as needed
    ports_per_thread = (end_port - start_port + 1) // thread_count

    for i in range(thread_count):
        thread_start = start_port + i * ports_per_thread
        thread_end = thread_start + ports_per_thread - 1
        if i == thread_count - 1:
            thread_end = end_port
        thread = threading.Thread(target=scan_ports, args=(target, thread_start, thread_end, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    time_taken = end_time - start_time

    return {'results': results, 'time_taken': time_taken}

if __name__ == '__main__':
    app.run(debug=True)
