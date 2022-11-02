import mailSender
import requester
from threading import Timer

notified = False
REQ_INTERVAL_SECONDS = 10 * 60

def setInterval(timer, task):
    isStop = task()
    if not isStop:
        Timer(timer, setInterval, [timer, task]).start()

def perform_poke():
    global notified
    res = requester.poke_easydoc("Elka Kacarska")

    if res and not notified:
        mailSender.send_mail_sendgrid(["stoychev.st2@gmail.com", "s_savek@yahoo.com"], "Superdoc crawler result", f'<strong>{res}</strong>')
        notified = True
    
    return notified

if __name__ == "__main__":
    print(f"Starting job with interval: {REQ_INTERVAL_SECONDS} sec.")
    setInterval(REQ_INTERVAL_SECONDS, perform_poke) # every X seconds, function will be called
