# Copyright (C) 2009-2015 Contributors as noted in the AUTHORS file
#
# This file is part of Autopilot.
#
# Autopilot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Autopilot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Autopilot.  If not, see <http://www.gnu.org/licenses/>.


from appargs import ApplicationArguments
from lib.manuscript.manuscript import Manuscript
import lib.reporting.logger as logger
from lib.reporting.logger import Logger
from lib.app.bootstrap import start_app
from lib.instructions.base.instructions import Instructions


class TestEngine(object):

    def __init__(self):
        self.appargs = ApplicationArguments()
        logger.set_debug(self.appargs.degbug())
        self.manuscript = Manuscript(self.appargs.manuscripts(), self.appargs.paths())
        if self.appargs.autoexit():
            self.manuscript.add_autoexit_instruction()

    def _log_effective_manuscript(self):
        print "%s %s\n" % (self.appargs.myname(), self.appargs.myversion())
        print "Application under test = %s" % self.appargs.program()
        print "Effective manuscript:"
        print "-----------------------------------------"
        print str(self.manuscript)
        print "-----------------------------------------"

    def _test(self):
        Logger.set_path(self.manuscript.get_log_path())
        Logger.set_log_dialog_descriptions(self.appargs.log_dialog_descriptions())
        Logger.add_section("Manuscript", str(self.manuscript))
        instructions = Instructions(self.manuscript, self.appargs.timedelay())
        start_app(instructions, self.appargs.program())

    def run(self):
        if self.appargs.investigate():
            self._log_effective_manuscript()
        else:
            try:
                self._test()
            finally:
                Logger.log()
        return True


if __name__ == '__main__':
    TestEngine().run()
