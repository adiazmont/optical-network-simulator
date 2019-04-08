description_files_dir = '/home/alan/Trinity-College/Research/opticalMAN/description-files/'
wdg_file_1 = "wdg1.txt"
wdg_file_2 = "wdg2.txt"

class Amplifier():
    
    def __init__(self, target_gain=18, noise_figure=6, wavelengthDependentGainId=0):
        self.amplifier_id = id(self)
        self.target_gain = target_gain
        self.noise_figure = noise_figure
        
        self.wavelengthDependentGain = self.setWavelengthDependentGain(wavelengthDependentGainId)
        
    def setWavelengthDependentGain(self, wavelengthDependentGainId):
        wavelengthDependentGain = []
        if wavelengthDependentGainId == 0:
            f = open(description_files_dir +wdg_file_1 , "r")
            for line in f.readlines():
                wavelengthDependentGain.append(float(line))
        else:
            f = open(description_files_dir + wdg_file_2, "r")
            for line in f.readlines():
                wavelengthDependentGain.append(float(line))
        return wavelengthDependentGain
    
    def getWavelengthDependentGain(self, channel):
        return self.wavelengthDependentGain[channel]
        
    def getNoiseFigure(self):
        return self.noise_figure
        
    def getTargetGain(self):
        return self.target_gain
        
