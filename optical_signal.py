import units as unit


class OpticalSignal:

    def __init__(self, index, channel_spacing=0.4*1e-9, launch_power=-2.0,
                 bandwidth=12.0*1e9, modulation_format="16QAM",
                 bits_per_symbol=4.0, symbol_rate=0.032*1e12):
        """
        :param index: signal index starting from 1 - int
        :param channel_spacing: channel spacing in nanometers - float
        :param launch_power: launch power in dBm - float
        :param bandwidth: channel bandwidth in GHz - float
        :param modulation_format: modulation format name - string
        :param bits_per_symbol: bits per symbol according to modulation format = float
        :param symbol_rate: symbol rate in GBaud - float
        """
        self.index = index
        self.wavelength = 1529.2 * unit.nm + index * channel_spacing
        self.frequency = unit.c / self.wavelength
        self.channel_spacing = channel_spacing
        self.launch_power = launch_power
        self.bandwidth = bandwidth
        self.modulation_format = modulation_format
        self.bits_per_symbol = bits_per_symbol
        self.symbol_rate = symbol_rate
