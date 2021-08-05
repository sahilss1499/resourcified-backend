from django.core.mail import send_mail
from django.template.loader import render_to_string

import logging

logger = logging.getLogger('')

def sendMail(subject, message, recipient_list):
    try:
        from resourcified.local_settings import EMAIL_HOST_USER
        from_email = EMAIL_HOST_USER 
        send_mail(subject, message, from_email, recipient_list,fail_silently=True)
        logger.info("Mails sent successfully")                   
    except ImportError:
        logger.warning("Didn't find specified resource to send email")


def sendHTMLPostMail(subject, post_created_by, course_name,frontend_url, recipient_list):
    try:
        from resourcified.local_settings import EMAIL_HOST_USER
        from_email = EMAIL_HOST_USER
        msg_plain = render_to_string('email.txt', {'post_created_by': post_created_by, 'course_name': course_name, 'frontend_url': frontend_url})
        msg_html = render_to_string('email.html', {'post_created_by': post_created_by, 'course_name': course_name, 'frontend_url': frontend_url})
        send_mail(subject, msg_plain, from_email, recipient_list,html_message=msg_html,fail_silently=True)
        logger.info("Mails sent successfully")                   
    except ImportError:
        logger.warning("Didn't find specified resource to send email")