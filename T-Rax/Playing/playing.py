from epics import caget
import time

while True:
    print caget('13LF1:cam1:Acquire')
    print caget('13LF1:cam1:Acquire')==0
    time.sleep(0.5)