import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

sender_email = os.getenv("APP_EMAIL")
password = os.getenv("PASS_KEY")


def sendEmail(to, subject, message):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to
    msg['Subject'] = subject

    html = f"""
    <html>
    <head></head>
    <body>
        <p style="color: black; font-size: 18px;">Hi Sir/Mam</p>
        <br/>
        <p style="color: black; font-size: 18px;">{message}</p>
        <br/>
        <p style="color: gray; font-size: 18px;">Best Regards</p>
        <p style="color: gray; font-size: 18px;">Team Libraray App</p>
    </body>
    </html>
    """

    # Attach the HTML content to the email message
    msg.attach(MIMEText(html, "html"))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        server.login(sender_email, password)
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.close()

        return True
    except Exception as e:
        print(e)
        return False

