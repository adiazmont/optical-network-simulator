import numpy as np
from activeChannels import ActiveChannels


def db_to_abs(dB_value):
    "Convert dB to absolute value"
    absolute_value = 10**(dB_value/float(10))
    return absolute_value

def abs_to_db(absolute_value):
    "Convert absolute value to dB"
    dB_value = 10*np.log10(absolute_value)
    return dB_value


class TransmissionSystem(object):

    def __init__(self, spectrum_band, bandwidth, grid):
        self.spectrum_band = spectrum_band
        self.bandwidth = bandwidth
        self.grid = grid
        self.activeChannels = ActiveChannels()

    def monitor(self, link, span, channel):
        "Return OSNR for link, span and channel"
        channel_power = self.activeChannels.get_active_channel_power(link, span, channel)
        channel_noise = self.activeChannels.get_active_channel_noise(link, span, channel)
        osnr = abs_to_db(channel_power/channel_noise)
        return osnr

    def run(self, path, wavelength_channels, launch_power):
        """Run transmission system, returning True on success
           path: list of Span tuples (span, amplifier)
           wavelength_channels: active channels
           launch_power: launch power in dB"""

        # Initialize active channels data structures
        self.activeChannels.init(path)

        # Update power and noise for every channel
        for channel in wavelength_channels:
            channel = channel - 1
            input_power = db_to_abs(launch_power)
            input_noise = db_to_abs(float("-inf"))

            txNode = True
            # Calculate the current channel behaviour across the
            # path elements (nodes and links)
            for node, link in path:
                # print("transmissionSystem.run: computing for node: %s" %str(node_type))

                # If we are at the Rx node, then we are done with this path
                if node.node_type == 'rx':
                    break
                else:
                    # Calculate impairments of the node
                    node_attenuation = db_to_abs(node.attenuation())
                    input_power = input_power / node_attenuation
                    input_noise = input_noise / node_attenuation

                    node_amplifier = node.amplifier
                    if node_amplifier:
                        amplifierWavelengthDependentGain = db_to_abs(
                            node_amplifier.wavelength_dependent_gain[channel])
                        amplifierTargetGain = db_to_abs(node_amplifier.target_gain)
                        amplifierNoiseFigure = db_to_abs(node_amplifier.noise_figure)

                        # The signal (and noise) traversing the first span already
                        # perceived the impairments of the first node
                        input_power, input_noise = self.activeChannels.output_power_noise(
                            input_power, input_noise, channel, amplifierTargetGain,
                            amplifierWavelengthDependentGain, amplifierNoiseFigure, self.bandwidth, self.grid)

                        # insert "new" channel-power_level relation to active_channels.
                        if txNode:
                            self.activeChannels.set_active_channel_original(
                                0, 0, channel, input_power, input_noise, amplifierWavelengthDependentGain)
                            self.activeChannels.set_active_channel_nonlinear(
                                0, 0, channel, input_power, input_noise, amplifierWavelengthDependentGain)
                            txNode = False

                    # Links are composed of fibre spans and amplifiers.
                    # Iterate through the link elements and compute the
                    # impairments raised by each
                    for span, amplifier in link.spans:

                        fibreAttenuation = db_to_abs(span.fibre_attenuation * span.length)
                        input_power = input_power / float(fibreAttenuation)
                        input_noise= input_noise / float(fibreAttenuation)

                        # It is not mandatory for spans to have amplifiers.
                        # If there is an amplifier, there is an output signal to compute.
                        # Otherwise, input power is the main value (to not register, though).
                        if amplifier:
                            amplifierWavelengthDependentGain = db_to_abs(
                                amplifier.wavelength_dependent_gain[channel])
                            amplifierTargetGain = db_to_abs(amplifier.target_gain)
                            amplifierNoiseFigure = db_to_abs(amplifier.noise_figure)

                            output_power, output_noise = self.activeChannels.output_power_noise(
                                input_power, input_noise, channel, amplifierTargetGain,
                                amplifierWavelengthDependentGain, amplifierNoiseFigure, self.bandwidth, self.grid)

                            # insert "new" channel-power_level relation to active_channels.
                            self.activeChannels.set_active_channel_original(
                                link, span, channel, output_power, output_noise, amplifierWavelengthDependentGain)
                            self.activeChannels.set_active_channel_nonlinear(
                                link, span, channel, output_power, output_noise, amplifierWavelengthDependentGain)

                        for span, _amplifier in link.spans:
                            # This is done at this point, because the input_power to be used
                            # for the computation of the output_power is already sharing
                            # the fibre with other channels (if any).
                            active_channels_per_span = self.activeChannels.get_active_channels_original(link, span)
                            # Check if active channels is  not single channel, or
                            # if the loop is not at the last EDFA.
                            if (len(active_channels_per_span) > 1):
                                # compute SRS impairment
                                new_active_channels_per_span = self.activeChannels.zirngibl_srs(
                                    active_channels_per_span, span.length,
                                    span.fibre_attenuation, self.grid)
                                self.activeChannels.update_active_channels_nonlinear(
                                    link, span, new_active_channels_per_span)
                                # Store not normalized power and noise levels
                                # to be considered in the power excursion calculation
                                not_normalized_power, not_normalized_noise = (
                                    self.activeChannels.get_active_channels_power_noise_nonlinear(link, span))
                                # Consider channel-normalization per-span
                                self.activeChannels.normalize_channel_levels(link, span)
                                # Consider power excursion and propagation per-span
                                self.activeChannels.power_excursion_propagation(
                                    link, span, not_normalized_power, not_normalized_noise)

                        input_power = output_power
                        input_noise = output_noise
        return True
