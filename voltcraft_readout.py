#!/bin/python
import serial
import time
import matplotlib.pyplot as plt
import numpy as np
import pickle

try:
    ser = serial.Serial(port='/dev/ttyUSB1',
                        baudrate=600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_TWO,
                        bytesize=serial.SEVENBITS,
                        timeout=1,
                        rtscts=False,
                        dsrdtr=False,
                        xonxoff=False)
    ser.setRTS(False)
    ser.setDTR(True)
except serial.SerialException:
    print("kon niet verbinden")
    ser.close()
    raise SystemExit



vals = []
unit = []
mode = []
t = []
t0 = time.time()
i = 0
while True:
    try:
        ser.write("D".encode("utf-8"))
        recv = ser.read(14)
        recv = recv.decode("utf-8")
        recv = recv.split(" ")
        for i,r in reversed(list(enumerate(recv))):
            if len(r) == 0:
                del recv[i]
                
        mode.append(recv[0].strip())
        try:
            vals.append(float(recv[1]))
        except ValueError:
            vals.append(np.nan)
        unit.append(recv[-1].split())
        t.append(time.time())
        
        i = i + 1
        time.sleep(0.5)
    except KeyboardInterrupt:
        ser.close()
        break
    except serial.SerialException:
        ser.close()
        break
    except IndexError:
        print("Could not parse input. Is the DMM turned on?")
        pass

fig, ax = plt.subplots()
ax.grid()
ax.plot([tt-t0 for tt in t],vals)
ax.set_ylabel("Measurement [" + unit[0][0] + "]")
ax.set_xlabel('Time [s]')
ax.set_title("Voltcraft ME-32 readout")

if False:
    AVG_SMP = 200
    vavg = []
    for i in range(0,len(vals)-AVG_SMP,AVG_SMP):
        temp = 0
        for j in range(AVG_SMP):
            temp = temp + vals[i+j]
        vavg.append(temp/AVG_SMP)
    
    fig, ax = plt.subplots()
    ax.plot([(tt-t0)/60 for tt in [t[i] for i in range(0,len(vals)-AVG_SMP,AVG_SMP)]],vavg)
    ax.set_xlabel('Time [min.]')
    ax.set_ylabel('Voltage [V]')
    ax.set_title('Lead acid battery idle voltage decay')
    ax.grid()
    
    fig, ax = plt.subplots()
    ax.semilogx([(tt-t0)/60 for tt in [t[i] for i in range(0,len(vals)-AVG_SMP,AVG_SMP)]],vavg)
    ax.set_xlabel('Time [min.]')
    ax.set_ylabel('Voltage [V]')
    ax.set_title('Lead acid battery idle voltage decay')
    ax.grid()
    
    pickling_on = open("loodaccu.pickle","wb")
    pickle.dump({"vals":vals,"vavg":vavg,"t":t}, pickling_on)
    pickling_on.close()
