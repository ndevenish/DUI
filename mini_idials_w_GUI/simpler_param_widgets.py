'''
DUI's command simple stacked widgets

Author: Luis Fuentes-Montero (Luiso)
With strong help from DIALS and CCP4 teams

copyright (c) CCP4 - DLS
'''

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import os, sys

import libtbx.introspection

class FindspotsSimplerParameterTab( QWidget):
    '''
    This widget is the tool for tunning the simpler and most common parameters
    in the spot-finder, this widget is the first to appear once the button
    "Find Sots" at the left side of the GUI is clicked
    '''

    item_changed = pyqtSignal(str, str)

    def __init__(self, parent = None):
        super(FindspotsSimplerParameterTab, self).__init__()
        #self.param_widget_parent = parent.param_widget_parent

        xds_gain_label = QLabel("spotfinder.threshold.dispersion.gain")
        xds_gain_spn_bx = QDoubleSpinBox()
        xds_gain_spn_bx.local_path = "spotfinder.threshold.dispersion.gain"
        xds_gain_spn_bx.valueChanged.connect(self.spnbox_changed)


        xds_sigma_background_label = QLabel("spotfinder.threshold.dispersion.sigma_background")
        xds_sigma_background_spn_bx = QDoubleSpinBox()
        xds_sigma_background_spn_bx.setValue(6.0)
        xds_sigma_background_spn_bx.local_path = "spotfinder.threshold.dispersion.sigma_background"
        xds_sigma_background_spn_bx.valueChanged.connect(self.spnbox_changed)

        xds_sigma_strong_label = QLabel("spotfinder.threshold.dispersion.sigma_strong")
        xds_sigma_strong_spn_bx = QDoubleSpinBox()
        xds_sigma_strong_spn_bx.setValue(3.0)
        xds_sigma_strong_spn_bx.local_path = "spotfinder.threshold.dispersion.sigma_strong"
        xds_sigma_strong_spn_bx.valueChanged.connect(self.spnbox_changed)

        xds_global_threshold_label = QLabel("spotfinder.threshold.dispersion.global_threshold")
        xds_global_threshold_spn_bx = QDoubleSpinBox()
        xds_global_threshold_spn_bx.local_path = "spotfinder.threshold.dispersion.global_threshold"
        xds_global_threshold_spn_bx.valueChanged.connect(self.spnbox_changed)

        localLayout = QVBoxLayout()

        xds_gain_hb = QHBoxLayout()
        xds_gain_hb.addWidget(xds_gain_label)
        xds_gain_hb.addWidget(xds_gain_spn_bx)
        localLayout.addLayout(xds_gain_hb)

        xds_sigma_background_hb = QHBoxLayout()
        xds_sigma_background_hb.addWidget(xds_sigma_background_label)
        xds_sigma_background_hb.addWidget(xds_sigma_background_spn_bx)
        localLayout.addLayout(xds_sigma_background_hb)

        xds_sigma_strong_hb = QHBoxLayout()
        xds_sigma_strong_hb.addWidget(xds_sigma_strong_label)
        xds_sigma_strong_hb.addWidget(xds_sigma_strong_spn_bx)
        localLayout.addLayout(xds_sigma_strong_hb)

        xds_global_threshold_hb = QHBoxLayout()
        xds_global_threshold_hb.addWidget(xds_global_threshold_label)
        xds_global_threshold_hb.addWidget(xds_global_threshold_spn_bx)
        localLayout.addLayout(xds_global_threshold_hb)


        hbox_lay_nproc =  QHBoxLayout()
        label_nproc = QLabel("spotfinder.mp.nproc")
        #label_nproc.setPalette(palette_object)
        #label_nproc.setFont( QFont("Monospace", 10))
        hbox_lay_nproc.addWidget(label_nproc)


        self.box_nproc = QSpinBox()
        self.box_nproc.local_path = "spotfinder.mp.nproc"


        self.box_nproc.valueChanged.connect(self.spnbox_changed)
        hbox_lay_nproc.addWidget(self.box_nproc)
        localLayout.addLayout(hbox_lay_nproc)

        localLayout.addStretch(1)

        self.setLayout(localLayout)

        self.lst_var_widg = []
        for i in xrange(localLayout.count()):
            upper_box = localLayout.itemAt(i)
            try:
                for j in xrange(upper_box.count()):
                    local_widget = upper_box.itemAt(j).widget()
                    self.lst_var_widg.append(local_widget)
            except:
                pass

    def spnbox_changed(self, value):
        sender = self.sender()
        str_value = str(value)
        print value
        str_path = str(sender.local_path)

        #self.param_widget_parent.update_lin_txt(str_path, str_value)
        self.item_changed.emit(str_path, str_value)

    def set_max_nproc(self):
        cpu_max_proc = int(libtbx.introspection.number_of_processors())
        self.box_nproc.setValue(cpu_max_proc)
        return cpu_max_proc


