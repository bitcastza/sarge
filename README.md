# Sarge

Sarge is a simple live-assist radio playout system. It is designed to be simple
to use and does not include many of the complex features provided in larger
automation systems such as [Rivendell](http://rivendellaudio.org/).

## Installation

```
sudo apt install pre-commit
git clone https://gitlab.com/bitcast/sarge
cd sarge
pre-commit install
virtualenv -p python3 pyenv
pyenv/bin/pip install -r requirements.txt
pyenv/bin/python -m sarge
```
