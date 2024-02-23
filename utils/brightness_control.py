import os
import logging
import subprocess
import platform
import screen_brightness_control as sbc

class BrightnessController:
    def __init__(self):
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        # Create a file handler and set the formatter
        log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),".." ,"brightness_controller.log")
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def Brightness_Increase(self):
        try:
            if platform.system() == 'Darwin':  # for mac
                command = ['osascript', '-e', 'tell application "System Events"', '-e', 'key code 144', '-e', 'end tell']
                subprocess.run(command)
                self.logger.info("Brightness Increased")
            elif platform.system() == 'Windows':  # for windows
                # get the brightness
                brightness = sbc.get_brightness()

                # increase the brightness for all displays
                new_brightness = [min(b + 5, 100) for b in brightness]

                # calculate the average brightness
                avg_brightness = int(sum(new_brightness) / len(new_brightness))

                # set the new brightness
                sbc.set_brightness(avg_brightness)
                print(avg_brightness)

                # show the current brightness for each detected monitor
                for monitor in sbc.list_monitors():
                    self.logger.info(f"{monitor} : {sbc.get_brightness(display=monitor)} %")
                
        except Exception as e:
            self.logger.error("Error increasing brightness: %s", e)

    def Brightness_Decrease(self):
        try:
            if platform.system() == 'Darwin':  # for mac
                command = ['osascript', '-e', 'tell application "System Events"', '-e', 'key code 145', '-e', 'end tell']
                subprocess.run(command)
                self.logger.info("Brightness Decreased")
            elif platform.system() == 'Windows':  # for windows
                # get the brightness
                brightness = sbc.get_brightness()

                # decrease the brightness for all displays
                new_brightness = [max(b - 5, 5) for b in brightness]

                # calculate the average brightness
                avg_brightness = int(sum(new_brightness) / len(new_brightness))

                # set the new brightness
                sbc.set_brightness(avg_brightness)
                print(avg_brightness)

                # show the current brightness for each detected monitor
                for monitor in sbc.list_monitors():
                    self.logger.info(f"{monitor} : {sbc.get_brightness(display=monitor)} %")
        except Exception as e:
            self.logger.error("Error decreasing brightness: %s", e)

if __name__ == "__main__":
    brightness_controller = BrightnessController()
    brightness_controller.Brightness_Increase()
    brightness_controller.Brightness_Decrease()
