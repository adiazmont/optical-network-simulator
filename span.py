import math
import units as unit


class Span:

    def __init__(self, length=50.0, fibre_attenuation=0.22):
        """
        :param length: optical fiber span length in km - float
        :param fibre_attenuation: optical fiber attenuation in dB - float
        """
        self.span_id = id(self)
        self.length = length * unit.km
        self.fibre_attenuation = fibre_attenuation / unit.km  # fiber attenuation in decibels/km
        self.loss_coefficient = 1 - 10 ** (self.fibre_attenuation / 10.0)
        self.effective_length = (1 - math.e ** (-self.loss_coefficient * self.length)) / self.loss_coefficient
        self.non_linear_coefficient = 1.3 / unit.km  # gamma fiber non-linearity coefficient [W^-1 km^-1]
        self.dispersion_coefficient = -21 * (unit.ps ** 2 / unit.km)  # B_2 dispersion coefficient [ps^2 km^-1]
        self.dispersion_slope = 0.1452 * (unit.ps ** 3 / unit.km)  # B_3 dispersion slope in (ps^3 km^-1)
        self.effective_area = 80 * unit.um * unit.um  # Aeff - SMF effective area
        self.raman_gain = 7.0*1e-12 * unit.cm / unit.W  # r - Raman Gain in SMF
        self.raman_amplification_band = 15 * unit.THz  # Raman amplification band ~15THz
        # Raman coefficient
        self.raman_coefficient = self.raman_gain / (2 * self.effective_area * self.raman_amplification_band)
