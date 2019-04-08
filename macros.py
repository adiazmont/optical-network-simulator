# DEFINITIONS FOR CLASS ACTIVE CHANNELS
# VARIABLES FOR RAMAN SCATTERING
c = 299792458.0 #Speed of light
#m = 1.0
nm = 1.0e-9 
cm = 1.0e-2
um = 1.0e-6
km = 1.0e3
THz = 1.0e12
mW = 1.0e-3
W = 1.0
#GRID = 0.4*nm; #Assume 50GHz spacing DWDM
Aeff = 80*um*um  #SMF effective area 
r = 7e-12*cm/float(W) #Raman Gain in SMF
B = 15*THz; #Raman amplification band ~15THz
beta = r/(2*Aeff*B)
