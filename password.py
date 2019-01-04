import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
import time

constants_known_owners = {"Isla": 'islachan.giftia@gmail.com'}

email = 'islachan.giftia@gmail.com'
password = 'ubuntu123!'
subject = 'Door Assistant'
message = ' is assessing the door at '
qr_location = './password.png'
client_location = './client.png'

class Password:

    def __init__(self, client):
        self.time = time.ctime()
        self.client = client
        self.client_email = constants_known_owners[self.client]
        self.msg = MIMEMultipart()
        self.msg['From'] = email
        self.msg['To'] = self.client_email
        self.msg['Subject'] = subject
        self.msg.attach(MIMEText(self.client + message + self.time, 'plain'))

    def run(self):
        self.attach()
        self.send()

    def attach(self):
        filename = os.path.basename(qr_location)
        attachment = open(qr_location, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        self.msg.attach(part)

        filename = os.path.basename(client_location)
        attachment = open(client_location, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        self.msg.attach(part)

    def send(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        text = self.msg.as_string()
        server.sendmail(email, self.client_email, text)
        server.quit()

if __name__ == "__main__":
    print("sending email")
    owner = "Isla"
    send_password = Password(owner)
    send_password.run()
    print("email sent")



