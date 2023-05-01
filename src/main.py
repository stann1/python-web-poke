import sys, os
import mailSender
import requester
from threading import Timer

# usage: main.py superdoc DrDre

notified = False
REQ_INTERVAL_SECONDS = 10 * 60  # 10 minutes

def setInterval(timer, task):
    isStop = task()
    if not isStop:
        Timer(timer, setInterval, [timer, task]).start()

def perform_poke():
    global notified
    if len(sys.argv) < 3:
        print("Missing arguments for {targetplatform} and {target}")
        print(f'Usage example: main.py easydoc "Doctor Jones"')
    
    platform = sys.argv[1]
    target = sys.argv[2]
    
    res = None
    if platform == "easydoc":
        res = requester.poke_easydoc(target)
    elif platform == "superdoc":
        res = requester.poke_superdoc(target)
    else:
        raise NotImplementedError()

    if res and not notified:
        mailSender.send_mail_sendgrid(["stoychev.st2@gmail.com", "s_savek@yahoo.com"], f"{platform} crawler result", f'<strong>{res}</strong>')
        notified = True
    
    return notified

if __name__ == "__main__":
    print(f"Starting job with interval: {REQ_INTERVAL_SECONDS} sec.")
    setInterval(REQ_INTERVAL_SECONDS, perform_poke) # every X seconds, function will be called
