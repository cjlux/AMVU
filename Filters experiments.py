# Work about filters by FFT
# Inspired by Dominique Lefebvre's work on TangenteX.com
# 
#

# Libraries importation
from numpy import pi, sin, linspace, log10, copy, arange, hanning
from numpy.fft import rfft, rfftfreq, irfft
import matplotlib.pyplot as plt
from random import randint, random

# Constants' definitions
K = 2*pi       # Pulsation/frequency conversion
A=[0.4,0,0,0]  # Signal's amplitudes
f=[10,3,8,1]   # Signal's frequencies

# Temporal's range of acquisition
t0 = 0         # start of acquisition (s)
t1 = 2         # end of acquisition (s)

# Sampling parameters' definition
FreqEch = 4096.                 # Sampling frequency
PerEch = 1./FreqEch             # Sampling period
N = int(FreqEch*(t1 - t0))      # Number of sampling points

# Timeline
t = arange(0, N)*PerEch
dF=FreqEch/N

# Signal's definition

signal = 0
for k in range(len(A)) :
    signal += A[k]*sin(f[k]*K*t)        #Signal=Sum of sinus

# Adding noise to signal

signal=signal.copy()
for k in range(len(signal)):
    if randint(1,3)==1:             
        signal[k]+= 0.8*randint(-10,10)   #Change the coeff in order to amplify/reduce noise

signalorigin=signal.copy()

# Window's size
Sizesignal = signal.size

#Hanning (Work in progress)

OptionHanning=0                        # =1 for hanning using
# It is usefull to use this hanning window to negate signal's discontinuity.
# But is also alterate the FFT graf of the signal

if OptionHanning==1:
    hann=hanning(len(signal))          # Hanning's window construction
    signal=signal*hann
    
# Discret Fourier Transform by FFT's aglorithm
signal_FFT = abs(rfft(signal) )   # In order to keep >0 valors

# Frequential's domain recovery
signal_freq = rfftfreq(N,PerEch)   #absiss vector (0,dF,2dF,...)

#Signal ploting

plt.subplot(211)
plt.ylim(min(signal)-0.1*abs(min(signal)), max(signal)+0.1*abs(max(signal)))
plt.plot(t, signal)
plt.xlabel('Temps (s)'); plt.ylabel('Amplitude')

#Signal's specter ploting
plt.subplot(212)
plt.plot(signal_freq,signal_FFT,"o") #you can use log10(signal_FFT)
plt.vlines(signal_freq,0,signal_FFT)
plt.xlabel('Frequence (Hz)'); plt.ylabel('Amplitude')
plt.show()

#------------
#Filter choice
antibruit =1 #Noise reducing 1 / No Noise reducing 0
choix=5      #low-pass filter 1 / high-pass filter 2 / bandpass filter 3 / notch filter 4 / No filter 5
fc=8         #Filter's frequency
Deltafc=0.25   #Semi-bandwidth

valeursignal=signal_FFT.copy()
valeurfreq=signal_freq.copy()

#------------
#low-pass filter 1
if choix==1 :
    for k in range(len(valeurfreq)):
        if valeurfreq[k]>fc :   #Filter definition
            valeursignal[k]=0   #Values outside filter's range =0


#------------
#high-pass filter 2
if choix==2 :
    for k in range(len(valeurfreq)):
        if valeurfreq[k]<fc :   
            valeursignal[k]=0

#------------
#bandpass filter 3
if choix==3 :
    for k in range(len(valeurfreq)):
        if fc-Deltafc>valeurfreq[k] or valeurfreq[k]>fc+Deltafc :
            valeursignal[k]=0
            
#------------
#notch filter 4
if choix==4 :
    for k in range(len(valeurfreq)):
        if fc-Deltafc<valeurfreq[k]<fc+Deltafc :
            valeursignal[k]=0


#------------
#Anti-noise
if antibruit==1:
    Amax=0
    for k in range(len(valeursignal)) :
        if valeursignal[k]>Amax :
            Amax=valeursignal[k]         #Research of FFT's max value

    for k in range(len(valeursignal)):
        if valeursignal[k]<0.99*Amax :   
                valeursignal[k]=0


#-----------
#Frequency filter's plot
maxfreq=max(signal_FFT)

#FFT without treatments
plt.subplot(211)
plt.title('Signal et son spectre')
plt.xlim(0,max(f)+5)
plt.plot(signal_freq,signal_FFT,"o")   #log10(signal_FFT)
plt.vlines(signal_freq,0,signal_FFT)
plt.xlabel('Frequence (Hz)'); plt.ylabel('Amplitude')



#FFT after treatments
plt.subplot(212)
plt.xlim(0,max(f)+5)
plt.plot(signal_freq,valeursignal,"o") #log10(valeursignal)
plt.vlines(signal_freq,0,valeursignal)
plt.xlabel('Frequence (Hz)'); plt.ylabel('Amplitude')

plt.show()

#------------
#FFT-1              
signal=irfft(valeursignal)


#------------
#Signals' plotting
maxaff1=max(signal)
minaff1=min(signal)
maxaff2=max(signalorigin)
minaff2=min(signalorigin)
maxaff=max(maxaff1,maxaff2)
minaff=min(minaff1,minaff2)

#Signal after treatments
plt.subplot(211)
plt.ylim(minaff-0.1*abs(minaff), maxaff+0.1*abs(maxaff))
plt.plot(t, signal)
plt.xlabel('Tems (s)'); plt.ylabel('Amplitude')

#Signal before treatments
plt.subplot(212)
plt.ylim(minaff-0.1*abs(minaff), maxaff+0.1*abs(maxaff))
plt.plot(t, signalorigin)
plt.xlabel('Temps (s)'); plt.ylabel('Amplitude')
plt.show()


