import socket
import concurrent.futures

def scan_port(host, port):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((host, port))

        if result == 0:
            return port

        sock.close()

    except:
        pass

    return None


def port_scan(host):

    ports = [21,22,23,25,53,80,110,143,443,445,3306,8080]

    open_ports = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:

        results = executor.map(lambda p: scan_port(host, p), ports)

        for r in results:
            if r:
                open_ports.append(r)

    return open_ports
