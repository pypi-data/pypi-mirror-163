from __future__ import annotations
from typing import TYPE_CHECKING
from enum import Enum
from qtpy import QtWidgets as QtW, QtCore, QtGui
from qtpy.QtCore import Qt

if TYPE_CHECKING:
    from ._tabwidget import QTabbedTableStack


class Anchor(Enum):
    """Anchor position"""

    top_left = "top_left"
    top_right = "top_right"
    bottom_left = "bottom_left"
    bottom_right = "bottom_right"


_STYLE = """
QOverlayWidget {
    background-color: white;
    border: 1px solid gray;
    border-radius: 3px;
}
"""


class QOverlayWidget(QtW.QDialog):
    def __init__(self, parent: QTabbedTableStack):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.SubWindow)
        self._widget = None
        self.setStyleSheet(_STYLE)

        _layout = QtW.QVBoxLayout()
        _layout.setContentsMargins(2, 2, 2, 2)

        self.setLayout(_layout)

        parent.resizedSignal.connect(self.alignToParent)
        self.setAnchor(Anchor.bottom_right)
        self.hide()

        effect = QtW.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)
        self._effect = effect

    def addWidget(self, widget: QtW.QWidget):
        if self.layout().count() > 0:
            self.removeWidget()
        self.layout().addWidget(widget)
        self.resize(widget.sizeHint())
        self._widget = widget
        self.alignToParent()

    def removeWidget(self):
        self._widget = None
        self.layout().removeWidget(self.layout().itemAt(0).widget())
        self.resize(QtCore.QSize(0, 0))

    def widget(self) -> QtW.QWidget:
        return self._widget

    def anchor(self) -> Anchor:
        return self._anchor

    def setAnchor(self, anc: Anchor | str) -> None:
        self._anchor = Anchor(anc)
        return self.alignToParent()

    if TYPE_CHECKING:

        def parentWidget(self) -> QTabbedTableStack:
            ...

    def show(self):
        super().show()
        return self.alignToParent()

    def alignToParent(self):
        """Position widget at the bottom right edge of the parent."""
        qtable = self.parentWidget()
        if not qtable:
            return
        if self._anchor == Anchor.bottom_left:
            self.alignBottomLeft()
        elif self._anchor == Anchor.bottom_right:
            self.alignBottomRight()
        elif self._anchor == Anchor.top_left:
            self.alignTopLeft()
        elif self._anchor == Anchor.top_right:
            self.alignTopRight()
        else:
            raise RuntimeError

    def viewRect(self) -> QtCore.QRect:
        """Return the parent table rect."""
        parent = self.parentWidget()
        qtable = parent.tableAtIndex(parent.currentIndex())
        rect = qtable.widget(0).rect()
        return rect

    def alignTopLeft(self, offset=(8, 8)):
        pos = self.viewRect().topLeft()
        pos.setX(pos.x() + offset[0])
        pos.setY(pos.y() + offset[1])
        self.move(pos)

    def alignTopRight(self, offset=(26, 8)):
        pos = self.viewRect().topRight()
        pos.setX(pos.x() - self.rect().width() - offset[0])
        pos.setY(pos.y() + offset[1])
        self.move(pos)

    def alignBottomLeft(self, offset=(8, 8)):
        pos = self.viewRect().bottomLeft()
        pos.setX(pos.x() + offset[0])
        pos.setY(pos.y() - self.rect().height() - offset[1])
        self.move(pos)

    def alignBottomRight(self, offset=(26, 8)):
        pos = self.viewRect().bottomRight()
        pos.setX(pos.x() - self.rect().width() - offset[0])
        pos.setY(pos.y() - self.rect().height() - offset[1])
        self.move(pos)
