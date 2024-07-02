from email.message import EmailMessage
import ssl
import smtplib


def send_email(email_sender, email_password, email_receivers, subject, sentences):
    body = f"This is sent from Python.\n{sentences}"

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    for email_receiver in email_receivers:
        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = email_receiver
        em["Subject"] = subject
        em.set_content(body)

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
            print(f"Email sent successfully to {email_receiver}.")
        except Exception as e:
            print(f"Failed to send email to {email_receiver}. Error: {e}")


def main(subject, sentences):
    email_sender = "msci436dssproject@gmail.com"
    email_password = "yhfk sskp qprk rdcl"
    email_receivers = [
        "rodrigo.tiscareno@uwaterloo.ca",
        "m3sheng@uwaterloo.ca",
        "v238pate@uwaterloo.ca",
        "ijacob@uwaterloo.ca",
    ]

    send_email(email_sender, email_password, email_receivers, subject, sentences)


if __name__ == "__main__":
    main("", "")
