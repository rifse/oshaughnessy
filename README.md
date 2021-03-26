# Value Composites from James O'Shaughnessy's What Works on Wall Street. 
## Installation, only Ubuntu support provided.
```shell
cd; git clone https://github.com/rifse/oshaughnessy.git
cd oshaughnessy; pip3 install -r requirements.txt
```
## Get finviz data
Run `python3 data_finviz.py`.

## Get yahoo data
```shell
pip3 install selenium
```
Download geckodriver to home folder like below or [find link to newest version](https://github.com/mozilla/geckodriver/releases) and proceed:
```shell
cd; wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
```
Finally unpack geckodriver, make it executable and install firefox:
```shell
tar -xvzf geckodriver*; chmod +x geckodriver; rm geckodriver-v*
sudo apt install firefox
```
Run `python3 data_yahoo.py`.

## Calculate VCs (not complete, missing BUYBACK YIELD).
```shell
python3 oshaughnessy.py
```
