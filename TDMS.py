from nptdms import TdmsFile
import numpy as np
import matplotlib.pyplot as plt
from pylab import figure, text, scatter, show

#Reading the TDMS File
with TdmsFile.open(r"C:\The Space\USC\DR\New1.tdms") as tdms_file:
    group = tdms_file['Stream 0']
    channel = group['AI0']
    channel_data = channel[:]

#Separating the data and the tick counts  
data = [j  for i, j in enumerate(channel_data) if i%32  not in [0, 1]]
lsb = [j  for i, j in enumerate(channel_data) if i%32 == 0]
msb = [j  for i, j in enumerate(channel_data) if i%32 == 1]

#Calculating the Start time
time = []
f1l = format(int(bin(lsb[0] & 0xffff), 2), '016b')
f1m = format(int(bin(msb[0] & 0xffff), 2), '016b')
tstart = int(f1m+ f1l, 2)


#Combining the msb and lsb to get the tick counts
for i in range(1, len(lsb) - 1):
    f1l = format(int(bin(lsb[i] & 0xffff), 2), '016b')
    f1m = format(int(bin(msb[i] & 0xffff), 2), '016b')
    tick = int(f1m+ f1l, 2) - tstart
    if tick < 0:
        break
    else:
        time.append(tick)


#Interpolation between each samples
count = 0
sampled_data = []
x_samples=[]
y_samples=[]
time = time[:10000]
duty_cycle = (3200*len(time))/(15*(max(time)))


for i in  range(1, len(time)):  
    #Assumption that consecutive clock pulses will have a difference of 2
    if(abs(time[i] - time[i-1])  < 3):
        x_sample = np.linspace(time[i - 1], time[i], 30)
        y_sample = data[count: count + 30]
        count += 30
        x_samples.extend(x_sample)
        y_samples.extend(y_sample)
        sampled_data.extend(list(zip(x_sample, y_sample)))



plt.title(f'The Duty Cycle is {duty_cycle: .2f}%')                                           
plt.scatter(x_samples, y_samples)
plt.xlabel("Tick")
plt.ylabel("Waveform")
plt.show()

                                      
plt.scatter(x_samples, x_samples)
plt.xlabel("Tick")
plt.ylabel("Waveform")
plt.show()


