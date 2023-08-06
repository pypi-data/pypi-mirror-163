#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2012-2017 DESY, Jan Kotanski <jkotan@mail.desy.de>
#
#    nexdatas is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    nexdatas is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with nexdatas.  If not, see <http://www.gnu.org/licenses/>.
# \package test nexdatas
# \file DBFieldTagServerH5PY_test.py
# unittests for field Tags running Tango Server
#

import unittest
import PyTango

try:
    import ServerSetUp
except Exception:
    from . import ServerSetUp

try:
    import DBFieldTagWriterH5PY_test
except Exception:
    from . import DBFieldTagWriterH5PY_test

try:
    from ProxyHelper import ProxyHelper
except Exception:
    from .ProxyHelper import ProxyHelper


# test fixture


class DBFieldTagServerH5PYTest(
        DBFieldTagWriterH5PY_test.DBFieldTagWriterH5PYTest):
    # server counter
    serverCounter = 0

    # constructor
    # \param methodName name of the test method
    def __init__(self, methodName):
        DBFieldTagWriterH5PY_test.DBFieldTagWriterH5PYTest.__init__(
            self, methodName)

        DBFieldTagServerH5PYTest.serverCounter += 1
        sins = self.__class__.__name__ + \
            "%s" % DBFieldTagServerH5PYTest.serverCounter
        self._sv = ServerSetUp.ServerSetUp("testp09/testtdw/" + sins, sins)

        self.__status = {
            PyTango.DevState.OFF: "Not Initialized",
            PyTango.DevState.ON: "Ready",
            PyTango.DevState.OPEN: "File Open",
            PyTango.DevState.EXTRACT: "Entry Open",
            PyTango.DevState.RUNNING: "Writing ...",
            PyTango.DevState.FAULT: "Error",
        }
#        self._counter =  [1, 2]
#        self._fcounter =  [1.1,-2.4,6.54,-8.456,9.456,-0.46545]

    # test starter
    # \brief Common set up of Tango Server
    def setUp(self):
        DBFieldTagWriterH5PY_test.DBFieldTagWriterH5PYTest.setUp(self)
        self._sv.setUp()
        print("SEED = %s" % self.seed)
        print("CHECKER SEED = %s" % self._sc.seed)

    # test closer
    # \brief Common tear down oif Tango Server
    def tearDown(self):
        DBFieldTagWriterH5PY_test.DBFieldTagWriterH5PYTest.tearDown(self)
        self._sv.tearDown()

    def setProp(self, rc, name, value):
        db = PyTango.Database()
        name = "" + name[0].upper() + name[1:]
        db.put_device_property(
            self._sv.new_device_info_writer.name,
            {name: value})
        rc.Init()

    # opens writer
    # \param fname file name
    # \param xml XML settings
    # \param json JSON Record with client settings
    # \returns Tango Data Writer proxy instance
    def openWriter(self, fname, xml, json=None):
        tdw = PyTango.DeviceProxy(self._sv.new_device_info_writer.name)
        self.assertTrue(ProxyHelper.wait(tdw, 10000))
        self.setProp(tdw, "writer", "h5py")
        tdw.FileName = fname
        self.assertEqual(tdw.state(), PyTango.DevState.ON)
        self.assertEqual(tdw.status(), self.__status[tdw.state()])

        tdw.OpenFile()

        self.assertEqual(tdw.state(), PyTango.DevState.OPEN)
        self.assertEqual(tdw.status(), self.__status[tdw.state()])

        tdw.XMLSettings = xml
        self.assertEqual(tdw.state(), PyTango.DevState.OPEN)
        self.assertEqual(tdw.status(), self.__status[tdw.state()])
        if json:
            tdw.JSONRecord = json
        tdw.OpenEntry()
        self.assertEqual(tdw.state(), PyTango.DevState.EXTRACT)
        self.assertEqual(tdw.status(), self.__status[tdw.state()])
        return tdw

    # closes writer
    # \param tdw Tango Data Writer proxy instance
    # \param json JSON Record with client settings
    def closeWriter(self, tdw, json=None):
        self.assertEqual(tdw.state(), PyTango.DevState.EXTRACT)
        self.assertEqual(tdw.status(), self.__status[tdw.state()])

        if json:
            tdw.JSONRecord = json
        tdw.CloseEntry()
        self.assertEqual(tdw.state(), PyTango.DevState.OPEN)
        self.assertEqual(tdw.status(), self.__status[tdw.state()])

        tdw.CloseFile()
        self.assertEqual(tdw.state(), PyTango.DevState.ON)
        self.assertEqual(tdw.status(), self.__status[tdw.state()])

    # performs one record step
    def record(self, tdw, string):
        tdw.Record(string)


if __name__ == '__main__':
    unittest.main()
