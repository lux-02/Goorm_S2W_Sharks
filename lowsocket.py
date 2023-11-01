import socket
import ssl
import concurrent.futures

target_ip = "43.200.177.222"
ports = list(range(1, 5000))
timeout = 1
MAX_THREADS = 50


def banner_grabbing(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    if port == 443:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            s = ctx.wrap_socket(s, server_hostname=ip)
        except ssl.SSLError as e:
            print(f"[-] SSL error on port {port}: {e}")
            return

    try:
        s.connect((ip, port))

        if port in [80, 443]:
            s.send(b"GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % ip.encode())

        banner = s.recv(1024).decode(errors='ignore')
        if banner:
            print()
            print('-----------------------------------')
            print(f"[+] Port {port} : {banner.strip()}")
            print('-----------------------------------')

    except socket.error as e:
        pass
    finally:
        s.close()


with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    executor.map(banner_grabbing, [target_ip]*len(ports), ports)