class IndexSimplerParamTab( QWidget):
    '''
    This widget is the tool for tunning the simpler and most common parameters
    in the indexer, this widget is the first to appear once the button
    "Index" at the left side of the GUI is clicked
    '''

    item_changed = pyqtSignal(str, str)

    def __init__(self, phl_obj = None, parent=None):
        super(IndexSimplerParamTab, self).__init__()

        #self.param_widget_parent = parent.param_widget_parent
        #indexing_method_check = QCheckBox("indexing.method")

        hbox_method =  QHBoxLayout()
        label_method_62 = QLabel("indexing.method")
        hbox_method.addWidget(label_method_62)
        box_method_62 = QComboBox()
        box_method_62.tmp_lst=[]
        box_method_62.local_path = "indexing.method"
        box_method_62.tmp_lst.append("fft3d")
        box_method_62.tmp_lst.append("fft1d")
        box_method_62.tmp_lst.append("real_space_grid_search")
        for lst_itm in box_method_62.tmp_lst:
            box_method_62.addItem(lst_itm)
        box_method_62.currentIndexChanged.connect(self.combobox_changed)

        hbox_method.addWidget(box_method_62)

        localLayout = QVBoxLayout()
        #localLayout.addLayout(hbox_lay_scan_varying)
        localLayout.addLayout(hbox_method)
        localLayout.addStretch(1)

        self.setLayout(localLayout)

        self.lst_var_widg = []
        for i in xrange(localLayout.count()):
            upper_box = localLayout.itemAt(i)
            try:
                for j in xrange(upper_box.count()):
                    local_widget = upper_box.itemAt(j).widget()
                    self.lst_var_widg.append(local_widget)
            except:
                pass

    def combobox_changed(self, value):
        sender = self.sender()
        str_value = str(sender.tmp_lst[value])
        str_path = str(sender.local_path)

        #self.param_widget_parent.update_lin_txt(str_path, str_value)
        self.item_changed.emit(str_path, str_value)


class RefineBravaiSimplerParamTab(QWidget):
    #TODO some doc string here

    item_changed = pyqtSignal(str, str)

    def __init__(self, parent = None):
        super(RefineBravaiSimplerParamTab, self).__init__()

        hbox_lay_scan_varying =  QHBoxLayout()
        localLayout = QVBoxLayout()
        label_scan_varying = QLabel("refinement.parameterisation.scan_varying")

        hbox_lay_scan_varying.addWidget(label_scan_varying)

        box_scan_varying = QComboBox()
        box_scan_varying.local_path = "refinement.parameterisation.scan_varying"
        box_scan_varying.tmp_lst=[]
        box_scan_varying.tmp_lst.append("True")
        box_scan_varying.tmp_lst.append("False")
        for lst_itm in box_scan_varying.tmp_lst:
            box_scan_varying.addItem(lst_itm)
        box_scan_varying.setCurrentIndex(1)

        box_scan_varying.currentIndexChanged.connect(self.combobox_changed)
        hbox_lay_scan_varying.addWidget(box_scan_varying)
        localLayout.addLayout(hbox_lay_scan_varying)
        localLayout.addStretch(1)
        self.setLayout(localLayout)

        self.lst_var_widg = []
        self.lst_var_widg.append(box_scan_varying)
        self.lst_var_widg.append(label_scan_varying)

    def combobox_changed(self, value):
        sender = self.sender()
        str_value = str(sender.tmp_lst[value])
        str_path = str(sender.local_path)

        #self.param_widget_parent.update_lin_txt(str_path, str_value)
        self.item_changed.emit(str_path, str_value)


