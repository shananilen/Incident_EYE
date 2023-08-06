import subprocess
import re
import json
import os
import datetime
#from datetime import datetime

def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False

def parse_journalctl_message(message):
    # Regular expression to match journalctl messages
    pattern = r'(?P<month>\S+)\s+(?P<day>\d{2})\s+(?P<time>\d{2}:\d{2}:\d{2})\s+(?P<host>\S+)\s+(?P<process>\S+):\s+(?P<message>.*)'
    match = re.match(pattern, message)

    if match:
        # If the message matches the pattern, return a dictionary of the matched groups
        return match.groupdict()
    else:
        # If the message doesn't match the pattern, return None
        return None

def save_logs(logs, filename):
    with open(filename, 'w') as f:
        json.dump(logs, f)

def gather_app_logs():
    print("\nPlease select the App/Service logs you want to gather:")
    print("1. Apache2")
    print("2. DHCP")
    print("3. OR enter the service name")
    print("4. Exit")
    print("\n")
    choice = input("Enter your choice: ")

    if choice == '1':
        service_name = 'apache2'
    elif choice == '2':
        service_name = 'isc-dhcp-server'
    elif choice == '3':
        print("---Use #systemctl list-units --type=service --- To determine the service")
        service_name = input("\nEnter the service name: ")
        # Check if the service exists
        try:
            services = subprocess.check_output(['systemctl', 'list-units', '--type=service']).decode('utf-8')
            if service_name not in services:
                print("Invalid service name. Please enter a valid service name.")
                gather_app_logs()
                return
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while checking service name: {e}")
            return
    elif choice == '4':
        print("Exiting...")
        return
    else:
        print("Invalid choice. Please choose a number between 1 and 4.")
        gather_app_logs()
        return

    while True:
        start_time = input("Enter the start time for the logs (format: YYYY-MM-DD HH:MM:SS): ")
        if validate_date(start_time):
            break
        else:
            print("Invalid date format. Please enter a valid date.")

    while True:
        end_time = input("Enter the end time for the logs (format: YYYY-MM-DD HH:MM:SS): ")
        if validate_date(end_time):
            break
        else:
            print("Invalid date format. Please enter a valid date.")


    print("\nPlease select the log level:")
    print("1. Emergency")
    print("2. Alert")
    print("3. Critical")
    print("4. Error")
    print("5. Warning")
    print("6. Notice")
    print("7. Info")
    print("8. Debug")

    level_choice = input("Enter your choice: ")

    if level_choice == '1':
        log_level = 'emerg'
    elif level_choice == '2':
        log_level = 'alert'
    elif level_choice == '3':
        log_level = 'crit'
    elif level_choice == '4':
        log_level = 'err'
    elif level_choice == '5':
        log_level = 'warning'
    elif level_choice == '6':
        log_level = 'notice'
    elif level_choice == '7':
        log_level = 'info'
    elif level_choice == '8':
        log_level = 'debug'
    else:
        print("Invalid choice. Please choose a number between 1 and 8.")
        gather_app_logs()
        return

    print(f"Gathering {service_name} logs from {start_time} to {end_time} with log level {log_level} and above...")
    try:
        logs = subprocess.check_output(['journalctl', '-u', service_name, '-p', log_level, '--since', start_time, '--until', end_time])
        log_messages = logs.decode('utf-8').split('\n')

        parsed_logs = []  # Create a list to store parsed log messages

        for message in log_messages:
            parsed_message = parse_journalctl_message(message)
            if parsed_message:
               # print(f"Timestamp: {parsed_message['timestamp']}")
                print(f"Timestamp: {parsed_message['month']} {parsed_message['day']} {parsed_message['time']}")
                print(f"Host: {parsed_message['host']}")
                print(f"Process: {parsed_message['process']}")
                print(f"Message: {parsed_message['message']}")
                print("-----")
                
                parsed_logs.append(parsed_message)  # Add parsed message to the list

        save_choice = input("\nDo you want to save the logs? (yes/no): ")
        if save_choice.lower() == 'yes':
            if not os.path.exists('logs'):
                os.makedirs('logs')
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            save_logs(parsed_logs, f'logs/parsed_{service_name}_logs_{timestamp}.json')
            print(f"\nLogs are save to the logs directory parsed_{service_name}_logs_{timestamp}.json file.")
            print("\n")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while gathering logs: {e}")
        return
    # Recursive call to allow multiple log gathering
    gather_app_logs()
