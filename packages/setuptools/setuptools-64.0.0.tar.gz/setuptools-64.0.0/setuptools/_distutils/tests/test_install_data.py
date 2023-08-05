"""Tests for distutils.command.install_data."""
import os

import pytest

from distutils.command.install_data import install_data
from distutils.tests import support


@pytest.mark.usefixtures('save_env')
class TestInstallData(
    support.TempdirManager,
    support.LoggingSilencer,
):
    def test_simple_run(self):
        pkg_dir, dist = self.create_dist()
        cmd = install_data(dist)
        cmd.install_dir = inst = os.path.join(pkg_dir, 'inst')

        # data_files can contain
        #  - simple files
        #  - a tuple with a path, and a list of file
        one = os.path.join(pkg_dir, 'one')
        self.write_file(one, 'xxx')
        inst2 = os.path.join(pkg_dir, 'inst2')
        two = os.path.join(pkg_dir, 'two')
        self.write_file(two, 'xxx')

        cmd.data_files = [one, (inst2, [two])]
        assert cmd.get_inputs() == [one, (inst2, [two])]

        # let's run the command
        cmd.ensure_finalized()
        cmd.run()

        # let's check the result
        assert len(cmd.get_outputs()) == 2
        rtwo = os.path.split(two)[-1]
        assert os.path.exists(os.path.join(inst2, rtwo))
        rone = os.path.split(one)[-1]
        assert os.path.exists(os.path.join(inst, rone))
        cmd.outfiles = []

        # let's try with warn_dir one
        cmd.warn_dir = 1
        cmd.ensure_finalized()
        cmd.run()

        # let's check the result
        assert len(cmd.get_outputs()) == 2
        assert os.path.exists(os.path.join(inst2, rtwo))
        assert os.path.exists(os.path.join(inst, rone))
        cmd.outfiles = []

        # now using root and empty dir
        cmd.root = os.path.join(pkg_dir, 'root')
        inst4 = os.path.join(pkg_dir, 'inst4')
        three = os.path.join(cmd.install_dir, 'three')
        self.write_file(three, 'xx')
        cmd.data_files = [one, (inst2, [two]), ('inst3', [three]), (inst4, [])]
        cmd.ensure_finalized()
        cmd.run()

        # let's check the result
        assert len(cmd.get_outputs()) == 4
        assert os.path.exists(os.path.join(inst2, rtwo))
        assert os.path.exists(os.path.join(inst, rone))
