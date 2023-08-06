import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


class ConfusionMatrix:
    """
    Plot confusion matrix
    """
    def __init__(self, y_true, y_pred, labels=None):
        self.y_true = np.asarray(y_true, dtype=np.int)
        self.y_pred = np.asarray(y_pred, dtype=np.int)
        self.labels = labels or [str(i) for i in range(min(self.y_true), max(self.y_true) + 1)]

    def show(self, title=None, normalize=None, cmap='viridis', xticks_rotation=70, **kwargs):
        """
        Draw matrix
        :param normalize: bool
        :param cmap: str
        :param xticks_rotation: int
        """
        cm = confusion_matrix(self.y_true, self.y_pred, normalize=normalize)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=self.labels)
        cf = disp.plot(include_values=True, cmap=cmap, xticks_rotation=xticks_rotation, **kwargs)

        if title is not None:
            cf.ax_.set_title(title)

        return cf