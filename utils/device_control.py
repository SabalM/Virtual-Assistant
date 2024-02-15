import os
import platform
import time

def system_control(choice):
    try:
        system_platform = platform.system().lower()

        if system_platform == 'windows':
            if choice == 'shutdown':
                cmd = os.system('shutdown /s /t 5')
            elif choice == 'sleep':
                cmd = os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            elif choice == 'logoff':
                cmd = os.system('shutdown /l')
            else:
                raise ValueError('Invalid choice')

        elif system_platform == 'linux':
            if choice == 'shutdown':
                cmd = os.system('sudo shutdown -h +5')
            elif choice == 'sleep':
                cmd = os.system('systemctl suspend')
            elif choice == 'logoff':
                cmd = os.system('gnome-session-quit --logout --no-prompt')
            else:
                raise ValueError('Invalid choice')

        # TODO: system_platform == 'macos'

        else:
            raise OSError('Unsupported operating system.')
        
        time.sleep(5)  # 5-second delay
        
    except Exception as e:
        print(f"An error occurred: {e}")
        cmd = None

    return cmd
