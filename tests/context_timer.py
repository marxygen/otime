from otime.helpers import Timer
from time import sleep

with Timer() as t:
    sleep(3)
    print('Haha inside Timer()!')
    sleep(5)
