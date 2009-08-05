
from customeditor import *

class ColorEditor(CustomEditor):
  
  def __init__(self, parent=None, editable=True, **kwargs):
    CustomEditor.__init__(self, parent)
    layout = QtGui.QVBoxLayout(self)
    layout.setSpacing(0)
    layout.setMargin(0)
    self.color_button = QtGui.QPushButton(parent)
    self.color_button.setMaximumSize(QtCore.QSize(20, 20))
    layout.addWidget(self.color_button)
    if editable:
      self.connect(self.color_button,
                   QtCore.SIGNAL('clicked(bool)'),
                   self.buttonClicked)
    self.setLayout(layout)
    self._color = None

  def get_value(self):
    color = self.getColor()
    if color:
      value = (color.red(), color.green(), color.blue(), color.alpha())
    else:
      value = None
    return CustomEditor.get_value(self) or value
      
  def set_value(self, value):
    value = CustomEditor.set_value(self, value)
    if value:
      color = QtGui.QColor()
      color.setRgb(*value)
      self.setColor(color)
    else:
      self.setColor(value)    
    
  def getColor(self):
    return self._color
  
  def setColor(self, color):
    pixmap = QtGui.QPixmap(16, 16)
    if color:
      pixmap.fill(color)
    else:
      pixmap.fill(Qt.transparent)
    self.color_button.setIcon(QtGui.QIcon(pixmap))
    self._color = color
     
  def buttonClicked(self, raised):
    if self._color:
      color = QtGui.QColorDialog.getColor(self._color)
    else:
      color = QtGui.QColorDialog.getColor()
    if color.isValid() and color!=self._color:
      self.setColor(color)
      self.emit(QtCore.SIGNAL('editingFinished()'))