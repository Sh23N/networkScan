import socket
def scan(target, ports):
    print('\n[+] Starting Scan For', target)
    for port in range(1, ports + 1):
        scan_port(target, port)

def scan_port(ipaddress, port):
    try:
        sock = socket.socket()
        sock.settimeout(0.5)
        sock.connect((ipaddress, port))
        print(f"[+] Port {port} is open on {ipaddress}")
        sock.close()
    except:
        pass

targets = input("[*] Enter Targets To Scan (separated by comma): ")
ports = int(input("[*] Enter How Many Ports You Want To Scan (e.g. 100): "))

if ',' in targets:
    print("[*] Scanning Multiple Targets...")
    for ip_addr in targets.split(','):
        scan(ip_addr.strip(), ports)
else:
    scan(targets.strip(), ports)
input("enter any kay to exit")