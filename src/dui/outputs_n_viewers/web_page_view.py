from __future__ import absolute_import, division, print_function

import logging
import os
import sys


try:
    from dui.outputs_n_viewers.img_view_tools import ProgBarBox
    from dui.qt import (
        QApplication,
        QHBoxLayout,
        QPushButton,
        QUrl,
        QVBoxLayout,
        QWebSettings,
        QWebView,
        QWidget,
    )

except ImportError:
    from .img_view_tools import ProgBarBox
    from ..qt import (
        QApplication,
        QHBoxLayout,
        QPushButton,
        QUrl,
        QVBoxLayout,
        QWebSettings,
        QWebView,
        QWidget,
    )

logger = logging.getLogger(__name__)


class WebTab(QWidget):
    def __init__(self):
        super(WebTab, self).__init__()
        tmp_off = """
        logger.debug(
            " QWebSettings.JavascriptEnabled = %s", QWebSettings.JavascriptEnabled
        )
        QWebSettings.JavascriptEnabled = True
        """

        self.dummy_html = """<html>
            <head>
            <title>A Sample Page</title>
            </head>
            <body>
            <h3>There is no report available for this step.</h3>
            </body>
            </html>"""

        self.web = QWebView()
        logger.debug("No need to load HTML file yet\n")
        self.web.loadFinished.connect(self.load_finished)

        self.my_bar = None
        hbox = QHBoxLayout()
        hbox.addWidget(self.web)
        self.setLayout(hbox)

    def update_page(self, new_path=None):
        try:
            logger.info("\n >> update_page( %s )", new_path)
            new_path = os.path.abspath(new_path)

            # new_path = "file://" + new_path # unix way
            new_path = "file:///" + new_path  # Windows way(seems to work on Unix too)
            logger.info(" >> new_path: %s", new_path)
            self.web.load(QUrl(new_path))

            logger.info(" Loading  %s", new_path)

            txt_lab = "updating Report view:"
            self.my_bar = ProgBarBox(min_val=0, max_val=10, text=txt_lab)
            self.my_bar(5)

        except BaseException as e:
            # TODO(nick) - Don't know what this generic exception was supposed
            # to catch so catch all for now and work out what it was supposed to be
            #logger.info("\n failed to show <<", new_path, ">>  on web view (", e, ")")
            self.web.setHtml(self.dummy_html)

    def load_finished(self, ok_bool):
        logger.info("HTML Load(ok) = %s", ok_bool)
        tmp_off = """
        if not ok_bool:
            self.web.setHtml(self.dummy_html)
        """

        self.web.show()
        logger.info(" finished Loading HTML ")

        if self.my_bar is not None:
            self.my_bar.ended()


class TmpTstWidget(QWidget):
    def __init__(self, parent=None):
        super(TmpTstWidget, self).__init__()
        # self.param_widget_parent = self
        self.my_widget = WebTab()
        self.btn1 = QPushButton("Click me", self)
        self.btn1.clicked.connect(self.load_page)
        my_box = QVBoxLayout()
        my_box.addWidget(self.my_widget)
        my_box.addWidget(self.btn1)
        self.npos = 1
        self.setLayout(my_box)

    def load_page(self):
        self.my_widget.update_page(sys.argv[self.npos])
        self.npos += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TmpTstWidget()
    ex.show()
    sys.exit(app.exec_())
