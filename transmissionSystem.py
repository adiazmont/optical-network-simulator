import numpy as np
#import cPickle
from activeChannels import ActiveChannels

# debugging
import sys


class TransmissionSystem():
    
    def __init__(self, spectrum_band, bandwidth, grid):
        self.spectrum_band = spectrum_band
        self.bandwidth = bandwidth
        self.grid = grid
        self.activeChannels = ActiveChannels()
        
    def db_to_abs(self, value):
        absolute_value = 10**(value/float(10))
        return absolute_value
        
    def abs_to_db(self,  value):
        dB_value = 10*np.log10(value)
        return dB_value
        
    def monitor(self, link, span, channel):
        channel_power = self.activeChannels.get_active_channel_power(link, span, channel)
        channel_noise = self.activeChannels.get_active_channel_noise(link, span, channel)
        osnr = self.abs_to_db(channel_power/channel_noise)
        return osnr

    def run(self, path, wavelength_channels, launch_power):
        # Initialize active channels data structures
        self.activeChannels.init(path)
        for channel in wavelength_channels:       
            channel = channel - 1
            input_power = self.db_to_abs(launch_power)
            input_noise = self.db_to_abs(float("-inf"))
            
            txNode = True
            # Calculate the current channel behaviour accross the 
            # path elements (nodes and links)
            for element in path:
                node = element[0]
                node_type = node.getNodeType()
                
#                print("transmissionSystem.run: computing for node: %s" %str(node_type))
                
                # Check if node is the Rx node
                if node_type is 2:
                    break
                else:
                    # Calculate impairments of the node
                    node_attenuation = self.db_to_abs(node.getNodeAttenuation())
                    input_power = input_power / node_attenuation
                    input_noise = input_noise / node_attenuation
                    
                    node_amplifier = node.getAmplifier()
                    if node_amplifier is not None:
                        amplifierWavelengthDependentGain = self.db_to_abs(node_amplifier.getWavelengthDependentGain(channel))
                        amplifierTargetGain = self.db_to_abs(node_amplifier.getTargetGain())
                        amplifierNoiseFigure = self.db_to_abs(node_amplifier.getNoiseFigure())
                            
                        # The signal (and noise) traversing the first span already 
                        # perceived the impairments of the first node
                        input_power, input_noise = self.activeChannels.output_power_noise(input_power, input_noise, channel, 
                                                                                                                                    amplifierTargetGain, amplifierWavelengthDependentGain, 
                                                                                                                                    amplifierNoiseFigure, self.bandwidth, self.grid)
                                                                                                                                    
                        # insert "new" channel-power_level relation to active_channels.
                        if txNode:
                            self.activeChannels.set_active_channel_original(0, 0, channel, input_power, input_noise, amplifierWavelengthDependentGain)
                            self.activeChannels.set_active_channel_nonlinear(0, 0, channel, input_power, input_noise, amplifierWavelengthDependentGain)
                            txNode = False
                    
                    link = element[1]
                    link_spans = link.getSpans()
                    # Links are composed of fibre spans and amplifiers.
                    # Iterate through the link elements and compute the
                    # impairments raised by each
                    for span_object in link_spans:
                        span = span_object[0]
                        span_amplifier = span_object[1]
                        
                        fibreAttenuation = self.db_to_abs(span.getFibreAttenuation() * span.getFibreSpanLength())
                        input_power = input_power / float(fibreAttenuation)
                        input_noise= input_noise / float(fibreAttenuation)
                        
                        # It is not mandatory for spans to have amplifiers.
                        # If there is an amplifier, there is an output signal to compute.
                        # Otherwise, input power is the main value (to not register, though).
                        if span_amplifier is not None:
                            amplifierWavelengthDependentGain = self.db_to_abs(span_amplifier.getWavelengthDependentGain(channel))
                            amplifierTargetGain = self.db_to_abs(span_amplifier.getTargetGain())
                            amplifierNoiseFigure = self.db_to_abs(span_amplifier.getNoiseFigure())

                            output_power, output_noise = self.activeChannels.output_power_noise(input_power, input_noise, channel, amplifierTargetGain, amplifierWavelengthDependentGain, amplifierNoiseFigure, self.bandwidth, self.grid)
                            
                            # insert "new" channel-power_level relation to active_channels.
                            self.activeChannels.set_active_channel_original(link, span, channel, output_power, output_noise, amplifierWavelengthDependentGain)
                            self.activeChannels.set_active_channel_nonlinear(link, span, channel, output_power, output_noise, amplifierWavelengthDependentGain)

                        for span_object in link_spans:
                            span = span_object[0]
                            # This is done at this point, because the input_power to be used
                            # for the computation of the output_power is already sharing
                            # the fibre with other channels (if any).
                            active_channels_per_span = self.activeChannels.get_active_channels_original(link, span)
                            # Check if active channels is  not single channel, or
                            # if the loop is not at the last EDFA.
                            if (len(active_channels_per_span) > 1):
                                # compute SRS impairment
                                new_active_channels_per_span = self.activeChannels.zirngibl_srs(active_channels_per_span, span.getFibreSpanLength(), span.getFibreAttenuation(), self.grid)
                                self.activeChannels.update_active_channels_nonlinear(link, span, new_active_channels_per_span)
                                # Store not normalized power and noise levels
                                # to be considered in the power excursion calculation
                                not_normalized_power,  not_normalized_noise = self.activeChannels.get_active_channels_power_noise_nonlinear(link, span)
                                # Consider channel-normalization per-span
                                self.activeChannels.normalize_channel_levels(link, span)
                                # Consider power excursion and propagation per-span
                                self.activeChannels.power_excursion_propagation(link, span, not_normalized_power, not_normalized_noise)
                                
                        input_power = output_power
                        input_noise = output_noise
        return 1
