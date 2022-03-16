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
            self.config.setValue('files', ['~/My Music/jingles/Station ID III (2017).mp3',
                                           '~/My Music/jingles/This is UCT Radio (Voice Only).mp3',
                                           '~/My Music/jingles/Transition Effect.mp3',
                                           '~/My Music/jingles/Turn It Up ( The Soundtrack to Your Campus life).mp3'])

        if not self.config.contains('music_directory'):
            changed = True
            self.config.setValue('music_directory', '~/music/2015-2016 music')

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
        return self.config.value('columns', type=str)

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
        channels = self.config.value("channels")
        return channels

    @sarge_player_channel.setter
    def sarge_player_channel(self, channel):
        self.config.setValue("channels", channel)
        del self.config
        self.config = QSettings(self.organisation, self.application)

    @property
    def sarge_player_sample_rate(self):
        """ Returns details on the play of the songs"""
        sample_rate = self.config.value("sample_rate")
        return sample_rate

    @sarge_player_sample_rate.setter
    def sarge_player_sample_rate(self, sample_rate):
        self.config.setValue("sample_rate", sample_rate)
        del self.config
        self.config = QSettings(self.organisation, self.application)
