import smtplib

class Mail:
    def __init__(self):
        self.sender = "daniel.radu@student.tuiasi.ro"
        self.sender_pass = "pobu tevh snjk ajhw"
        self.receiver = "daniel.radu@student.tuiasi.ro"

    def sendMail(self, message):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(self.sender, self.sender_pass)
        s.sendmail(self.sender, self.receiver, message)
        s.quit()