################################### END CHANNEL LOADING SEQUENCE PROCESS ######################################
#        output_file = cs.ROOT_DIR + 'data-files/'+str(self.thread_id)+'-'+str(channel_to_load)+'.pkl'
#        output = open(output_file,  'wb')
#        cPickle.dump(self.pe_obj.active_channels_per_link_nonlinear,  output)
#        output.close()
#################################### CHANNEL REMOVING SEQUENCE PROCESS ######################################
#        for channel in self.dc.CHANNEL_REMOVING:
#            channel = channel - 1
#            for node in range(self.node_no):
#                link_id = node # Temporal variable
#                if node is self.node_no-1:
#                    link_id = node-1# Temporal variable
#                    span = -1
#                    self.pe_obj.remove_active_channel_original(link_id, span, channel)
#                    self.pe_obj.remove_active_channel_nonlinear(link_id, span, channel)
#                    break
#                else:
#                    for span in range(self.amplifier_no):
#                        self.pe_obj.remove_active_channel_original(link_id, span, channel)
#                        self.pe_obj.remove_active_channel_nonlinear(link_id, span, channel)
#                    
#                for span in range(self.amplifier_no):
#                            # This is done at this point, because the input_power to be used
#                            # for the computation of the output_power is already sharing
#                            # the fibre with other channels (if any).
#                            active_channels_per_span = self.pe_obj.get_active_channels_original(link_id, span)
#                            # Check if active channels is  not single channel, or
#                            # if the loop is not at the last EDFA.
#                            if ((len(active_channels_per_span) > 1)  and (span is not 0)):
#                                # compute SRS impairment
#                                new_active_channels_per_span = self.pe_obj.zirngibl_srs(active_channels_per_span, self.dc.FIBRE_SPAN)
#                                self.pe_obj.update_active_channels_nonlinear(link_id, span, new_active_channels_per_span)
#                                # Store not normalized power and noise levels
#                                # to be considered in the power excursion calculation
#                                not_normalized_power,  not_normalized_noise = self.pe_obj.get_active_channels_power_noise_nonlinear(link_id, span)
#                                # Consider channel-normalization per-span
#                                self.pe_obj.normalize_channel_levels(link_id, span)
#        #                        # Consider power excursion and propagation per-span
#                                self.pe_obj.power_excursion_propagation(link_id,  span,  not_normalized_power,  not_normalized_noise)
#################################### END CHANNEL REMOVING SEQUENCE PROCESS ######################################
#
#        output_file = '/home/alan/Trinity-College/Research/NEXT_PUBLICATION/experiments/offline-data-gen/data-files/47'+str(self.thread_id)+'.pkl'
#        output = open(output_file,  'wb')
#        cPickle.dump(self.pe_obj.active_channels_per_link_nonlinear,  output)
#        output.close()
#
#################################### CHANNEL REMOVING SEQUENCE PROCESS - ONE CHANNEL######################################
#        channel = 4 # Index 5
#        for node in range(self.node_no):
#            link_id = node # Temporal variable
#            if node is self.node_no-1:
#                link_id = node-1# Temporal variable
#                span = -1
#                self.pe_obj.remove_active_channel_original(link_id, span, channel)
#                self.pe_obj.remove_active_channel_nonlinear(link_id, span, channel)
#                break
#            else:
#                for span in range(self.amplifier_no):
#                    self.pe_obj.remove_active_channel_original(link_id, span, channel)
#                    self.pe_obj.remove_active_channel_nonlinear(link_id, span, channel)
#                
#            for span in range(self.amplifier_no):
#                # This is done at this point, because the input_power to be used
#                # for the computation of the output_power is already sharing
#                # the fibre with other channels (if any).
#                active_channels_per_span = self.pe_obj.get_active_channels_original(link_id, span)
#                # Check if active channels is  not single channel, or
#                # if the loop is not at the last EDFA.
#                if ((len(active_channels_per_span) > 1)  and (span is not 0)):
#                    # compute SRS impairment
#                    new_active_channels_per_span = self.pe_obj.zirngibl_srs(active_channels_per_span, self.dc.FIBRE_SPAN)
#                    self.pe_obj.update_active_channels_nonlinear(link_id, span, new_active_channels_per_span)
#                    # Store not normalized power and noise levels
#                    # to be considered in the power excursion calculation
#                    not_normalized_power,  not_normalized_noise = self.pe_obj.get_active_channels_power_noise_nonlinear(link_id, span)
#                    # Consider channel-normalization per-span
#                    self.pe_obj.normalize_channel_levels(link_id, span)
##                        # Consider power excursion and propagation per-span
#                    self.pe_obj.power_excursion_propagation(link_id,  span,  not_normalized_power,  not_normalized_noise)
#################################### CHANNEL REMOVING SEQUENCE PROCESS - ONE CHANNEL######################################
#
#        output_file = '/home/alan/Trinity-College/Research/NEXT_PUBLICATION/experiments/offline-data-gen/data-files/46'+str(self.thread_id)+'.pkl'
#        output = open(output_file,  'wb')
#        cPickle.dump(self.pe_obj.active_channels_per_link_nonlinear,  output)
#        output.close()
#        
#################################### CHANNEL LOADING SEQUENCE PROCESS - ONE CHANNEL ######################################
#        channel = 43
#        input_power = self.dc.TARGET_POWER / self.dc.WSS_LOSS
#        input_noise = self.dc.INPUT_NOISE / self.dc.WSS_LOSS
#        
#        for node in range(self.node_no):
#            link_id = node # Temporal variable
#            # If it is the last node
#            if node is self.node_no-1:
#                target_gain = self.compute_preamplified_gain(input_power)
#                
#                link_id = node-1# Temporal variable
#                amplifier_attenuation = 1 # one in absolute value
#                span = -1
#                
#                # MISSING SIGNAL RECONFIGURATION PROCEDURE
#                
#                output_power, output_noise = self.pe_obj.output_power_noise(input_power, input_noise, channel, target_gain, amplifier_attenuation)
#                # insert "new" channel-power_level relation to active_channels.
#                self.pe_obj.set_active_channel_original(link_id, span, channel, input_power, input_noise, amplifier_attenuation)
#                self.pe_obj.set_active_channel_nonlinear(link_id, span, channel, input_power, input_noise, amplifier_attenuation)
#                
#                osnr = float(output_power/output_noise)
#                self.osnr_arr.append(osnr)
#                break
#            else:
#                #print("Checking node: %s" %node)
#                for span in range(self.amplifier_no):
#                    ripple_function_id = self.amplifier_attenuation_funcs[span]
#                    amplifier_attenuation = self.dc.get_function_value(ripple_function_id, channel)
#                    self.debug_ripple[channel] = amplifier_attenuation
#                    if (span is 0):
#                        target_gain = self.dc.POWER_AMPLIFICATION_GAIN
#                    elif (span is self.amplifier_no-1):
#                        target_gain = self.dc.LINE_AMPLIFICATION_GAIN
#                        output_power, output_noise = self.pe_obj.output_power_noise(input_power, input_noise, channel, target_gain, amplifier_attenuation)
#                        # insert "new" channel-power_level relation to active_channels.
#                        self.pe_obj.set_active_channel_original(link_id, span, channel, output_power, output_noise, amplifier_attenuation)
#                        self.pe_obj.set_active_channel_nonlinear(link_id, span, channel, output_power, output_noise, amplifier_attenuation)
#                        input_power = output_power / self.dc.WSS_LOSS
#                        input_noise = output_noise / self.dc.WSS_LOSS
#                        break
#                    else:
#                        target_gain = self.dc.LINE_AMPLIFICATION_GAIN
#                        
#                    output_power, output_noise = self.pe_obj.output_power_noise(input_power, input_noise, channel, target_gain, amplifier_attenuation)
#
#                    # insert "new" channel-power_level relation to active_channels.
#                    self.pe_obj.set_active_channel_original(link_id, span, channel, output_power, output_noise, amplifier_attenuation)
#                    self.pe_obj.set_active_channel_nonlinear(link_id, span, channel, output_power, output_noise, amplifier_attenuation)
#                    #time.sleep(0.01)
#                    fa = self.dB_to_abs(self.dc.FIBRE_SPAN*self.dc.FIBRE_ATTENUATION)
#                    input_power = output_power / float(fa)
#                    input_noise= output_noise / float(fa)
#                    
##############################################################################################                    
#                    for span in range(self.amplifier_no):
#                        # This is done at this point, because the input_power to be used
#                        # for the computation of the output_power is already sharing
#                        # the fibre with other channels (if any).
#                        active_channels_per_span = self.pe_obj.get_active_channels_original(link_id, span)
#                        # Check if active channels is  not single channel, or
#                        # if the loop is not at the last EDFA.
#                        if ((len(active_channels_per_span) > 1)  and (span is not 0)):
#                            # compute SRS impairment
#                            new_active_channels_per_span = self.pe_obj.zirngibl_srs(active_channels_per_span, self.dc.FIBRE_SPAN)
#                            self.pe_obj.update_active_channels_nonlinear(link_id, span, new_active_channels_per_span)
#                            # Store not normalized power and noise levels
#                            # to be considered in the power excursion calculation
#                            not_normalized_power,  not_normalized_noise = self.pe_obj.get_active_channels_power_noise_nonlinear(link_id, span)
#                            # Consider channel-normalization per-span
#                            self.pe_obj.normalize_channel_levels(link_id, span)
#                            # Consider power excursion and propagation per-span
#                            self.pe_obj.power_excursion_propagation(link_id,  span,  not_normalized_power,  not_normalized_noise)
#                            #time.sleep(0.01)
##################################### END CHANNEL LOADING SEQUENCE PROCESS - ONE CHANNEL ######################################
#
#        output_file = '/home/alan/Trinity-College/Research/NEXT_PUBLICATION/experiments/offline-data-gen/data-files/47-RECON'+str(self.thread_id)+'.pkl'
#        output = open(output_file,  'wb')
#        cPickle.dump(self.pe_obj.active_channels_per_link_nonlinear,  output)
#        output.close()
#        new_ts = time.time()
#        total_time = new_ts - ts
#        print("Time required for computation of OSNR for %s channels: %s seconds." %(len(self.osnr_arr), total_time))
        #osnr_dB = [self.abs_to_dB(float(value)) for value in self.osnr_arr]
        #print(osnr_dB)
