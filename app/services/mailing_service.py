import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from jinja2 import Template

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
        <p style="color: gray; font-size: 18px;">Team Library App</p>
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

def sendEmailReport(to, subject, report_data):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to
    msg['Subject'] = subject

    template_str = """
    <html>
    <head></head>
    <body>
        <p style="color: black; font-size: 18px;">Hi Sir/Mam</p>
        <br/>
        <p style="color: black; font-size: 18px;">Please find a montly activity report</p>
        <br/>
        <table style="border-collapse: collapse; width: 100%;">
        <tr>
            <th style="border: 1px solid #dddddd; text-align: left; padding: 8px; background-color: #f2f2f2;">Book Name</th>
            <th style="border: 1px solid #dddddd; text-align: left; padding: 8px; background-color: #f2f2f2;">Author</th>
            <th style="border: 1px solid #dddddd; text-align: left; padding: 8px; background-color: #f2f2f2;">Section</th>
            <th style="border: 1px solid #dddddd; text-align: left; padding: 8px; background-color: #f2f2f2;">Status</th>
            <th style="border: 1px solid #dddddd; text-align: left; padding: 8px; background-color: #f2f2f2;">Days Requested</th>
            <th style="border: 1px solid #dddddd; text-align: left; padding: 8px; background-color: #f2f2f2;">Is Returned</th>
        </tr>
        {% for book in report_data %}
        <tr>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{{ book.book_name }}</td>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{{ book.author }}</td>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{{ book.section }}</td>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{{ book.status }}</td>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{{ book.days_requested }}</td>
            <td style="border: 1px solid #dddddd; text-align: left; padding: 8px;">{{ book.is_returned }}</td>
        </tr>
        {% endfor %}
    </table>
        <br/>
        <p style="color: gray; font-size: 18px;">Best Regards</p>
        <p style="color: gray; font-size: 18px;">Team Library App</p>
    </body>
    </html>
    """
    template = Template(template_str)
    html_content = template.render(report_data=report_data)
    # Attach the HTML content to the email message
    msg.attach(MIMEText(html_content, "html"))
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
