import math
import numpy as np
import scipy.constants as sc
import units as unit


def db_to_abs(db_value):
    """
    :param db_value: list or float
    :return: Convert dB to absolute value
    """
    absolute_value = 10**(db_value/float(10))
    return absolute_value


def abs_to_db(absolute_value):
    """
    :param absolute_value: list or float
    :return: Convert absolute value to dB
    """
    db_value = 10*np.log10(absolute_value)
    return db_value


class TransmissionSystem(object):

    def __init__(self):

        # active_channels =
        # {link_id:
        #   {span_id: [
        #       {channel_id: power_level},
        #       {channel_id: noise_levels},
        #       {channel_id: amplifier_attenuation}]
        #   }
        # }
        # Stores the values of each active channel without considering nonlinearities.
        self.active_channels = {}  # TO BE REMOVED
        self.input_power = {}
        self.output_power = {}
        self.amplified_spontaneous_emission_noise = {}
        self.nonlinear_interference_noise = {}
        
    def init_interfaces(self, links):

        for link in links:
            self.active_channels[link] = {}
            self.input_power[link] = {}
            self.output_power[link] = {}
            self.amplified_spontaneous_emission_noise[link] = {}
            self.nonlinear_interference_noise[link] = {}
            spans = link.spans
            for span, _amplifier in spans:
                self.active_channels[link][span] = {"power": {}, "ase_noise": {}, "nli_noise": {}, "wdg": {}}
                self.input_power[link][span] = {}
                self.output_power[link][span] = {}
                self.amplified_spontaneous_emission_noise[link][span] = {}
                self.nonlinear_interference_noise[link][span] = {}

    # GETTERS TO BE REMOVED
    def get_active_channel_power(self, link_id, span_id, channel):
        return self.active_channels[link_id][span_id]["power"][channel]

    def get_active_channel_ase_noise(self, link_id, span_id, channel):
        return self.active_channels[link_id][span_id]["ase_noise"][channel]

    def get_active_channel_nli_noise(self, link_id, span_id, channel):
        return self.active_channels[link_id][span_id]["nli_noise"][channel]

    def propagate(self, path, signals):
        """

        :param path: list of Span tuples (span, amplifier)
        :param signals: list of signals in transmission - list[Signal(),]
        :return: Run transmission system, returning True on success
        """

        input_power = {}
        output_power = {}
        signal_power_nonlinear = {}
        amplified_spontaneous_emission_noise = {}
        nonlinear_interference_noise = {}
        wdg = {}
        for signal in signals:
            signal_index = signal.index
            input_power[signal_index] = db_to_abs(signal.launch_power)
            output_power[signal_index] = db_to_abs(signal.launch_power)
            nonlinear_interference_noise[signal_index] = db_to_abs(0.0)

        # get last node in path (Rx)
        rx_node = path[-1][0]
        # Calculate the current signal behaviour across the
        # path elements (nodes and links)
        for node, link in path:
            # If we are at the Rx node, then we are done with this path
            if node == rx_node:
                break
            else:
                # Calculate impairments of the node and its compensation
                node_attenuation = db_to_abs(node.attenuation())
                node_amplifier = node.amplifier
                previous_amplifier = node_amplifier

                for signal in signals:
                    signal_index = signal.index
                    signal_frequency = signal.frequency
                    signal_launch_power = signal.launch_power  # MAYBE TO BE REMOVED
                    signal_power = output_power[signal_index]
                    # Needed for computation of nonlinear interference noise
                    signal_power_nonlinear[signal_index] = output_power[signal_index]

                    signal_power = signal_power / node_attenuation

                    if node_amplifier:
                        amplifier_target_gain = node_amplifier.target_gain
                        amplifier_noise_figure = node_amplifier.noise_figure
                        amplifier_mode = node_amplifier.mode
                        amplifier_bandwidth = node_amplifier.bandwidth
                        amplifier_wavelength_dependent_gain = node_amplifier.wavelength_dependent_gain[signal_index]

                        signal_noise = self.stage_amplified_spontaneous_emission_noise(
                            signal_frequency, amplifier_target_gain, amplifier_wavelength_dependent_gain,
                            amplifier_noise_figure, amplifier_bandwidth)
                        amplified_spontaneous_emission_noise[signal_index] = signal_noise

                        # Output signal power levels after amplification
                        signal_power = self.output_amplified_power(
                            signal_power, amplifier_target_gain, amplifier_mode,
                            signal_launch_power, amplifier_wavelength_dependent_gain)

                    # Signal performance after node
                    # Output power levels after amplification
                    output_power[signal_index] = signal_power

                # Links are composed of fibre spans and amplifiers.
                # Iterate through the link elements and compute the
                # impairments raised by each
                for span, amplifier in link.spans:
                    # Retrieve linear degradation effects due to the optical fiber
                    fibre_attenuation = db_to_abs(span.fibre_attenuation * span.length)

                    for signal in signals:
                        # Compute linear effects
                        signal_index = signal.index
                        signal_power = output_power[signal_index]

                        signal_power = signal_power / fibre_attenuation
                        # dispersion requires revision
                        # dispersion = self.dispersion(signal, span)
                        # signal_power = signal_power / dispersion

                        # Signal performance at the end of span
                        # considering linear effects
                        input_power[signal_index] = signal_power
                        if amplifier:
                            wdg[signal_index] = amplifier.wavelength_dependent_gain[signal_index]

                    # Check if active channels is  not single channel, or
                    # if the loop is not at the last EDFA.
                    if len(input_power) > 1:
                        # Compute nonlinear effects
                        # compute SRS impairment
                        input_power = self.zirngibl_srs(signals,
                                                        input_power,
                                                        span)

                        if amplifier:
                            # Store not normalized power and noise levels
                            # to be considered in the power excursion calculation
                            not_normalized_power = input_power
                            not_normalized_noise = amplified_spontaneous_emission_noise

                            normalized_power, normalized_noise = self.normalize_channel_levels(
                                input_power,
                                amplified_spontaneous_emission_noise,
                                wdg)
                            # Consider power excursion and propagation per-span
                            input_power = self.power_excursion_propagation(
                                normalized_power, normalized_noise,
                                not_normalized_power, not_normalized_noise)

                    if len(input_power) > 2:
                        # Compute nonlinear interference noise, passing the node_amplifier
                        # because its amplification gain impacts negatively the nonlinear
                        # interference.
                        if amplifier:
                            nonlinear_interference_noise = self.output_nonlinear_noise(
                                signals,
                                nonlinear_interference_noise,
                                signal_power_nonlinear,
                                span,
                                node_amplifier)
                            self.nonlinear_interference_noise[link][span] = nonlinear_interference_noise

                    for signal in signals:
                        # Compute linear effects
                        signal_index = signal.index
                        signal_frequency = signal.frequency
                        signal_launch_power = signal.launch_power
                        signal_power = input_power[signal_index]

                        self.input_power[link][span][signal_index] = signal_power * unit.mW

                        if amplifier:
                            amplifier_target_gain = amplifier.target_gain
                            amplifier_previous_gain = previous_amplifier.target_gain
                            amplifier_noise_figure = amplifier.noise_figure
                            amplifier_mode = amplifier.mode
                            amplifier_bandwidth = node_amplifier.bandwidth
                            amplifier_wavelength_dependent_gain = amplifier.wavelength_dependent_gain[signal_index]
                            amplifier_previous_wavelength_dependent_gain = \
                                previous_amplifier.wavelength_dependent_gain[signal_index]

                            signal_noise = self.stage_amplified_spontaneous_emission_noise(
                                signal_frequency, amplifier_previous_gain, amplifier_previous_wavelength_dependent_gain,
                                amplifier_noise_figure, amplifier_bandwidth)
                            self.amplified_spontaneous_emission_noise[link][span][signal_index] = signal_noise

                            # Output signal power levels after amplification
                            signal_power = self.output_amplified_power(
                                signal_power, amplifier_target_gain, amplifier_mode,
                                signal_launch_power, amplifier_wavelength_dependent_gain)

                            previous_amplifier = amplifier

                        # Output power levels after amplification
                        self.output_power[link][span][signal_index] = signal_power

    @staticmethod
    def dispersion(signal, span):
        symbol_rate = signal.symbol_rate
        bits_per_symbol = signal.bits_per_symbol
        gross_bit_rate = symbol_rate * np.log2(bits_per_symbol)
        bandwidth_nm = unit.c / signal.bandwidth
        dispersion = -(2 * unit.pi * unit.c/signal.wavelength**2) * span.dispersion_coefficient
        dispersion_penalty = 5 * np.log10(1 + (4 * bandwidth_nm*unit.nm * gross_bit_rate * span.length * dispersion)**2)
        dispersion_penalty_abs = db_to_abs(dispersion_penalty)
        return dispersion_penalty_abs

    @staticmethod
    def output_amplified_power(signal_power, target_gain, mode, launch_power, amplifier_wavelength_dependent_gain):
        """
        :param signal_power: units: mW - float
        :param target_gain: units mW (absolute value) - float
        :param mode: amplifier mode - string
        :param launch_power: units: mW, only used if mode=AGC - float
        :param amplifier_wavelength_dependent_gain: units: mW - float
        :param amplifier_wavelength_dependent_gain: units: mW - float
        :return: amplification-compensated power levels - float
        """
        if mode == 'AGC':
            # Adjust the gain to keep signal power constant
            target_gain = db_to_abs(abs(abs_to_db(signal_power)-launch_power))
        # Conversion from dB to linear
        target_gain_linear = db_to_abs(target_gain)
        wavelength_dependent_gain_linear = db_to_abs(amplifier_wavelength_dependent_gain)
        return signal_power * target_gain_linear * wavelength_dependent_gain_linear

    @staticmethod
    def stage_amplified_spontaneous_emission_noise(signal_frequency, amplifier_target_gain,
                                                   amplifier_wavelength_dependent_gain,
                                                   amplifier_noise_figure, amplifier_bandwidth):
        """
        :param signal_frequency: units: THz
        :param amplifier_target_gain: units: dB
        :param amplifier_wavelength_dependent_gain: units: dB
        :param amplifier_noise_figure: units: dB
        :param amplifier_bandwidth: units: GHz
        :return: ASE noise in linear form
        Ch.5 Eqs. 4-16,18 in: Gumaste A, Antony T. DWDM network designs and engineering solutions. Cisco Press; 2003.
        """

        # Compute parameters needed for ASE model
        population_inversion = 0.5 * 10**(amplifier_noise_figure/10.0)
        amplifier_gain = amplifier_target_gain - 1

        # Conversion from dB to linear
        gain_linear = db_to_abs(amplifier_gain)
        wavelength_dependent_gain_linear = db_to_abs(amplifier_wavelength_dependent_gain)

        # Calculation of the amplified spontaneous emission (ASE) noise.
        # Simpler formula
        # ase_noise = db_to_abs(amplifier_noise_figure) * sc.h * signal_frequency * amplifier_bandwidth
        ase_noise = 2 * population_inversion * (gain_linear * wavelength_dependent_gain_linear) * \
            sc.h * signal_frequency * amplifier_bandwidth
        return ase_noise

    def output_nonlinear_noise(self, signals, nonlinear_interference_noise,
                               signal_power_nonlinear, span, node_amplifier):
        """
        :param signals: signals interacting at given transmission - list[Signal() object]
        :param nonlinear_interference_noise: accumulated NLI noise - dict{signal_index: NLI noise levels}
        :param signal_power_nonlinear: power levels at beginning of span - dict{signal_index: power levels}
        :param span: Span() object
        :param node_amplifier: Amplifier() object at beginning of span
        :return: dict{signal_index: accumulated NLI noise levels}
        """
        node_amplifier_gain = db_to_abs(node_amplifier.target_gain)
        nonlinear_noise = self.nonlinear_noise(signals, signal_power_nonlinear, span, node_amplifier_gain)
        out_noise = {}
        for signal_index, value in nonlinear_noise.items():
            out_noise[signal_index] = nonlinear_interference_noise[signal_index] + nonlinear_noise[signal_index]
        return out_noise

    @staticmethod
    def nonlinear_noise(signals, signal_power, span, lump_gain):
        """
        Computation taken from: Poggiolini, P., et al. "Accurate Non-Linearity Fully-Closed-Form Formula
        based on the GN/EGN Model and Large-Data-Set Fitting." Optical Fiber Communication Conference.
        Optical Society of America, 2019. Equations 1-4

        :param signals: signals interacting at given transmission - list[Signal() object]
        :param signal_power: power levels at beginning of span - dict{signal_index: power levels}
        :param span: Span() object
        :param lump_gain: EDFA target gain + wavelength dependent gain - float
        :return: Nonlinear Interference noise - dictionary{signal_index: NLI}
        """
        nonlinear_noise_struct = {}
        channels_index = sorted(signal_power.keys())
        for channel_index in channels_index:
            nonlinear_noise_struct[channel_index] = None
        channel_center = channels_index[int(math.floor(len(signal_power.keys()) / 2))]
        for signal in signals:
            if signal.index == channel_center:
                frequency_center = signal.frequency
                break

        # Retrieve fiber properties from span
        b2 = span.dispersion_coefficient
        b3 = span.dispersion_slope
        alpha = span.loss_coefficient
        gamma = span.non_linear_coefficient
        span_length = span.length

        for signal in signals:
            channel_under_test = signal.index
            frequency_cut = signal.frequency
            symbol_rate_cut = signal.symbol_rate
            bits_per_symbol_cut = signal.bits_per_symbol
            gross_bit_rate_cut = symbol_rate_cut * np.log2(bits_per_symbol_cut)
            bw_cut = gross_bit_rate_cut / (2 * np.log2(4))  # full bandwidth of the nth channel (THz).
            pwr_cut = signal_power[signal.index]
            g_cut = pwr_cut / bw_cut  # G is the flat PSD per channel power (per polarization)

            nonlinear_noise_term2 = 0

            for ch in signals:
                # omit channel under test
                if ch == channel_under_test:
                    continue

                frequency_ch = ch.frequency
                symbol_rate_ch = signal.symbol_rate
                bits_per_symbol_ch = signal.bits_per_symbol
                gross_bit_rate_ch = symbol_rate_ch * np.log2(bits_per_symbol_ch)
                bw_ch = gross_bit_rate_ch / (2 * np.log2(4))  # full bandwidth of the nth channel (THz).
                pwr_ch = signal_power[ch.index]
                g_ch = pwr_ch / bw_ch  # G is the flat PSD per channel power (per polarization)

                b2_eff_nch = b2 + unit.pi * b3 * (
                            frequency_ch + frequency_cut - 2 * frequency_center)  # FWM-factor - [1], Eq. (5)
                b2_eff_ncut = b2 + unit.pi * b3 * (
                        2 * frequency_cut - 2 * frequency_center)  # FWM-factor - [1], Eq. (6)

                nch_dividend1 = math.asinh(
                    (unit.pi ** 2 / 2) * abs(b2_eff_nch / alpha) *
                    (frequency_ch - frequency_cut + (bw_ch / 2)) * bw_cut)
                nch_divisor1 = 8 * unit.pi * abs(b2_eff_nch) * alpha

                nch_dividend2 = math.asinh(
                    (unit.pi ** 2 / 2) * abs(b2_eff_nch / alpha) *
                    (frequency_ch - frequency_cut - (bw_ch / 2)) * bw_cut)
                nch_divisor2 = 8 * unit.pi * abs(b2_eff_nch) * alpha

                _nch = (nch_dividend1 / float(nch_divisor1)) - (
                            nch_dividend2 / float(nch_divisor2))  # [1], Eq. (3)

                cut_dividend = math.asinh((unit.pi ** 2 / 2) * abs(b2_eff_ncut / (2 * alpha)) * bw_cut ** 2)
                cut_divisor = 4 * unit.pi * abs(b2_eff_ncut) * alpha
                _cut = cut_dividend / float(cut_divisor)  # [1], Eq. (4)

                nonlinear_noise_term2 += (2 * g_ch ** 2 * _nch + g_cut ** 2 * _cut)

            nonlinear_noise_term1 = 16 / 27.0 * gamma ** 2 * lump_gain * math.e ** (-2 * alpha * span_length) * g_cut
            nonlinear_noise = nonlinear_noise_term1 * nonlinear_noise_term2
            nonlinear_noise_struct[channel_under_test] = nonlinear_noise
        return nonlinear_noise_struct

    @staticmethod
    def zirngibl_srs(signals, active_channels, span):
        """
        Computation taken from : M. Zirngibl Analytical model of Raman gain effects in massive
        wavelength division multiplexed transmission systems, 1998. - Equations 7,8.

        :param signals: signals interacting at given transmission - list[Signal() object]
        :param active_channels: power levels at the end of span - dict{signal_index: power levels}
        :param span: Span() object
        :return:
        """
        min_wavelength_index = 90
        max_wavelength_index = 0
        min_signal = None
        max_signal = None
        for signal in signals:
            if signal.index < min_wavelength_index:
                min_signal = signal
                min_wavelength_index = signal.index
            if signal.index > max_wavelength_index:
                max_signal = signal
                max_wavelength_index = signal.index
        frequency_min = min_signal.frequency  # minimum frequency of longest wavelength
        frequency_max = max_signal.frequency  # maximum frequency of shortest wavelength

        effective_length = span.effective_length  # SMF effective distance
        beta = span.raman_coefficient

        total_power = 0  # Total input power calculated by following loop
        for channel, power_per_channel in active_channels.items():
            total_power += power_per_channel*unit.mW

        # Calculate delta P for each channel
        for signal in signals:
            signal_index = signal.index
            frequency = signal.frequency
            r1 = beta * total_power * effective_length * (frequency_max - frequency_min) * math.e ** (
                        beta * total_power * effective_length * (frequency_max - frequency))  # term 1
            r2 = math.e ** (beta * total_power * effective_length * (frequency_max - frequency_min)) - 1  # term 2

            delta_p = float(r1/r2)  # Does the arithmetic in mW
            active_channels[signal_index] *= delta_p

        return active_channels

    @staticmethod
    def normalize_channel_levels(power_levels, noise_levels, wavelength_dependent_gains):
        """
        :param power_levels: units: mW - list[float,]
        :param noise_levels: units: linear - list[float,]
        :param wavelength_dependent_gains: units: dB list[float,]
        :return: dictionary of normalized power and noise - dict{signal_index: power/noise}
        """
        # Sum amplifier attenuation for each channel
        # Calculate the main system gain of the loaded channels
        # (i.e. mean wavelength gain)
        loaded_gains_db = wavelength_dependent_gains.values()
        total_system_gain_db = sum(loaded_gains_db)
        channel_count = len(wavelength_dependent_gains)
        mean_system_gain_db = total_system_gain_db/float(channel_count)
        mean_system_gain_abs = db_to_abs(mean_system_gain_db)

        # Affect the power and noise with the mean of wavelength gain
        normalized_power = {k: abs(x/mean_system_gain_abs) for k, x in power_levels.items()}
        normalized_noise = {k: abs(x/mean_system_gain_abs) for k, x in noise_levels.items()}

        return normalized_power, normalized_noise

    @staticmethod
    def power_excursion_propagation(normalized_power, normalized_noise,
                                    not_normalized_power, not_normalized_noise):
        """
        :param normalized_power: dict{signal_index: power - float}
        :param normalized_noise: dict{signal_index: noise - float}
        :param not_normalized_power: dict{signal_index: power - float}
        :param not_normalized_noise: dict{signal_index: noise - float}
        :return: dictionary with the power excursion propagated in the signal power levels
        """
        # Calculate total power values given by the form: P*N
        total_power = {}
        for k in normalized_power.keys():
            power = normalized_power[k]
            noise = normalized_noise[k]
            total_power[k] = abs(power * noise + power)
        total_power_old = {}
        for k in normalized_power.keys():
            power = not_normalized_power[k]
            noise = not_normalized_noise[k]
            total_power_old[k] = abs(power * noise + power)

        # Calculate excursion
        excursion = max(p/op for p, op in zip(total_power.values(), total_power_old.values()))

        # Propagate power excursion
        power_excursion_prop = {k: p*excursion for k, p in total_power.items()}  # new

        # update current power levels with the excursion propagation
        return power_excursion_prop
