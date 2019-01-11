"""
Containers for widgets related to each step

Author: Luis Fuentes-Montero (Luiso)
With strong help from DIALS and CCP4 teams

copyright (c) CCP4 - DLS
"""
from __future__ import absolute_import, division, print_function, unicode_literals

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import logging
import numbers
import string

from dxtbx.model.experiment_list import InvalidExperimentListError

from .outputs_n_viewers.info_handler import update_all_data
from .qt import QHBoxLayout, QLabel, QWidget, uic
from .gui_utils import get_package_path

logger = logging.getLogger(__name__)


def update_data_label(data_label, data_info, n_dec=2):
    # data_label.setStyleSheet("background-color: silver")
    data_label.setStyleSheet("background-color: lightGray")

    if "int" in str(type(data_info)):
        data_label.setText(str(data_info))

    elif "float" in str(type(data_info)):
        rnd_nm = round(data_info, ndigits=n_dec)
        data_label.setText(str(rnd_nm))

    elif "str" in str(type(data_info)):
        data_label.setText(data_info)

    else:
        data_label.setText("   -      ")
        # data_label.setStyleSheet("background-color: gray")
        data_label.setStyleSheet("background-color: lightGray")


def get_spacebox(size):
    space_box = QHBoxLayout()
    space_box.insertSpacing(1, size)
    return space_box


class InfoWidgetFormatter(string.Formatter):
    """Special formatter for InfoWidget fields.

    Has the following special behaviour:
        - None fields are shown as "-"
        - All floating-point numbers are default formatted to
          2 d.p. if there has not been a format otherwise specified.
    """

    def format_field(self, value, format_spec):
        # If the value has nothing, don't convert
        if value is None:
            return "-"
        # By default, floating point numbers to 2 decimal places
        if (
            isinstance(value, numbers.Real)
            and not isinstance(value, numbers.Integral)
            and not format_spec
        ):
            format_spec = ".2f"
        return super(InfoWidgetFormatter, self).format_field(value, format_spec)


class InfoWidget(QWidget):
    def __init__(self, parent=None):
        super(InfoWidget, self).__init__(parent=parent)

        info_panel_path = get_package_path("resources/info_panel.ui")
        uic.loadUi(info_panel_path, self)

        self.my_json_path = None
        self.my_pikl_path = None

        self.infoWidgets = [
            x
            for x in self.findChildren(QLabel)
            if "infoPath" in x.dynamicPropertyNames()
        ]
        logger.debug("Found %d info Widgets on info panel", len(self.infoWidgets))

        self.update_data(
            exp_json_path=self.my_json_path, refl_pikl_path=self.my_pikl_path
        )

        self.setMaximumSize(self.maximumSize().width(), self.sizeHint().height())

    def update_data(self, exp_json_path=None, refl_pikl_path=None):
        """Update the widget with new display information"""
        # TODO: Change interface of function to not recieve list including
        #       predicted reflections, as long as it doesn't need it

        logger.debug("\n\nrefl_pikl_path = %s", refl_pikl_path)
        logger.debug("exp_json_path = %s %s", exp_json_path, "\n")

        try:
            try:
                pickle_to_read = refl_pikl_path[0]
            except ValueError:
                pickle_to_read = None

            self.all_data = update_all_data(
                experiments_path=exp_json_path, reflections_path=pickle_to_read
            )
        except InvalidExperimentListError:
            # Probably an invalid json file - we sometimes try to parse these
            self.all_data = update_all_data(
                experiments_path=None, reflections_path=None
            )
        except BaseException as e:
            # We don't want to catch bare exceptions but don't know
            # what this was supposed to catch. Log it.
            logger.error("Caught unknown exception type %s: %s", type(e).__name__, e)
            logger.debug("unable to update data panel")
            self.all_data = update_all_data(
                experiments_path=None, reflections_path=None
            )

        # Update every widget with it's dynamic field name
        fmt = InfoWidgetFormatter()
        for widget in self.infoWidgets:
            infoPath = widget.property("infoPath")
            new_text = fmt.format(infoPath, **self.all_data.__dict__)
            widget.setText(new_text)
