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
import os
import mutagen

def get_key(metadata, key, default=None):
    try:
        return metadata[key][0]
    except KeyError:
        return default

def get_metadata(filename):
    metadata = mutagen.File(filename, easy=True)
    if metadata == None:
        return None
    length = metadata.info.length
    return {
        'title': get_key(metadata, 'title', os.path.basename(filename)),
        'artist': get_key(metadata, 'artist'),
        'length': '{:0>2.0f}:{:0>2.0f}'.format(length//60, length%60),
        'file': filename
    }
