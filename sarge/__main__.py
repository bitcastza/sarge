###########################################################################
# Sarge is Copyright (C) 2021 Kyle Robbertze <kyle@bitcast.co.za>
#
# Sarge is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3, or
# any later version as published by the Free Software Foundation.
#
# Sarge is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sarge. If not, see <http://www.gnu.org/licenses/>.
###########################################################################
from .interface import UserInterface


def gui():
    gui = UserInterface()
    gui.run()


if __name__ == "__main__":
    gui()
