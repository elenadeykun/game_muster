from django.core.mail import EmailMessage


def split(array, part_length):
    return [array[i:i + part_length] for i in range(0, len(array), part_length)]


def send_mail(email, mail_subject, message):
    to_email = email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()

