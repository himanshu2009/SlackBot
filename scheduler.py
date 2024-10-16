from apscheduler.schedulers.blocking import BlockingScheduler
from get_new_vulnerabilities import get_cves
from send_to_slack import send_message_to_admin

def check_for_vulnerabilities():
    vulnerabilities = get_cves()
    print(vulnerabilities)
    if vulnerabilities:
        send_message_to_admin(vulnerabilities)
    else:
        print('No new vulnerabilties to show')


scheduler = BlockingScheduler()
scheduler.add_job(check_for_vulnerabilities, 'interval', minutes=2)
