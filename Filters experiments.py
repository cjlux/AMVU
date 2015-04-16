# Work about filters by FFT
# Inspired by Dominique Lefebvre's work on TangenteX.com
# 
#

# Libraries importation
from numpy import pi, sin, linspace, log10, copy
from scipy.fftpack import fft, fftfreq, ifft, rfft, irfft, rfftfreq
import matplotlib.pyplot as plt
from random import randint, random

# Constants' definitions
K = 2*pi       # Pulsation/frequency conversion
A=[5,20,2,10]  # Signal's amplitudes
f=[10,3,8,1]   # Signal's frequencies

# Temporal's range of acquisition
t0 = 0         # start of acquisition (s)
t1 = 2         # end of acquisition (s)

# Sampling parameters' definition
FreqEch = 4096                  # Sampling frequency
PerEch = 1./FreqEch             # Sampling period
N = FreqEch*(t1 - t0)           # Number of sampling points

# Timeline
t = linspace(t0, t1, N)

# Signal's definition

signal = 0
signal2 = 0
for k in range(len(A)) :
    signal += A[k]*sin(f[k]*K*t)        #Signal=Sum of sinus

# Adding noise to signal

signal=signal.copy()
for k in range(len(signal)):
    if randint(1,3)==1:             
        signal[k]+= 0.5*randint(-10,10)   #Change "0.5" in order to amplify/reduce noise
signal2=signal.copy()

    
# Window's size
FenAcq = signal.size            
    
# Discret Fourier Transform by FFT's aglorithm
signal_FFT = abs(rfft(signal) )   # In order to keep >0 valors
signal2_FFT = abs(rfft(signal2))

# Frequential's domain recovery
signal_freq = rfftfreq(FenAcq,PerEch)
signal2_freq = rfftfreq(FenAcq,PerEch)
#np.arrange(signal)*Deltaf( fréquence dech. *Nbr point)


#Signal ploting
plt.subplot(211)
plt.title('Signal et son spectre')
plt.ylim(min(signal)-5, max(signal)+5)
plt.plot(t, signal)
plt.plot(t, signal2)
plt.xlabel('Temps (s)'); plt.ylabel('Amplitude')


### IN WORK###
#Signal's specter ploting
plt.subplot(212)
plt.xlim(0,max(f)+5) 
plt.plot(signal_freq,signal_FFT,".-") #a mettre log10 pour voir en hauteur
#plt.plot(signal2_freq,log10(signal2_FFT),"o")
#tracer le premier en point puis chopper les coordonnés des deux point et tracer en -
#[fy,0] [0,yi] ou voir dans matplotlib
plt.xlabel('Frequence (Hz)'); plt.ylabel('Amplitude')
#plt.title('Signal et son spectre')
plt.show()
#######

#------------
#Filter choice
antibruit = 1 #Noise reducing 1 / No Noise reducing 0
choix=2       #low-pass filter 1 / high-pass filter 2 / bandpass filter 3 / notch filter 4 / No filter 5
fc=3          #Filter's frequency
Deltafc=0.5   #Semi-bandwidth

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
        if valeursignal[k]<0.05*Amax :   
                valeursignal[k]=0


#-----------
#Frequency filter's plot

#FFT without treatments
plt.subplot(211)
plt.title('Signal et son spectre')
plt.xlim(0,max(f)+5)
plt.plot(signal_freq,signal_FFT)
plt.xlabel('Temps (s)'); plt.ylabel('Amplitude')
#FFT after treatments
plt.subplot(212)
plt.xlim(0,max(f)+5)
plt.plot(signal_freq,valeursignal)
plt.xlabel('Frequence (Hz)'); plt.ylabel('Amplitude')
plt.show()

#------------
#FFT-1
signal2=irfft(signal2_FFT)   #Les deux à mettres en comms.            
signal=irfft(valeursignal)


#------------
#Signals' plotting

#Signal after treatments
plt.subplot(211)
#plt.title('Signal débruité')
plt.ylim(min(signal)-5, max(signal)+5)
plt.plot(t, signal)
#plt.xlabel('Temps (s)'); plt.ylabel('Amplitude')

#Signal before treatments
plt.subplot(212)
#plt.title('Signal initial')
plt.ylim(min(signal2)-5, max(signal2)+5)
plt.plot(t, signal2)
#plt.xlabel('Temps (s)'); plt.ylabel('Amplitude')
plt.show()


