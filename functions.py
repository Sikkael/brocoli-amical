import time

LOG = 'LOG.log'
# log function
def log(message, fn=LOG):
    # write log
    _now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(fn, 'a') as logfs:
        logfs.write('['+_now+']'+message+'\n')