class RefineSimplerParamTab( QWidget):
    '''
    This widget is the tool for tunning the simpler and most common parameters
    in the refiner, this widget is the first to appear once the button
    "Refine" at the left side of the GUI is clicked
    '''

    item_changed = pyqtSignal(str, str)

    def __init__(self, parent = None):
        super(RefineSimplerParamTab, self).__init__()
        #self.param_widget_parent = parent.param_widget_parent

        hbox_lay_scan_varying =  QHBoxLayout()
        localLayout = QVBoxLayout()
        label_scan_varying = QLabel("refinement.parameterisation.scan_varying")

        hbox_lay_scan_varying.addWidget(label_scan_varying)

        box_scan_varying = QComboBox()
        box_scan_varying.local_path = "refinement.parameterisation.scan_varying"
        box_scan_varying.tmp_lst=[]
        box_scan_varying.tmp_lst.append("True")
        box_scan_varying.tmp_lst.append("False")
        box_scan_varying.tmp_lst.append("Auto")

        for lst_itm in box_scan_varying.tmp_lst:
            box_scan_varying.addItem(lst_itm)
        box_scan_varying.setCurrentIndex(1)

        box_scan_varying.currentIndexChanged.connect(self.combobox_changed)
        hbox_lay_scan_varying.addWidget(box_scan_varying)
        localLayout.addLayout(hbox_lay_scan_varying)
        localLayout.addStretch(1)
        self.setLayout(localLayout)

        self.lst_var_widg = []
        self.lst_var_widg.append(box_scan_varying)
        self.lst_var_widg.append(label_scan_varying)

    def combobox_changed(self, value):
        sender = self.sender()
        str_value = str(sender.tmp_lst[value])
        str_path = str(sender.local_path)

        #self.param_widget_parent.update_lin_txt(str_path, str_value)
        self.item_changed.emit(str_path, str_value)



class IntegrateSimplerParamTab( QWidget):
    '''
    This widget is the tool for tunning the simpler and most common parameters
    in the integrate algorithm, this widget is the first to appear once the button
    "Integrate" at the left side of the GUI is clicked
    '''

    item_changed = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(IntegrateSimplerParamTab, self).__init__()
        #self.param_widget_parent = parent.param_widget_parent

        localLayout = QVBoxLayout()
        PrFit_lay_out =  QHBoxLayout()
        label_PrFit = QLabel("integration.profile.fitting")
        PrFit_lay_out.addWidget(label_PrFit)

        PrFit_comb_bx = QComboBox()
        PrFit_comb_bx.local_path = "integration.profile.fitting"
        PrFit_comb_bx.tmp_lst=[]
        PrFit_comb_bx.tmp_lst.append("True")
        PrFit_comb_bx.tmp_lst.append("False")

        for lst_itm in PrFit_comb_bx.tmp_lst:
            PrFit_comb_bx.addItem(lst_itm)
        PrFit_comb_bx.currentIndexChanged.connect(self.combobox_changed)
        PrFit_lay_out.addWidget(PrFit_comb_bx)
        localLayout.addLayout(PrFit_lay_out)

        hbox_lay_algorithm_53 =  QHBoxLayout()
        label_algorithm_53 = QLabel("integration.background.algorithm")
        hbox_lay_algorithm_53.addWidget(label_algorithm_53)

        box_algorithm_53 = QComboBox()
        box_algorithm_53.local_path = "integration.background.algorithm"
        box_algorithm_53.tmp_lst=[]
        box_algorithm_53.tmp_lst.append("simple")
        box_algorithm_53.tmp_lst.append("null")
        box_algorithm_53.tmp_lst.append("median")
        box_algorithm_53.tmp_lst.append("gmodel")
        box_algorithm_53.tmp_lst.append("glm")

        for lst_itm in box_algorithm_53.tmp_lst:
            box_algorithm_53.addItem(lst_itm)
        box_algorithm_53.setCurrentIndex(4)
        box_algorithm_53.currentIndexChanged.connect(self.combobox_changed)
        hbox_lay_algorithm_53.addWidget(box_algorithm_53)
        localLayout.addLayout(hbox_lay_algorithm_53)

        hbox_lay_nproc =  QHBoxLayout()
        label_nproc = QLabel("integration.mp.nproc")
        #label_nproc.setFont( QFont("Monospace", 10))
        hbox_lay_nproc.addWidget(label_nproc)

        self.box_nproc = QSpinBox()

        self.box_nproc.local_path = "integration.mp.nproc"
        self.box_nproc.valueChanged.connect(self.spnbox_changed)
        hbox_lay_nproc.addWidget(self.box_nproc)
        localLayout.addLayout(hbox_lay_nproc)

        localLayout.addStretch(1)
        '''
        self.mtz_name_lin =   QLineEdit(self)
        self.mtz_name_lin.setText("hkl_out.mtz")
        localLayout.addWidget(QLabel("mtz output name:"))
        localLayout.addWidget(self.mtz_name_lin)
        self.mtz_name_lin.textChanged.connect(self.mtz_name_changed)
        '''

        self.setLayout(localLayout)
        self.box_nproc.tmp_lst = None

        self.lst_var_widg = []
        for i in xrange(localLayout.count()):
            upper_box = localLayout.itemAt(i)
            try:
                for j in xrange(upper_box.count()):
                    local_widget = upper_box.itemAt(j).widget()
                    self.lst_var_widg.append(local_widget)

            except:
                pass

    def combobox_changed(self, value):
        sender = self.sender()
        str_value = str(sender.tmp_lst[value])
        str_path = str(sender.local_path)

        #self.param_widget_parent.update_lin_txt(str_path, str_value)
        self.item_changed.emit(str_path, str_value)

    def spnbox_changed(self, value):
        sender = self.sender()
        str_value = str(value)
        print value
        str_path = str(sender.local_path)

        self.item_changed.emit(str_path, str_value)

    def set_max_nproc(self):
        cpu_max_proc = int(libtbx.introspection.number_of_processors())
        self.box_nproc.setValue(cpu_max_proc)
        return cpu_max_proc

    def mtz_name_changed(self, value):
        print "used to run"
        #print "self.param_widget_parent.super_parent.mtz_name_changed(value)"



