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
"""
Manages the settings that are used while running
"""
from PyQt5.QtCore import QSettings
import os


class Settings:
    """
    Holds the settings for sarge
    """

    def __init__(self):
        self.organisation = 'Bitcast'
        self.application = 'sarge'
        self.config = QSettings(self.organisation, self.application)
        changed = False
        if not self.config.contains('columns'):
            changed = True
            self.config.setValue('columns', 2)

        if not self.config.contains('files'):
            changed = True
            self.config.setValue('files', ['~/music/jingles/Station ID III (2017).mp3',
                                           '~/music/jingles/This is UCT Radio (Voice Only).mp3',
                                           '~/music/jingles/Transition Effect.mp3',
                                           '~/music/jingles/Turn It Up ( The Soundtrack to Your Campus life).mp3'])

        if not self.config.contains('music_directory'):
            changed = True
            self.config.setValue('music_directory', '~/music/library')

        if not self.config.contains('sample_rate'):
            changed = True
            self.config.setValue('sample_rate', 48000)

        if not self.config.contains("channels"):
            changed = True
            self.config.setValue("channels", "Mono")

        if changed:
            del self.config
            self.config = QSettings(self.organisation, self.application)

    @property
    def sarge_columns(self):
        """ returns number of columns """
        return self.config.value('columns', type=int)

    @sarge_columns.setter
    def sarge_columns(self, columns):
        self.config.setValue("columns", columns)
        del self.config
        self.config = QSettings(self.organisation, self.application)

    @property
    def music_directory(self):
        """ Returns the directory of the voice """
        directory = self.config.value('music_directory', type=str)
        if directory.startswith("~"):
            return os.path.expanduser(directory)
        return directory

    @music_directory.setter
    def music_directory(self, directory):
        self.config.setValue("music_directory", directory)
        del self.config
        self.config = QSettings(self.organisation, self.application)

    @property
    def sarge_files(self):
        all_files = self.config.value("files")
        return all_files

    @sarge_files.setter
    def sarge_files(self, files):
        self.config.setValue("files", files)
        del self.config
        self.config = QSettings(self.organisation, self.application)

    @property
    def sarge_player_channel(self):
        """ Returns details on the play of the songs"""
        channels = self.config.value("channels", type=int)
        return channels

    @sarge_player_channel.setter
    def sarge_player_channel(self, channel):
        self.config.setValue("channels", channel)
        del self.config
        self.config = QSettings(self.organisation, self.application)

    @property
    def sarge_player_sample_rate(self):
        """ Returns details on the play of the songs"""
        sample_rate = self.config.value("sample_rate", type=int)
        return sample_rate

    @sarge_player_sample_rate.setter
    def sarge_player_sample_rate(self, sample_rate):
        self.config.setValue("sample_rate", sample_rate)
        del self.config
        self.config = QSettings(self.organisation, self.application)
