description_files_dir = 'description-files/'
description_files = { 'wdg1': 'wdg1.txt', 'wdg2': 'wdg2.txt'}

class Amplifier():

    def __init__(self, target_gain=18, noise_figure=6, wavelengthDependentGainId='wdg1'):
        """target_gain: target gain in dB (18)
           noise_figure: noise figure in dB (6)
           wavelengthDependentGainId: description identifier ('wdg1')"""
        self.amplifier_id = id(self)
        self.target_gain = target_gain
        self.noise_figure = noise_figure
        self.wavelength_dependent_gain =  (
            self.loadWavelengthDependentGain(wavelengthDependentGainId))

    def loadWavelengthDependentGain(self, wavelengthDependentGainId):
        "Return wavelength dependent gain array"
        wdg_file = description_files[wavelengthDependentGainId]
        with open(description_files_dir + wdg_file, "r") as f:
            return [float(line) for line in f]
