
import math
import numpy as np
import scipy.constants as sc
import macros as mc

class ActiveChannels():
    def __init__(self):
        # active_channels_per_link_original = {link_id: {span_id:  [{channel_id: power_level},
                                                                                    #{channel_id: noise_levels},
                                                                                    #{channel_id: amplifier_attenuation}]}}
        # Stores the values of each active channel without considering nonlinearities.
        self.active_channels_per_link_original = {}
        # Stores the values of each active channel considering nonlinearities.
        self.active_channels_per_link_nonlinear = {}

    # Calculate output power
    # Calculate output noise
    # Calculate SRS
    # Calculate Channel Levels Normalization
    # Calculate Power Excursion Propagation

    def init(self, path):
        txNode = True
        for element in path:
            if txNode:
                self.active_channels_per_link_nonlinear[0] = {}
                self.active_channels_per_link_original[0] = {}
                self.active_channels_per_link_original[0][0] = []
                self.active_channels_per_link_original[0][0].append({})
                self.active_channels_per_link_original[0][0].append({})
                self.active_channels_per_link_original[0][0].append({})
                # Constructor of nonlinear active channels structure
                self.active_channels_per_link_nonlinear[0][0] = []
                self.active_channels_per_link_nonlinear[0][0].append({}) # power levels
                self.active_channels_per_link_nonlinear[0][0].append({}) # noise levels
                self.active_channels_per_link_nonlinear[0][0].append({}) # amplifier wavelength dependent gain
                txNode = False
            node = element[0]
            node_type = node.node_type
            # Rx node to do something else (???)
            if node_type is not 'rx':
                link = element[1]
                self.active_channels_per_link_original[link] = {}
                self.active_channels_per_link_nonlinear[link] = {}
                link_spans = link.spans
                for span, _amplifier in link_spans:
                    self.active_channels_per_link_original[link][span] = []
                    self.active_channels_per_link_original[link][span].append({}) # power levels
                    self.active_channels_per_link_original[link][span].append({}) # noise levels
                    self.active_channels_per_link_original[link][span].append({}) # amplifier wavelength dependent gain
                    # Constructor of nonlinear active channels structure
                    self.active_channels_per_link_nonlinear[link][span] = []
                    self.active_channels_per_link_nonlinear[link][span].append({}) # power levels
                    self.active_channels_per_link_nonlinear[link][span].append({}) # noise levels
                    self.active_channels_per_link_nonlinear[link][span].append({}) # amplifier wavelength dependent gain

    def set_active_channel_original(self, link_id, span_id, channel, power_level,  noise_level,  amplifier_attenuation):
#        try:
        self.active_channels_per_link_original[link_id][span_id][0][channel] = power_level
        self.active_channels_per_link_original[link_id][span_id][1][channel] = noise_level
        self.active_channels_per_link_original[link_id][span_id][2][channel] = amplifier_attenuation
