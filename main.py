# main.py

import network_connections
import running_processes
import network_config_check
import user_info
import gather_sys_logs
import gather_app_logs
import correlate_information
import analyse_logs
import ad_analyse_logs


def print_header():
    print("""

 ----------------------------------------------------------------
  _____            _     _            _     ________     ________
 |_   _|          (_)   | |          | |   |  ____\ \   / /  ____|
   | |  _ __   ___ _  __| | ___ _ __ | |_  | |__   \ \_/ /| |__
   | | | '_ \ / __| |/ _` |/ _ \ '_ \| __| |  __|   \   / |  __|
  _| |_| | | | (__| | (_| |  __/ | | | |_  | |____   | |  | |____
 |_____|_| |_|\___|_|\__,_|\___|_| |_|\__| |______|  |_|  |______|

 ----------------------------------------------------------------
                IncidentEYE v1.0 - Shanan Ilen
    """)

class IncidentResponseFramework:
    def __init__(self):
        self.logs = []
        self.incidents = []

    def run(self):
        print_header()
        print("Welcome to the Linux IR framework.")
        while True:
            print("\nPlease choose an option:")
            print("\n1. Gather Network Connections")
            print("2. Gather Running Processes")
            print("3. Correlate Network - Running information")
            print("4. Verify Network Configurations")
            print("5. Gather User Account Information")
            print("6. Gather, Parse & Store SYSTEM Logs")
            print("7. Gather, Parse & Store APPLICATION Logs")
            print("8. Analyse Logs")
            print("9. Advanced Logs analysis")
            print("10. Exit")
            try:
                print("\n")
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    result = network_connections.network_connections()
                    print(result)
                elif choice == 2:
                    result = running_processes.running_processes()
                    print(result)
                elif choice == 3:
                    result = correlate_information.correlate_information()
                    print(result)
                elif choice == 4:
                    result = network_config_check.network_config_check()
                    print(result)
                elif choice == 5:
                    result = user_info.user_info()
                    print(result)
                elif choice == 6:
                    result = gather_sys_logs.gather_sys_logs()
                    print(result)    
                elif choice == 7:
                    result = gather_app_logs.gather_app_logs()
                    print(result)
                elif choice == 8:
                    result = analyse_logs.analyse_logs()
                    print(result)    
                elif choice == 9:
                    result = ad_analyse_logs.ad_analyse_logs()
                    print(result)
                elif choice == 10:
                    print("Exiting the framework.")
                    break
                else:
                    print("Invalid choice. Please choose a number between 1 and 10.")
            except ValueError:
                print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    irf = IncidentResponseFramework()
    irf.run()
