import tweepy
import smtplib

from config import load_config, EMAIL_OVERRIDE

CONFIG = load_config()

def prepare_twitter_message(status):
    """ shrink to the right size and add link to site. """
    link = "http://www.pypi-mirrors.org"
    link_len = len(link) + 4
    message_len = 140 - link_len
    status_new = status[:message_len]
    if len(status) > message_len:
        status_new += "..."
    status_new += " {0}".format(link)
    return status_new


def update_twitter_status(status):
    """ update the twitter account's status """

    consumer_key=CONFIG.get('twitter_consumer_key')
    consumer_secret=CONFIG.get('twitter_consumer_secret')

    access_token=CONFIG.get('twitter_access_key')
    access_token_secret=CONFIG.get('twitter_access_secret')

    message = prepare_twitter_message(status)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_status(message)


def send_warning_email(message):
    """ send a message saying a mirror(s) is out of date. """
    email_to = CONFIG.get('email_to')
    email_from = CONFIG.get('email_from')
    email_template = '''Subject: [pypi-mirrors] Mirror is out of Date Notice

    This is an automated email from http://www.pypi-mirrors.org to let you
    know that the following mirrors are out of date.

    {message}

    --
    This automated message is sent to you by http://www.pypi-mirrors.org If you no
    longer want to receive these emails, please contact Ken Cochrane (@KenCochrane) on twitter
    or reply to this email.
    '''
    email_body = email_template.format(message=message)

    send_email(email_body, email_to, email_from)


def send_status_email(message):
    """ send a daily status message """
    email_to = CONFIG.get('email_to_admin')
    email_from = CONFIG.get('email_from')
    email_template = '''Subject: [pypi-mirrors] Mirrors are all up to date

    This is an automated email from http://www.pypi-mirrors.org to let you
    know that the following mirrors are all up to date.

    {message}
    --
    This automated message is sent to you by http://www.pypi-mirrors.org If you no
    longer want to receive these emails, please contact Ken Cochrane (@KenCochrane) on twitter
    or reply to this email.
    '''

    email_body = email_template.format(message=message)

    send_email(email_body, email_to, email_from)


def send_email(email_body, email_to, email_from):
    """ Send an email using the configuration provided """
    email_host = CONFIG.get('email_host')
    email_port = CONFIG.get('email_port')
    email_user = CONFIG.get('email_user')
    email_password = CONFIG.get('email_password')
    email_bcc = CONFIG.get('email_bcc')

    if EMAIL_OVERRIDE:
        print 'Over-riding email with {0}.'.format(EMAIL_OVERRIDE)
        email = EMAIL_OVERRIDE
    else:
        email = email_to

    print("email to {0} , bcc: {1}; from {2}".format(email, email_bcc, email_from))
    smtp = smtplib.SMTP(email_host, email_port)
    smtp.starttls()
    smtp.login(email_user, email_password)
    smtp.sendmail(email_from, [email, email_bcc], email_body)
    smtp.quit()

    