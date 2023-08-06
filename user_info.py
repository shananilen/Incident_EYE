# user_info.py

import pwd
import grp
import os
import subprocess
import spwd
import datetime


def get_group_name(username):
    # Get the group name for a user.
    user_info = pwd.getpwnam(username)
    group_info = grp.getgrgid(user_info.pw_gid)
    return group_info.gr_name

def user_info():
    print("Gathering user information...")
    # Get information about all user accounts
    print("\n{:<10} {:<10} {:<10} {:<12} {:<30} {:<30} {:<20}".format('UID', 'Username', 'GID', 'Group Name', 'Description', 'Home Directory', 'Shell'))
    for p in pwd.getpwall():
        # Ignore system accounts
        if p.pw_uid >= 1000 and 'nologin' not in p.pw_shell:
            group_name = get_group_name(p.pw_name)
            print("{:<10} {:<10} {:<10} {:<12} {:<30} {:<30} {:<20}".format(p.pw_uid, p.pw_name, p.pw_gid, group_name, p.pw_gecos, p.pw_dir, p.pw_shell))

    # Ask if the user wants to examine an user in-detail
    choice = input("\nDo you want to examine an user in-detail? (yes/no) :")
    if choice.lower() == 'yes':
        try:
            uid = int(input("Enter the UID of the user: "))
            p = pwd.getpwuid(uid)

            print(f"\nExamining user {p.pw_name}:")

            # Get the date of the last password change
            user_info = spwd.getspnam(p.pw_name)
            days_since_1970 = user_info.sp_lstchg
            if days_since_1970:
                password_changed_date = datetime.date(1970, 1, 1) + datetime.timedelta(days_since_1970)
            else:
                password_changed_date = "Unknown"
            print("\n")
            print(f"Password last changed: {password_changed_date}")

            # Check for sudo privileges
            print("\nSudo privileges:")
            try:
                output = subprocess.run(['sudo', '-l', '-U', p.pw_name], capture_output=True, text=True, check=True).stdout
                print(output)
            except subprocess.CalledProcessError as e:
                print(f"Error checking sudo privileges: {e}")

            # Get login history
            print("\nLogin history:")
            output = subprocess.run(['last', '-n', '10', p.pw_name], capture_output=True, text=True).stdout
            print(output)

            # Get failed login attempts
            print("\nFailed login attempts:")
            output = subprocess.run(['faillog', '-u', p.pw_name], capture_output=True, text=True).stdout
            if not output.strip():
                print("No failed login attempts recorded by faillog.")
                print("Note: For more detailed logs, consider querying the systemd journal using 'journalctl'.")
            else:
                print(output)

            # Get user activity
            print("\nUser activity:")
            output = subprocess.run(['w', '-h', p.pw_name], capture_output=True, text=True).stdout
            print(output)

            # Get user processes
            print("\nUser processes:")
            output = subprocess.run(['ps', '-u', p.pw_name], capture_output=True, text=True).stdout
            print(output)

            # Get user's cron jobs
            print("\nCron jobs:")
            result = subprocess.run(['crontab', '-l', '-u', p.pw_name], capture_output=True, text=True)
            if result.returncode == 0:
                print(result.stdout)
            else:
                print("No cron jobs")

        except (ValueError, KeyError):
            print("Invalid UID. Please enter an UID from the List")
