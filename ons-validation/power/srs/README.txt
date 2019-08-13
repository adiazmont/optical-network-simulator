This folder contains the figures generated with the scripts.py for the
validation of the Stimulated Raman Scattering from Zirgnbl 1998.



i) Depicts the signal propagation of the shortest, centre, and the longest 
wavelength when it's interacting with 7, 15, 33, 63 wavelengths.
The link lengths are the same, set to 500 km separated in EDFA-compensated
spans of 100 km each.
Figure files: centre_, first_, last_wavelength.png

scripts and functions used:

scripts.py - inspect_zirngibl_srs(topo='linear', cut=1)
graphics.py - plot_power_srs_cut(power_values, spans_length, cut)
ons system




ii) Depicts the signal propagation of the shortest, centre, and the longest 
wavelength when it's interacting with 7, 15, 33, 63 wavelengths.
The link lengths are: [100, 500, 1000, 1500, 2000, 2500, 3000], separated
in EDFA-compensated spans of 100km each. Only the power levels at the last
span are considered.
Figure files: centre_link_, first_link_, last_link_wavelength.png

scripts and functions used:

scripts.py - inspect_zirngibl_srs_max_distance(topo='linear', cut=1)
graphics.py - plot_power_srs_cut_max_distance(power_values, distances, cut)
ons system



iii) In the folder before-edfa; depicts the signals propagation across
the spans, and the monitoring is done before the amplification procedures,
hence the power levels consider the attenuation caused by the optical fiber.



Remarks:
Without the ideal AGC-EDFA it is not possible to compute extremely-long
links, varied and limited to the launch power used. The lower the power
levels the longer the reach possible to be computed. Otherwise the results
are too long numbers that Python cannot handle by default (i.e., inf, NaN).
From Zirngibl98', in a single span system with 80km and 80 channels, the
losses increase with higher power levels. Specifically from his findings:
1mW launch power leads to -0.65 dB and 0.62 dB losses for the shortest and
longest wavelengths, respectively. For 4mW --> -2.8 dB and 2.3 dB.
From the book pg. 333 ; "in order to keep the penalty below 0.5 dB, we must
have the power per channel < 0.1.
