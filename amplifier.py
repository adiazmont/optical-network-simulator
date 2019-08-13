description_files_dir = 'description-files/'
description_files = {'wdg1': 'wdg1.txt', 'wdg2': 'wdg2.txt'}


class Amplifier:

    def __init__(self, target_gain=18.0, noise_figure=6.0, mode=None,
                 bandwidth=12.5e9, wavelength_dependent_gain_id='wdg1'):
        """
        :param target_gain: amplifier gain in dB - float
        :param noise_figure: float
        :param mode: None or AGC - string
        :param bandwidth: amplification bandwidth - float
        :param wavelength_dependent_gain_id: file name id (see top of script) - string
        """
        self.amplifier_id = id(self)
        self.target_gain = target_gain
        self.noise_figure = noise_figure
        self.mode = mode
        self.bandwidth = bandwidth
        self.wavelength_dependent_gain = (
            self.load_wavelength_dependent_gain(wavelength_dependent_gain_id))

    @staticmethod
    def load_wavelength_dependent_gain(wavelength_dependent_gain_id):
        """
        :param wavelength_dependent_gain_id: file name id (see top of script) - string
        :return: Return wavelength dependent gain array
        """
        wdg_file = description_files[wavelength_dependent_gain_id]
        with open(description_files_dir + wdg_file, "r") as f:
            return [float(line) for line in f]
