import base64
import os
from python_http_client.exceptions import HTTPError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Cc, Attachment, FileContent, FileName, FileType, Disposition)


useSendGrid = "doha"
if useSendGrid == "jithu":
    apikey = os.getenv('apiKey')
    fromMail = os.getenv('fromMail')
else:
    apikey = os.getenv("apiKey")
    fromMail = os.getenv("fromMail")


def send_mail(toEmail, emailSubject, emailTemplate, cc=[]):
    message = Mail(
        from_email=fromMail,
        to_emails=toEmail,
        subject=emailSubject,
        html_content=emailTemplate
    )
    # CC MAILS
    cc_emails = []
    if cc:
        for c in cc:
            cc_emails.append(Cc(c, c))
        if cc_emails:
            message.add_cc(cc_emails)
    try:
        sg = SendGridAPIClient(apikey)
        response = sg.send(message)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(str(e))
        return False


def send_mail_with_attachemnt(toEmail, emailSubject, emailTemplate, attachment_location, name_of_attachment, cc=[]):
    message = Mail(
        from_email=fromMail,
        to_emails=toEmail,
        subject=emailSubject,
        html_content=emailTemplate
    )
    # Mail Attachement
    with open(attachment_location, 'rb') as f:
        data = f.read()
        f.close()
    encoded_file = base64.b64encode(data).decode()

    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName('{}'.format(name_of_attachment)),
        FileType('application/pdf'),
        Disposition('attachment')
    )
    message.attachment = attachedFile
    # CC MAILS
    cc_emails = []
    # return str(message)
    if cc:
        for c in cc:
            cc_emails.append(Cc(c, c))
        if cc_emails:
            message.add_cc(cc_emails)
    try:
        sg = SendGridAPIClient(apikey)
        response = sg.send(message)
        if response.status_code == 200:
            return True
        else:
            return False
    except HTTPError as e:
        print(e.to_dict)
        # return str(e.to_dict)
    except Exception as e:
        print(str(e))
        # return str(e)
