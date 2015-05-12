# Work about filters by FFT
# Inspired by Dominique Lefebvre's work on TangenteX.com
# 
#

# Libraries importation
from numpy import pi, sin, linspace, log10, copy, arange, correlate, hanning
from scipy.fftpack import fft, fftfreq, ifft, rfft, irfft, rfftfreq
import matplotlib.pyplot as plt
from random import randint, random


# Setup of csv file
csv=open("mesures.csv","w")                                        #Opening of a csv file for measurments
csv.write("Phase théorique; ")                                     #First line of csv file
csv.write("Phase mesurée; ")
csv.write("Erreur; ")
csv.write("\n")
#----------

# Constants' definitions
K = 2*pi                                                           # Pulsation/frequency conversion
A=[5,0,0,0]                                                        # Signal's amplitudes
f=[10,3,8,1]                                                       # Signal's frequencies
#----------

# Temporal's range of acquisition
t0 = 0                                                             # start of acquisition (s)
t1 = 2                                                             # end of acquisition (s)
#----------

# Sampling parameters' definition
FreqEch = 4096                                                     # Sampling frequency
PerEch = 1./FreqEch                                                # Sampling period
N = FreqEch*(t1 - t0)                                              # Number of sampling points

# Timeline
t = arange(0, N)*PerEch
FenAcq = t.size  
#----------

# Signal's definition
for k in range(900) :                                              #Variation of Phi from 0.1 to 90 in order to analyse phase shift
    Phi=(0.1*k)+0.1
    
    signal = A[0]*sin(f[0]*K*t)     
    signal2 = A[0]*sin(f[0]*K*t+Phi*pi/180)                        #Signal 2 is signal 1 +Phi phase shift
    
# Window's size
 

# Adding noise to signal
    np=0.1                                                         #Change np (noise parameter) in order to amplify/reduce the noise on signals

    signal=signal.copy()
    for k in range(len(signal)):
        if randint(1,3)==1:             
            signal[k]+= np*randint(-10,10)               

    signal2=signal2.copy()
    for k in range(len(signal)):
        if randint(1,3)==1:             
            signal2[k]+= np*randint(-10,10)  
#----------


###WIP hanning window
#fen1=hanning(len(signal))
#fen2=hanning(len(signal2))
#signal=signal*fen1
#signal2=signal2*fen2
###WIP hanning window
#----------

# Discret Fourier Transform by FFT's aglorithm
    signal_FFT = abs(rfft(signal) )                                # In order to keep >0 valors
    signal2_FFT = abs(rfft(signal2))

# Frequential's domain recovery
    signal_freq = rfftfreq(FenAcq,PerEch)
    signal2_freq = rfftfreq(FenAcq,PerEch)
#np.arrange(signal)*Deltaf( fréquence dech. *Nbr point)


#----------

# Noise filter
    antibruit = 1 #Noise reducing 1 / No Noise reducing 0

    valeursignal=signal_FFT.copy()
    valeurfreq=signal_freq.copy()
    valeursignal2=signal2_FFT.copy()
    valeurfreq=signal2_freq.copy()

    if antibruit==1:
        Amax1=0
        for k in range(len(valeursignal)) :
            if valeursignal[k]>Amax1 :
                Amax1=valeursignal[k]                             #Research of FFT's max value

        for k in range(len(valeursignal)):
            if valeursignal[k]<0.05*Amax1 :   
                    valeursignal[k]=0

        Amax2=0
        for k in range(len(valeursignal2)) :
            if valeursignal2[k]>Amax2 :
                Amax1=valeursignal2[k]                            #Research of FFT's max value

        for k in range(len(valeursignal2)):
            if valeursignal2[k]<0.05*Amax2 :   
                    valeursignal2[k]=0
#------------
                    
#FFT-1
    signal2=irfft(valeursignal2)                                  #FFT-1          
    signal=irfft(valeursignal)
#------------
    
#Phase shift measurement
    crossCorr = correlate(signal, signal2, mode='same')

    res = 360.*PerEch*f[0]


    ccMax = max(crossCorr)
    crossCorr /= ccMax
    phaseDiff = (crossCorr.argmax()-N//2)*res

    diff=format(abs(abs(Phi)-abs(phaseDiff)))
    
    print("  Phase shift sampled resolution                 : {:6.2f} degrees".format(res))
    print("  Theoretical phase shift between S1 and S2      : {:6.2f} degrees".format(Phi))

    print("  Measured Phase shift between S1 and S2         : {:6.2f} degrees".format(phaseDiff))
    print("                                           Error : {:6.2f} degrees".format(abs(abs(Phi)-abs(phaseDiff))))
    print("                                       Precision : {:6.2f} %".format(100*abs(Phi-phaseDiff)/Phi))

    csv.write(str(Phi).replace(".",",")+";")
    csv.write(str(phaseDiff).replace(".",",")+";")
    csv.write(str(diff).replace(".",",")+";")
    csv.write("\n")



csv.close()
