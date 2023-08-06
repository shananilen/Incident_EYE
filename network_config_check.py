# network_config_check.py

import netifaces
import dns.resolver
import subprocess
import psutil

def network_config_check():
    print("Gathering network configuration...")

    # Get information about each network interface
    for interface in netifaces.interfaces():
        print(f"\nInterface: {interface}")

        # Get IP addresses
        if netifaces.AF_INET in netifaces.ifaddresses(interface):
            for addr in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                print(f"  IP Address: {addr['addr']}")
                print(f"  Netmask: {addr['netmask']}")

        # Get default gateway
        gws = netifaces.gateways()
        if gws['default'].get(netifaces.AF_INET):
            gw, _ = gws['default'][netifaces.AF_INET]
            print(f"  Default Gateway: {gw}")

    # Get DNS servers
    print("\nDNS Servers:")
    for server in dns.resolver.get_default_resolver().nameservers:
        print(f"  {server}")

    # Get routing table
    print("\nRouting Table:")
    route_output = subprocess.run(['ip', 'route'], capture_output=True, text=True).stdout
    for line in route_output.splitlines():
        print(f"  {line}")

    # Check for unexpected DNS servers
    print("\nDo you want to check for unexpected DNS servers? (yes/no)")
    choice = input("Enter your choice: ")
    if choice.lower() == 'yes':
        expected_dns_servers = ['8.8.8.8', '8.8.4.4']  # Replace with expected DNS servers
        for server in dns.resolver.get_default_resolver().nameservers:
            if server not in expected_dns_servers:
                print(f"WARNING: Unexpected DNS server {server}")

    # Check for open ports
    print("\nDo you want to check for open ports? (yes/no)")
    choice = input("Enter your choice: ")
    if choice.lower() == 'yes':
        expected_ports = [80, 443]  # Replace with expected open ports
        for conn in psutil.net_connections():
            if conn.status == 'LISTEN' and conn.laddr.port not in expected_ports:
                print(f"WARNING: Unexpected open port {conn.laddr.port}")
                
 
