import subprocess
import re
import json
import os
import datetime


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

def gather_sys_logs():
    print("\nPlease select which logs you want to gather:")
    print("1. Syslogs")
    print("2. Auth Logs")
    print("3. Kernel Logs")
    print("4. System Daemon Logs")
    print("5. Exit")
    print("\n")
    choice = input("Enter your choice: ")

    if choice == '1':
        log_type = 'syslog'
        log_category = 'Syslog'
    elif choice == '2':
        log_type = 'auth'
        log_category = 'Auth'
    elif choice == '3':
        log_type = 'kern'
        log_category = 'Kernel'
    elif choice == '4':
        log_type = 'daemon'
        log_category = 'System Daemon'
    elif choice == '5':
        print("Exiting...")
        return
    else:
        print("Invalid choice. Please choose a number between 1 and 5.")
        gather_sys_logs()
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
        gather_sys_logs()
        return

    print(f"Gathering {log_category} logs from {start_time} to {end_time} with log level {log_level} and above...")
    try:
        logs = subprocess.check_output(['journalctl', '--facility', log_type, '-p', log_level, '--since', start_time, '--until', end_time])
        log_messages = logs.decode('utf-8').split('\n')

        parsed_logs = []  # Create a list to store parsed log messages

        for message in log_messages:
            parsed_message = parse_journalctl_message(message)
            if parsed_message:
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
            save_logs(parsed_logs, f'logs/parsed_{log_type}_logs_{timestamp}.json')
            print(f"\nLogs are save to the logs directory parsed_{log_type}_logs_{timestamp}.json file.")
            print("\n")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while gathering logs: {e}")
        return
    # Recursive call to allow multiple log gathering
    gather_sys_logs()