#        except:
#            print("activeChannels.set_active_channel_original: Unable to insert active channel: %s" %channel)

    def set_active_channel_nonlinear(self, link_id, span_id, channel, power_level,  noise_level,  amplifier_attenuation):
        try:
            self.active_channels_per_link_nonlinear[link_id][span_id][0][channel] = power_level
            self.active_channels_per_link_nonlinear[link_id][span_id][1][channel] = noise_level
            self.active_channels_per_link_nonlinear[link_id][span_id][2][channel] = amplifier_attenuation
        except:
            print("activeChannels.set_active_channel_nonlinear: Unable to insert active channel: %s" %channel)

    def get_active_channel_power(self, link_id, span_id, channel):
        return self.active_channels_per_link_nonlinear[link_id][span_id][0][channel]

    def get_active_channel_noise(self, link_id, span_id, channel):
        return self.active_channels_per_link_nonlinear[link_id][span_id][1][channel]

    def remove_active_channel_original(self,  link_id, span_id, channel):
        try:
            self.active_channels_per_link_original[link_id][span_id][0].pop(channel)
            self.active_channels_per_link_original[link_id][span_id][1].pop(channel)
            self.active_channels_per_link_original[link_id][span_id][2].pop(channel)
        except:
            print("Err: remove_active_channel_original: Unable to remove active channel: ", str(channel))

    def remove_active_channel_nonlinear(self,  link_id, span_id, channel):
        try:
            self.active_channels_per_link_nonlinear[link_id][span_id][0].pop(channel)
            self.active_channels_per_link_nonlinear[link_id][span_id][1].pop(channel)
            self.active_channels_per_link_nonlinear[link_id][span_id][2].pop(channel)
        except:
            print("Err: remove_active_channel_nonlinear: Unable to remove active channel: ", str(channel))

    def get_active_channels_original(self, link_id, span_id):
        try:
            return dict(self.active_channels_per_link_original[link_id][span_id][0])
        except:
            print('Err: get_active_channels_original: Unable to return active channels')
            return -1

    def get_active_channels_nonlinear(self, link_id, span_id):
        try:
            return dict(self.active_channels_per_link_nonlinear[link_id][span_id][0])
        except:
            print('Err: get_active_channels_nonlinear: Unable to return active channels')
            return -1

    def get_active_channels_power_noise_original(self,  link_id, span_id):
        try:
            not_normalized_power = list(self.active_channels_per_link_original[link_id][span_id][0].values())
            not_normalized_noise = list(self.active_channels_per_link_original[link_id][span_id][1].values())
            return not_normalized_power,  not_normalized_noise
        except:
            print("Err: (Class Link) get_active_channels_power_noise_original: Unable to get power and noise levels: ")

    def get_active_channels_power_noise_nonlinear(self,  link_id, span_id):
        try:
            # first substract the amplifier attenuation of each channel (previously computed)
            not_normalized_power = []
            not_normalized_noise = []
            for channel_index in self.active_channels_per_link_nonlinear[link_id][span_id][0]:
                not_normalized_power.append(self.active_channels_per_link_nonlinear[link_id][span_id][0][channel_index]/self.active_channels_per_link_nonlinear[link_id][span_id][2][channel_index])
                not_normalized_noise.append(self.active_channels_per_link_nonlinear[link_id][span_id][1][channel_index]/self.active_channels_per_link_nonlinear[link_id][span_id][2][channel_index])
            return not_normalized_power,  not_normalized_noise
        except:
            print("Err: (Class Link) get_active_channels_power_noise_nonlinear: Unable to get power and noise levels: ")

    def get_count_active_channels(self,  link_id,  span_id):
        try:
            return len(self.active_channels_per_link_original[link_id][span_id][0])
        except:
            print('Err: get_count_active_channels: Unable to return active channels')
            return -1

    def update_active_channels_nonlinear(self, link_id, span_id, active_channels_per_span):
        try:
            self.active_channels_per_link_nonlinear[link_id][span_id][0] = active_channels_per_span
        except:
            print("Err: update_active_channels_nonlinear: Unable to update active channels at span: ", span_id)

    def update_active_channels_dict_nonlinear(self,  link_id, span_id, active_channels_per_span_list,  index):
        channels = [channel for channel in sorted(self.active_channels_per_link_nonlinear[link_id][span_id][0])]
        for i in range(0, len(channels)):
            channel_key = channels[i]
            self.active_channels_per_link_nonlinear[link_id][span_id][index][channel_key] = active_channels_per_span_list[i]
        return 0

    def output_power_noise(self, input_power, input_noise, channel, target_gain, amplifierWavelengthDependentGain, amplifierNoiseFigure, bandwidth, grid):
        output_power = target_gain * input_power * amplifierWavelengthDependentGain
        output_noise = self.output_noise(input_noise, channel, amplifierWavelengthDependentGain*target_gain, amplifierNoiseFigure, bandwidth, grid)
        return output_power, output_noise

    def output_noise(self, input_noise, channel, sys_gain, amplifierNoiseFigure, bandwidth, grid):
        channel = channel + 1
        c_band_lambda = 1529.2*mc.nm+channel*grid # Starting in 1530 nm (C-band)
        out_noise = (input_noise * sys_gain) + (sc.h*(sc.speed_of_light/c_band_lambda) * sys_gain * amplifierNoiseFigure * bandwidth)

        return out_noise


    def zirngibl_srs (self, channel_powers, span_length, fibre_attenuation, grid):
		# Type channels_powers: dict - i.e. {2:-3.1, 85:-1.1}
		# Type span_length: float - i.e. 80.0
		# Return type:  dict - i.e. {2:-3.3, 85:-0.9}
        """This is a mathmatical model to estimate Stimulated Raman Scattering in SMF.
		wmo@optics.arizona.edu

		M. Zirngibl Analytical model of Raman gain effects in massive wavelength division multiplexed transmission systems, 1998.
		use Equation (10) for approximation
		Assumption 1: Raman gain shape as a triangle symmetric the central wavelength
		Assumption 2: Assume channel distribution symmetric to central wavelength
		Assumption 3: When calculating the SRS, assume equal power per-channel
		Assumption 4: SMF Aeff=80um^2, raman amplification band = 15THZ

		For more precise model, integrals need be calculated based on the input power spectrum using
		Equation (7)

		Args:
		channel_powers(dict): key->channel index, value: launch power in dBm
				       e.g., {2:-3.1, 85:-1.1}

		span_length (float) - in kilometer, e.g., 80.0

		Return type:
		channel_powers(dict): -after SRS effect, key->channel index, value: launch power in dBm
				          e.g., {2:-3.3, 85:-0.9}
		"""
        min_wavelength_index = min(channel_powers.keys())
        max_wavelength_index = max(channel_powers.keys())
        wavelength_min = 1529.2*mc.nm + (min_wavelength_index+1)*grid
        wavelength_max = 1529.2*mc.nm + (max_wavelength_index+1)*grid
        frequency_min = mc.c/(wavelength_max) #minimum frequency of longest wavelength
        frequency_max = mc.c/(wavelength_min) #maximum frequency of shortest wavelength

        alpha_dB = fibre_attenuation/mc.km; #SMF fiber attenuation in decibels/km
        alpha = 1-10**(alpha_dB/float(10)) #SMF fiber attenuation

        Lspan = span_length*mc.km #SMF span length
        Leff = (1-math.e**(-alpha*Lspan))/alpha #SMF effective distance

        P0 = 0 #Total input power calculated by following loop
        for channel, power_per_channel in channel_powers.items():
            P0 += power_per_channel*mc.mW

        #Calculate delta P for each channel
        for wavelength_index in channel_powers:  #Apply formula (10)
            wavelength = 1529.2*mc.nm + (wavelength_index+1)*grid
            frequency = mc.c/wavelength #Frequency of the wavelength of interest
            R1 = mc.beta*P0*Leff*(frequency_max-frequency_min)*math.e**(mc.beta*P0*Leff*(frequency_max-frequency)) #term 1
            R2 = math.e**(mc.beta*P0*Leff*(frequency_max-frequency_min))-1 #term 2

            delta_P = float(R1/R2) # Does the aritmetics in mW
            channel_powers[wavelength_index] *= delta_P

        return channel_powers

    def normalize_channel_levels(self,  link_id,  span_id):
        if span_id is -1:
            span_id = sorted(self.active_channels_per_link_nonlinear[link_id].keys())[-1] # get last span ID
        # Add amplifier attenuation of each channel

        # Calculate the main system gain of the loaded channels
        # (i.e. mean wavelength gain)
        loaded_gains_abs = self.active_channels_per_link_nonlinear[link_id][span_id][2].values()
        loaded_gains_dB = [self.abs_to_dB(x) for x in loaded_gains_abs]
        total_system_gain_dB = sum(loaded_gains_dB)
        channel_count = self.get_count_active_channels(link_id,  span_id)
        mean_system_gain_dB = total_system_gain_dB/float(channel_count)
        mean_system_gain_abs = self.dB_to_abs(mean_system_gain_dB)
        # Retrieve current power and noise levels
        power_levels = self.active_channels_per_link_nonlinear[link_id][span_id][0].values()
        noise_levels = self.active_channels_per_link_nonlinear[link_id][span_id][1].values()

        # Affect the power and noise with the mean of wavelength gain
        normalized_power = [abs(x/mean_system_gain_abs) for x in power_levels]
        normalized_noise = [abs(x/mean_system_gain_abs) for x in noise_levels]

        # Update the current power and noise levels with the "normalized" features.
        self.update_active_channels_dict_nonlinear(link_id,  span_id,  normalized_power,  0)
        self.update_active_channels_dict_nonlinear(link_id,  span_id,  normalized_noise,  1)


    def power_excursion_propagation(self, link_id,  span_id,  not_normalized_power,  not_normalized_noise):
        if span_id is -1:
            span_id = sorted(self.active_channels_per_link_nonlinear[link_id].keys())[-1] # get last span ID
        normalized_power = self.active_channels_per_link_nonlinear[link_id][span_id][0].values()
        normalized_noise = self.active_channels_per_link_nonlinear[link_id][span_id][1].values()
        # Calculate total power values given by the form: P*N
        total_power = [abs(p*n+p) for p, n in zip(normalized_power, normalized_noise)]
        total_power_old = [abs(p*n+p) for p, n in zip(not_normalized_power, not_normalized_noise)]

        # Calculate excursion
        excursion = max(p/op for p, op in zip(total_power, total_power_old))

        # Propagate power excursion
        power_excursion_prop = [p*excursion for p in total_power]  # new

        # update current power levels with the excursion propagation
        self.update_active_channels_dict_nonlinear(link_id,  span_id,  power_excursion_prop,  0) # new

    def dB_to_abs(self, value):
        absolute_value = 10**(value/10.0)
        return absolute_value

    def abs_to_dB(self, value):
        dB_value = 10*np.log10(value)
        return dB_value
