from flask import Flask, jsonify, request
import socket
import ssl
import concurrent.futures
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


MAX_THREADS = 50
timeout = 1


def banner_grabbing(ip, port):
    results = []

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    if port == 443:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            s = ctx.wrap_socket(s, server_hostname=ip)
        except ssl.SSLError as e:
            return f"[-] SSL error on port {port}: {e}"

    try:
        s.connect((ip, port))

        if port in [80, 443]:
            s.send(b"GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % ip.encode())

        banner = s.recv(1024).decode(errors='ignore')
        if banner:
            results.append((port, banner.strip()))

    except socket.error as e:
        pass
    finally:
        s.close()

    return results


@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    target_ip = data['target_ip']
    ports = list(range(1, 5000))

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        scan_results = executor.map(
            banner_grabbing, [target_ip]*len(ports), ports)
        for result in scan_results:
            results.extend(result)

    return jsonify(results=results)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
