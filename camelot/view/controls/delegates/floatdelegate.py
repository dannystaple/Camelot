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
from PyQt4 import QtCore
from PyQt4.QtCore import Qt

from customdelegate import CustomDelegate, DocumentationMetaclass
from camelot.view.controls import editors
from camelot.core import constants
from camelot.core.utils import variant_to_pyobject
from camelot.view.proxy import ValueLoading

class FloatDelegate( CustomDelegate ):
    """Custom delegate for float values"""

    __metaclass__ = DocumentationMetaclass

    editor = editors.FloatEditor

    def __init__( self,
                 minimum=constants.camelot_minfloat,
                 maximum=constants.camelot_maxfloat,
                 precision=2,
                 parent=None,
                 unicode_format=None,
                 **kwargs ):
        """
        :param precision:  The number of digits after the decimal point displayed.  This defaults
        to the precision specified in the definition of the Field.     
        If the attribute is a calculated field, which gets its precision from SQLAclhemy introspection,
        precision will be set to None, so precision must be explicitely set in the field attributes.
        """
        CustomDelegate.__init__(self,
                                parent=parent,
                                precision=precision or 2,
                                minimum=minimum, maximum=maximum,
                                **kwargs )                   
        self.minimum = minimum
        self.maximum = maximum
        self.precision = precision or 2
        self.unicode_format = unicode_format

    def paint( self, painter, option, index ):
        painter.save()
        self.drawBackground(painter, option, index)
        value = variant_to_pyobject(index.model().data(index, Qt.EditRole))

        if value in (None, ValueLoading):
            value_str = ''
        elif self.unicode_format:
            value_str = self.unicode_format(value)
        else:
            value_str = QtCore.QString("%L1").arg(float(value),0,'f',self.precision)

        self.paint_text( painter, option, index, value_str, horizontal_align=Qt.AlignRight )
        painter.restore()

