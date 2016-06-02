from dials.util.idials import Controller
import sys

linear_example_from_JMP = '''
controller = Controller(".")
controller.set_mode("import")
controller.set_parameters("template=../X4_wide_M1S4_2_####.cbf", short_syntax=True)
controller.run()

controller.set_mode("find_spots")
controller.run()
'''

PyQt4_ver = '''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
print "using PyQt4"
#'''

#PySide_ver = '''
from PySide.QtGui import *
from PySide.QtCore import *
print "using PySide"
#'''

class MainWidget( QWidget):
    lst_commands = [
                    "import",
                    "find_spots",
                    "index",
                    "refine"
                    ]


    def __init__(self):
        super(MainWidget, self).__init__()

        self.lst_exe_pos = 0
        self.controller = Controller(".")


        self.btn_prv =  QPushButton('\n  Prev \n', self)
        self.btn_prv.clicked.connect(self.prv_clicked)

        self.btn_go =  QPushButton('\n    Go  \n', self)
        self.btn_go.clicked.connect(self.go_clicked)

        self.btn_nxt =  QPushButton('\n  Next \n', self)
        self.btn_nxt.clicked.connect(self.nxt_clicked)

        hbox =  QHBoxLayout()

        hbox.addWidget(self.btn_prv)
        hbox.addWidget(self.btn_go)
        hbox.addWidget(self.btn_nxt)

        self.setLayout(hbox)
        self.setWindowTitle('Shell dialog')
        self.show()

    def go_clicked(self):
        print "go_clicked(self)"
        cmd_to_run = self.lst_commands[self.lst_exe_pos]
        self.controller.set_mode(cmd_to_run)

        if( cmd_to_run == "import" ):
            self.controller.set_parameters("template=../X4_wide_M1S4_2_####.cbf", short_syntax=True)

        self.controller.run()


    def nxt_clicked(self):
        print "nxt_clicked(self)"
        self.lst_exe_pos += 1
        '''
        if( self.lst_exe_pos > len(self.lst_commands - 1) ):
            self.lst_exe_pos = len(self.lst_commands - 1)
        '''

    def prv_clicked(self):
        print "prv_clicked(self)"
        self.lst_exe_pos -= 1
        '''
        if( self.lst_exe_pos < 0 ):
            self.lst_exe_pos = 0
        '''

if __name__ == '__main__':
    app =  QApplication(sys.argv)
    ex = MainWidget()
    sys.exit(app.exec_())


