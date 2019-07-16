import matplotlib.pyplot as plt

class Graphic():
    
    def plot_osnr_increment(self, osnr_values, spans_length):
        plt.plot(osnr_values, marker='o')
        plt.ylabel("OSNR-ASE (dB)")
        plt.xlabel("# of spans (length of each span: %s, unit: km; total distance: %s km)" %(spans_length, sum(spans_length)))
        plt.title("Signal degradation with # of span")
        plt.grid(True)
        plt.show()
