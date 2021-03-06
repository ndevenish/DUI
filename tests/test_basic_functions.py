# coding: utf-8

"""Test running DUI, but in a screenshot-friendly way"""

import pytest

from dui.m_idials_gui import MainWidget
from dui.cli_utils import sys_arg


@pytest.mark.gui
def test_reopen_without_write(qtbot, tmpdir):
    sys_arg.directory = str(tmpdir)
    # Open twice.
    MainWidget().close()
    MainWidget().close()
