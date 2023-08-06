import socket
import psutil
import json
from datetime import datetime

def network_connections():
    print("\n")
    print("Gathering network connections...")
    print("\n")
    connections = psutil.net_connections()

    # Create a dictionary to map family constants to strings
    families = {
        socket.AF_INET: "IPV4",
        socket.AF_INET6: "IPV6",
        socket.AF_UNIX: "UNIX",
    }

    # Print the heading and then printing network connections
    details = []
    print(f"{'PID':<10}{'Process Name':<25}{'Family':<10}{'Local Address':<35}{'Remote Address':<35}{'Status':<35}")
    for conn in connections:
        laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
        raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
        family = families.get(conn.family, "N/A")
        try:
            process_name = psutil.Process(conn.pid).name() if conn.pid else "N/A"
        except psutil.NoSuchProcess:
            process_name = "N/A"
        detail = {
            "PID": conn.pid if conn.pid else "N/A",
            "Process Name": process_name,
            "Family": family,
            "Local Address": laddr,
            "Remote Address": raddr,
            "Status": conn.status
        }
        details.append(detail)
        print(f"{conn.pid if conn.pid else 'N/A':<10}{process_name:<25}{family:<10}{laddr:<35}{raddr:<35}{conn.status:<35}")

    # Prompt to save the output to a file
    save = input("\nDo you want to save these details to a file? (yes/no): ")
    if save.lower() == 'yes':
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        try:
            with open(f"network_{timestamp_str}.json", 'w') as f:
                json.dump(details, f)
            print(f"Details saved to network_{timestamp_str}.json")
        except Exception as e:
            print(f"Failed to save details: {e}")