class SymmetrySimplerParamTab(QWidget):
    '''
    This widget is the tool for tunning the simpler and most common parameters
    in the symmetry command, this widget is the first to appear once the button
    "Symmetry" at the left side of the GUI is clicked
    '''

    item_changed = pyqtSignal(str, str)

    def __init__(self, parent = None):
        super(SymmetrySimplerParamTab, self).__init__()

        hbox_d_min =  QHBoxLayout()
        localLayout = QVBoxLayout()
        label_d_min = QLabel("d_min")

        hbox_d_min.addWidget(label_d_min)

        xds_sigma_strong_label = QLabel("d_min")
        d_min_spn_bx = QDoubleSpinBox()
        d_min_spn_bx.local_path = "d_min"
        d_min_spn_bx.setSpecialValueText("Auto")
        d_min_spn_bx.setValue(0.0)
        hbox_d_min.addWidget(d_min_spn_bx)

        d_min_spn_bx.valueChanged.connect(self.spnbox_changed)

        localLayout.addLayout(hbox_d_min)
        localLayout.addStretch(1)
        self.setLayout(localLayout)

        self.lst_var_widg = []
        self.lst_var_widg.append(d_min_spn_bx)
        self.lst_var_widg.append(label_d_min)

    def spnbox_changed(self, value):
        sender = self.sender()
        str_value = str(value)
        print value
        str_path = str(sender.local_path)

        self.item_changed.emit(str_path, str_value)


