from django.core.mail import send_mail
import logging
logger = logging.getLogger('')

def sendMail(subject, message, recipient_list):
    try:
        from resourcified.local_settings import HOST_EMAIL
        from_email = HOST_EMAIL 
        send_mail(subject, message, from_email, recipient_list,fail_silently=True)
        logger.info("Mails sent successfully")                   
    except ImportError:
        logger.warning("Didn't find specified resource to send email")
    