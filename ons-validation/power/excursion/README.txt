This folder contains the figures generated with the scripts.py for the
validation of the Power excursion.



i) Depicts the signal propagation of the shortest, centre, and the longest 
wavelength when it's interacting with 7, 15, 33, 63 wavelengths.
The link lengths are the same, set to 500 km separated in EDFA-compensated
spans of 100 km each.
Figure files: centre_, first_, last_wavelength.png

scripts and functions used:

scripts.py - inspect_zirngibl_srs(topo='linear', cut=1)
graphics.py - plot_power_excursion_cut(power_values, spans_length, cut)
ons system




ii) Depicts the signal propagation of the shortest, centre, and the longest 
wavelength when it's interacting with 7, 15, 33, 63 wavelengths.
The link lengths are: [100, 500, 1000, 1500, 2000, 2500, 3000], separated
in EDFA-compensated spans of 100km each. Only the power levels at the last
span are considered.
Figure files: centre_link_, first_link_, last_link_wavelength.png

scripts and functions used:

scripts.py - inspect_zirngibl_srs_max_distance(topo='linear', cut=1)
graphics.py - plot_power_excursion_cut_max_distance(power_values, distances, cut)
ons system



iii) In the folder before-edfa; depicts the signals propagation across
the spans, and the monitoring is done before the amplification procedures,
hence the power levels consider the attenuation caused by the optical fiber.



Remarks:
The excursion affecting each channel is the same for all the channels.
The impact is proportional to the travelled distance.
