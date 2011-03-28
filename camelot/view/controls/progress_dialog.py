#  ============================================================================
#
#  Copyright (C) 2007-2011 Conceptive Engineering bvba. All rights reserved.
#  www.conceptive.be / project-camelot@conceptive.be
#
#  This file is part of the Camelot Library.
#
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file license.txt included in the packaging of
#  this file.  Please review this information to ensure GNU
#  General Public Licensing requirements will be met.
#
#  If you are unsure which license is appropriate for your use, please
#  visit www.python-camelot.com or contact project-camelot@conceptive.be
#
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
#  For use of this library in commercial applications, please contact
#  project-camelot@conceptive.be
#
#  ============================================================================

"""Functions and classes to use a progress dialog in combination with
a model thread"""

import logging

from camelot.core.utils import ugettext as _
from camelot.view.art import Icon

from PyQt4 import QtGui, QtCore

LOGGER = logging.getLogger( 'camelot.view.controls.progress_dialog' )

class ProgressDialog(QtGui.QProgressDialog):
    """A Progress Dialog to be used in combination with a post to the model thread::
    
    to display a progress dialog until my_function has finished :
    
    d = ProgressDialog()
    post(my_function, p.finished, p.exception)
    d.exec_()
    
    """

    progress_icon = Icon('tango/32x32/actions/appointment-new.png')
    
    def __init__(self, name, icon=progress_icon):
        QtGui.QProgressDialog.__init__( self, QtCore.QString(), QtCore.QString(), 0, 0 )
        label = QtGui.QLabel(unicode(name))
        #label.setPixmap(icon.getQPixmap())
        self.setLabel(label)
        self.setWindowTitle( _('Please wait') )

    @QtCore.pyqtSlot(bool)
    @QtCore.pyqtSlot()
    def finished(self, success=True):
        self.close()
        
    @QtCore.pyqtSlot(object)
    def exception(self, exception_info):
        from camelot.view.controls.exception import model_thread_exception_message_box
        model_thread_exception_message_box(exception_info)
        self.finished(False)
        
    @QtCore.pyqtSlot(object)
    def display_chart(self, chart ):
        from camelot.view.controls.editors import ChartEditor
        litebox = ChartEditor.show_fullscreen_chart(chart, self)
        litebox.closed_signal.connect( self.close )

    @QtCore.pyqtSlot(object)
    def display_pixmap(self, pixmap):
        """
        :param image: a camelot.view.art.Pixmap object
        """
        from camelot.view.controls.liteboxview import LiteBoxView
        litebox = LiteBoxView(parent=self)
        litebox.closed_signal.connect( self.close )
        litebox.show_fullscreen_pixmap( pixmap.getQPixmap() )
        
    @QtCore.pyqtSlot(object)
    def exit(self, return_code):
        """Stop the application event loop, with the given return code"""
        LOGGER.info( 'exit application with code %s'%return_code )
        QtGui.QApplication.exit( int( return_code ) ) 

