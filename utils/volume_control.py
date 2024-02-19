import os
import logging
import platform

class ActionHandler:
    def __init__(self, predicted_class=None):
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        # Create a file handler and set the formatter
        log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "action_handler.log")
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def volume_increase(self):
        try:
            # Check if the system is Windows
            if platform.system() == 'Windows':
                # Powershell script to increase volume by 6
                ps_script = "$obj = new-object -com wscript.shell; " + \
                            "1..3 | ForEach-Object { $obj.SendKeys([char]175) }"

                # Run the PowerShell script
                os.system('powershell.exe -Command "' + ps_script + '"')
            else:
                # Increase volume for non-Windows systems
                for _ in range(100):
                    os.system("cliclick kp:volume-up kp:volume-up")
            self.logger.info("Volume Increased")
        except Exception as e:
            self.logger.error("Error increasing volume: %s", e)


    def volume_decrease(self):
        try:
            # Check if the system is Windows
            if platform.system() == 'Windows':
                # Define the PowerShell script
                ps_script = "$obj = new-object -com wscript.shell; " + \
                            "1..3 | ForEach-Object { $obj.SendKeys([char]174) }"
                
                # Run the PowerShell script
                os.system('powershell.exe -Command "' + ps_script + '"')
            else:
                # Decrease volume for non-Windows systems
                for _ in range(5):
                    os.system("cliclick kp:volume-down kp:volume-down")
            self.logger.info("Volume Decreased")
        except Exception as e:
            self.logger.error("Error decreasing volume: %s", e)