import matplotlib.pyplot as plt


class Graphic:

    @staticmethod
    def plot_osnr_increment(osnr_values, spans_length):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        plt.plot(osnr_values, color='y', marker='o')
        for i, j in zip(range(len(osnr_values)), osnr_values):
            ax.annotate(str(round(j, 2)), xy=(i, j), xytext=(2, 2), textcoords='offset points')

        mock = [19.7, 18.2, 16.4, 15.5, 13.5]
        mock2 = [11.5, 10.4, 7.5, 5.9, 4]
        plt.plot(mock, color='r', marker='*')
        plt.plot(mock2, color='b', marker='*')
        plt.ylabel("OSNR-ASE (dB)")
        plt.xlabel(
            "# of spans (length of each span: %s, unit: km; total distance: %s km)" % (spans_length, sum(spans_length)))
        plt.title("Signal degradation with # of span")
        plt.grid(True)
        plt.show()

    """
    The following functions are defined for validation purposes.
    """
    @staticmethod
    def plot_noise(noise_values, spans_length):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        plt.plot(noise_values, color='y', marker='o')
        for i, j in zip(range(len(noise_values)), noise_values):
            ax.annotate(str(round(j, 2)), xy=(i, j), xytext=(-10, -10), textcoords='offset points')
        plt.ylabel("ASE Noise (dB)")
        plt.xlabel(
            "# of spans (length of each span: %s, unit: km; total distance: %s km)" % (spans_length, sum(spans_length)))
        plt.title("Signal degradation with # of span")
        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_power(power_values, spans_length):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        plt.plot(power_values, color='y', marker='o')
        for i, j in zip(range(len(power_values)), power_values):
            ax.annotate(str(round(j, 2)), xy=(i, j), xytext=(-10, -10), textcoords='offset points')
        plt.ylabel("Power levels (dBm)")
        plt.xlabel(
            "# of spans (length of each span: %s, unit: km; total distance: %s km)" % (spans_length, sum(spans_length)))
        plt.title("Signal degradation with # of span")
        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_dict_power_levels(power_values, spans_length):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.tick_params(width=0.2)
        labels = {0: 8, 1: 16, 2: 32, 3: 64}
        colors = {0: 'y', 1: 'b', 2: 'r', 3: 'g'}
        for key, power_value in power_values.items():
            label = str(labels[key]) + ' wavelengths'
            plt.plot(power_value, label=label, color=colors[key], marker='o')
        ax.legend(loc=2)
        plt.ylabel("Power levels (dBm)")
        plt.xlabel(
            "# of spans (length of each span: %s, unit: km; total distance: %s km)" % (spans_length[0][0],
                                                                                       sum(spans_length[0])))
        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_dict_noise_levels(noise_values, spans_length):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.tick_params(width=0.2)
        labels = {0: 8, 1: 16, 2: 32, 3: 64}
        colors = {0: 'y', 1: 'b', 2: 'r', 3: 'g'}
        for key, noise_value in noise_values.items():
            label = str(labels[key]) + ' wavelengths'
            plt.plot(noise_value, label=label, color=colors[key], marker='o')
        ax.legend(loc=2)
        plt.ylabel("Noise levels (dB)")
        plt.xlabel(
            "# of spans (length of each span: %s, unit: km; total distance: %s km)" % (spans_length[0][0],
                                                                                       sum(spans_length[0])))
        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_dict_power_levels_distance(power_values, distances):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.tick_params(width=0.2)
        labels = {0: 8, 1: 16, 2: 32, 3: 64}
        colors = {0: 'y', 1: 'b', 2: 'r', 3: 'g'}
        for key, power_value in power_values.items():
            label = str(labels[key]) + ' wavelengths'
            plt.plot(distances, power_value, label=label, color=colors[key], marker='o')
        ax.legend(loc=3)
        plt.ylabel("Power levels (dBm)")
        plt.xlabel("Link length (km)")
        plt.title("Signal-1529.6 nm propagation with # of spans")
        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_dict_noise_levels_distance(noise_values, distances):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.tick_params(width=0.2)
        labels = {0: 8, 1: 16, 2: 32, 3: 64}
        colors = {0: 'y', 1: 'b', 2: 'r', 3: 'g'}
        for key, noise_value in noise_values.items():
            label = str(labels[key]) + ' wavelengths'
            plt.plot(distances, noise_value, label=label, color=colors[key], marker='o')
        ax.legend(loc=4)
        plt.ylabel("Noise levels (dB)")
        plt.xlabel("Link length (km)")
        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_osnr(osnr_values, spans_length, osnr_type):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.tick_params(width=0.2)
        labels = {0: 8, 1: 16, 2: 32, 3: 64}
        colors = {0: 'y', 1: 'b', 2: 'r', 3: 'g'}
        for key, noise_value in osnr_values.items():
            label = str(labels[key]) + ' wavelengths'
            plt.plot(noise_value, label=label, color=colors[key], marker='o')
        ax.legend(loc=3)
        if osnr_type == 'gosnr':
            plt.ylabel("gOSNR (ASE + NLI) levels (dB)")
        else:
            plt.ylabel("ASE-OSNR levels (dB)")
        plt.xlabel(
            "# of spans (length of each span: %s, unit: km; total distance: %s km)" % (spans_length[0][0],
                                                                                       sum(spans_length[0])))
        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_osnr_per_distance(osnr_values, distances, osnr_type):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.tick_params(width=0.2)
        labels = {0: 8, 1: 16, 2: 32, 3: 64}
        colors = {0: 'y', 1: 'b', 2: 'r', 3: 'g'}
        for key, osnr_value in osnr_values.items():
            label = str(labels[key]) + ' wavelengths'
            plt.plot(distances, osnr_value, label=label, color=colors[key], marker='o')
        ax.legend(loc=3)
        if osnr_type == 'gosnr':
            plt.ylabel("gOSNR (ASE + NLI) levels (dB)")
        else:
            plt.ylabel("ASE-OSNR levels (dB)")
        plt.xlabel("Link length (km)")
        plt.grid(True)
        plt.show()
