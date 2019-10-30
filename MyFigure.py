from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QSizePolicy

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(PlotCanvas, self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)

    def plot(self, data):
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('Fu Zai Gong Lv')
        self.draw()