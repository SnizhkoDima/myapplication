"""
Модуль, що містить користувацькі віджети PySide6.
"""
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class StatsCanvas(FigureCanvas):
    """
    Віджет для відображення графіків Matplotlib у PySide6.
    """
    def __init__(self, parent=None):
        fig = Figure(figsize=(5, 4), dpi=100, facecolor='#f7f7f7')
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)