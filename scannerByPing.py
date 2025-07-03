import socket
import subprocess
import ipaddress
import platform
import threading

active_hosts = []
lock=threading.Lock()

def get_local_ip():
    # Get the IP address of the local machine.
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def get_network_range():
    #Get the IP range based on the local IP and subnet.
    #This assumes a default /24 subnet (e.g., 192.168.1.0/24).
    
    local_ip = get_local_ip()
    print(str(local_ip))
    network = ipaddress.IPv4Network(local_ip + '/24', strict=False)
    return network


def ping_ip(ip):
    # Ping an IP address to check if it's active.
    # Returns True if active, otherwise False.
    param=""
    wait=""
    print(str(ip))
    os=platform.system().lower()
    if os=="windows":
        param="-n"
        wait="-w"
    else:
        param="-c"
        wait="-W"
   
    response = subprocess.run(
        ["ping", param, "1", wait, "1000", str(ip)], 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    #deside by exit code
    return response.returncode == 0


def get_hostname(ip):
    #Get the hostname of an active IP address.
    try:
        hostname = socket.gethostbyaddr(str(ip))
        return hostname[0]
    except socket.herror:
        return None

def check_range(ip_list):
    for ip in ip_list:
        if ping_ip(ip):
            hostname = get_hostname(ip)
            with lock:
                active_hosts.append((str(ip), hostname or "Unknown"))

def scan_network_split_threads(num_threads=10):
    network = list(get_network_range()) 
    chunk_size = len(network) // num_threads
    threads = []

    for i in range(num_threads):
        start = i * chunk_size
        if i != num_threads - 1:
            end = (i + 1) * chunk_size
        else:
            end = len(network)
        ip_chunk = network[start:end]

        t = threading.Thread(target=check_range, args=(ip_chunk,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return active_hosts

if __name__ == "__main__":
    print("Scanning network for active hosts...\n")
    active_hosts = scan_network_split_threads(num_threads=10)

    if active_hosts:
        print("Active hosts in the network:")
        for ip, hostname in active_hosts:
            print(f"IP: {ip}, Hostname: {hostname}")
    else:
        print("No active hosts found in the network.")
        input("pleas enter a kay to exit.")
