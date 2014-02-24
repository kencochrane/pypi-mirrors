from mirrorlib import find_out_of_date_mirrors
from config import MIRRORS
from notification import (update_twitter_status, send_warning_email,
                         send_status_email)


def __tweet_outofdate(mirror, last_update):
    """ Send a tweet saying we have a mirror out of date """
    status = "{0} is out of date, it was last updated {1}".format(mirror,
                                                           last_update)
    update_twitter_status(status)


def daily_out_of_date_mirror_check():
    """ run everything """
    results = find_out_of_date_mirrors(mirrors=MIRRORS)

    if results:
        email_message = ""
        for res in results:
            email_message += "{0} was last updated {1}\n".format(
                                                res.get('mirror'),
                                                res.get('time_diff_human'))

            print("{0} is out of date. {1}".format(
                    res.get('mirror'), res.get('time_diff_human')))

            # one tweet for each out of date mirror
            __tweet_outofdate(res.get('mirror'), res.get('time_diff_human'))

        # one email for all out of date mirrors
        send_warning_email(email_message)
    else:
        print("All is good, sending Good message!")
        send_status_email("[All Mirrors are up to date]")


def run():
    """ run all of the daily cron jobs."""
    daily_out_of_date_mirror_check()


if __name__ == '__main__':
    run()