class ScaleSimplerParamTab(QWidget):

    '''
    This widget is the tool for tunning the simpler and most common parameters
    in the scale command, this widget is the first to appear once the button
    "Scale" at the left side of the GUI is clicked
    '''

    item_changed = pyqtSignal(str, str)

    def __init__(self, parent = None):
        super(ScaleSimplerParamTab, self).__init__()

        localLayout = QVBoxLayout()

        hbox_lay_mod =  QHBoxLayout()
        label_mod = QLabel("model")

        hbox_lay_mod.addWidget(label_mod)

        box_mod = QComboBox()
        box_mod.local_path = "model"
        box_mod.tmp_lst=[]
        box_mod.tmp_lst.append("physical")
        box_mod.tmp_lst.append("array")
        box_mod.tmp_lst.append("KB")
        for lst_itm in box_mod.tmp_lst:
            box_mod.addItem(lst_itm)

        box_mod.currentIndexChanged.connect(self.combobox_changed)
        hbox_lay_mod.addWidget(box_mod)

        hbox_lay_wgh_opt_err =  QHBoxLayout()
        label_wgh_opt_err = QLabel("weighting.optimise_errors")

        hbox_lay_wgh_opt_err.addWidget(label_wgh_opt_err)

        box_wgh_opt_err = QComboBox()
        box_wgh_opt_err.local_path = "weighting.optimise_errors"
        box_wgh_opt_err.tmp_lst=[]
        box_wgh_opt_err.tmp_lst.append("True")
        box_wgh_opt_err.tmp_lst.append("False")
        for lst_itm in box_wgh_opt_err.tmp_lst:
            box_wgh_opt_err.addItem(lst_itm)

        box_wgh_opt_err.currentIndexChanged.connect(self.combobox_changed)
        hbox_lay_wgh_opt_err.addWidget(box_wgh_opt_err)

        localLayout.addLayout(hbox_lay_mod)
        localLayout.addLayout(hbox_lay_wgh_opt_err)
        localLayout.addStretch(1)

        self.setLayout(localLayout)

        self.lst_var_widg = []
        self.lst_var_widg.append(box_mod)
        self.lst_var_widg.append(label_mod)
        self.lst_var_widg.append(box_wgh_opt_err)
        self.lst_var_widg.append(label_wgh_opt_err)

    def combobox_changed(self, value):
        sender = self.sender()
        str_value = str(sender.tmp_lst[value])
        str_path = str(sender.local_path)

        #self.param_widget_parent.update_lin_txt(str_path, str_value)
        self.item_changed.emit(str_path, str_value)

        '''
    def spnbox_changed(self, value):
        sender = self.sender()
        str_value = str(value)
        print value
        str_path = str(sender.local_path)

        self.item_changed.emit(str_path, str_value)
        '''

class ExportSimplerParamTab(QWidget):

    '''
    This widget is the tool for tunning the simpler and most common parameters
    in the scale command, this widget is the first to appear once the button
    "Scale" at the left side of the GUI is clicked
    '''

    item_changed = pyqtSignal(str, str)

    def __init__(self, parent = None):
        super(ExportSimplerParamTab, self).__init__()

        hbox_lay_scan_varying =  QHBoxLayout()
        localLayout = QVBoxLayout()
        label_scan_varying = QLabel("... export ...scan_varying")

        hbox_lay_scan_varying.addWidget(label_scan_varying)

        box_scan_varying = QComboBox()
        box_scan_varying.local_path = "refinement.parameterisation.scan_varying"
        box_scan_varying.tmp_lst=[]
        box_scan_varying.tmp_lst.append("True")
        box_scan_varying.tmp_lst.append("False")
        for lst_itm in box_scan_varying.tmp_lst:
            box_scan_varying.addItem(lst_itm)
        box_scan_varying.setCurrentIndex(1)

        box_scan_varying.currentIndexChanged.connect(self.combobox_changed)
        hbox_lay_scan_varying.addWidget(box_scan_varying)
        localLayout.addLayout(hbox_lay_scan_varying)
        localLayout.addStretch(1)
        self.setLayout(localLayout)

        self.lst_var_widg = []
        self.lst_var_widg.append(box_scan_varying)
        self.lst_var_widg.append(label_scan_varying)

    def combobox_changed(self, value):
        sender = self.sender()
        str_value = str(sender.tmp_lst[value])
        str_path = str(sender.local_path)

        #self.param_widget_parent.update_lin_txt(str_path, str_value)
        self.item_changed.emit(str_path, str_value)

        '''
    def spnbox_changed(self, value):
        sender = self.sender()
        str_value = str(value)
        print value
        str_path = str(sender.local_path)

        self.item_changed.emit(str_path, str_value)
        '''


class TmpTstWidget( QWidget):

    def __init__(self, parent = None):
        super(TmpTstWidget, self).__init__()
        #self.param_widget_parent = self
        #my_widget = FindspotsSimplerParameterTab(self)
        #my_widget = SymmetrySimplerParamTab(self)
        #my_widget = ScaleSimplerParamTab(self)
        my_widget = ExportSimplerParamTab(self)

        my_box = QVBoxLayout()
        my_box.addWidget(my_widget)
        self.setLayout(my_box)
        self.show()


if(__name__ == "__main__"):
    app =  QApplication(sys.argv)
    ex = TmpTstWidget()
    sys.exit(app.exec_())

