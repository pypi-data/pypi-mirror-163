"""Tests for distutils.spawn."""
import os
import stat
import sys
import unittest.mock as mock

from test.support import unix_shell

from . import py38compat as os_helper

from distutils.spawn import find_executable
from distutils.spawn import spawn
from distutils.errors import DistutilsExecError
from distutils.tests import support
import pytest


class TestSpawn(support.TempdirManager, support.LoggingSilencer):
    @pytest.mark.skipif("os.name not in ('nt', 'posix')")
    def test_spawn(self):
        tmpdir = self.mkdtemp()

        # creating something executable
        # through the shell that returns 1
        if sys.platform != 'win32':
            exe = os.path.join(tmpdir, 'foo.sh')
            self.write_file(exe, '#!%s\nexit 1' % unix_shell)
        else:
            exe = os.path.join(tmpdir, 'foo.bat')
            self.write_file(exe, 'exit 1')

        os.chmod(exe, 0o777)
        with pytest.raises(DistutilsExecError):
            spawn([exe])

        # now something that works
        if sys.platform != 'win32':
            exe = os.path.join(tmpdir, 'foo.sh')
            self.write_file(exe, '#!%s\nexit 0' % unix_shell)
        else:
            exe = os.path.join(tmpdir, 'foo.bat')
            self.write_file(exe, 'exit 0')

        os.chmod(exe, 0o777)
        spawn([exe])  # should work without any error

    def test_find_executable(self):
        with os_helper.temp_dir() as tmp_dir:
            # use TESTFN to get a pseudo-unique filename
            program_noeext = os_helper.TESTFN
            # Give the temporary program an ".exe" suffix for all.
            # It's needed on Windows and not harmful on other platforms.
            program = program_noeext + ".exe"

            filename = os.path.join(tmp_dir, program)
            with open(filename, "wb"):
                pass
            os.chmod(filename, stat.S_IXUSR)

            # test path parameter
            rv = find_executable(program, path=tmp_dir)
            assert rv == filename

            if sys.platform == 'win32':
                # test without ".exe" extension
                rv = find_executable(program_noeext, path=tmp_dir)
                assert rv == filename

            # test find in the current directory
            with os_helper.change_cwd(tmp_dir):
                rv = find_executable(program)
                assert rv == program

            # test non-existent program
            dont_exist_program = "dontexist_" + program
            rv = find_executable(dont_exist_program, path=tmp_dir)
            assert rv is None

            # PATH='': no match, except in the current directory
            with os_helper.EnvironmentVarGuard() as env:
                env['PATH'] = ''
                with mock.patch(
                    'distutils.spawn.os.confstr', return_value=tmp_dir, create=True
                ), mock.patch('distutils.spawn.os.defpath', tmp_dir):
                    rv = find_executable(program)
                    assert rv is None

                    # look in current directory
                    with os_helper.change_cwd(tmp_dir):
                        rv = find_executable(program)
                        assert rv == program

            # PATH=':': explicitly looks in the current directory
            with os_helper.EnvironmentVarGuard() as env:
                env['PATH'] = os.pathsep
                with mock.patch(
                    'distutils.spawn.os.confstr', return_value='', create=True
                ), mock.patch('distutils.spawn.os.defpath', ''):
                    rv = find_executable(program)
                    assert rv is None

                    # look in current directory
                    with os_helper.change_cwd(tmp_dir):
                        rv = find_executable(program)
                        assert rv == program

            # missing PATH: test os.confstr("CS_PATH") and os.defpath
            with os_helper.EnvironmentVarGuard() as env:
                env.pop('PATH', None)

                # without confstr
                with mock.patch(
                    'distutils.spawn.os.confstr', side_effect=ValueError, create=True
                ), mock.patch('distutils.spawn.os.defpath', tmp_dir):
                    rv = find_executable(program)
                    assert rv == filename

                # with confstr
                with mock.patch(
                    'distutils.spawn.os.confstr', return_value=tmp_dir, create=True
                ), mock.patch('distutils.spawn.os.defpath', ''):
                    rv = find_executable(program)
                    assert rv == filename

    def test_spawn_missing_exe(self):
        with pytest.raises(DistutilsExecError) as ctx:
            spawn(['does-not-exist'])
        assert "command 'does-not-exist' failed" in str(ctx.value)
