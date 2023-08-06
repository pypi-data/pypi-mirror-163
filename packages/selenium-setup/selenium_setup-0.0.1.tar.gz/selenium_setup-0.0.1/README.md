# selenium_setup

[![pypi](https://img.shields.io/pypi/v/selenium_setup?color=%2334D058)](https://pypi.org/project/selenium_setup/)

## install

```shell
pip install selenium_setup
```

## CLI

### download default version driver and unzip to CWD  

```shell
python -m selenium_setup
```

```console
chrome ver = '104.0.5112.79'
linux64
downloading to: /path/to/chromedriver_linux64--104.0.5112.79.zip
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.1/7.1 MB 200.8 kB/s
```

### list 10 links of some latest versions

```shell
python -m selenium_setup --list
```

```console
chrome linux64:
  105.0.5195.19  https://chromedriver.storage.googleapis.com/105.0.5195.19/chromedriver_linux64.zip
  104.0.5112.79  https://chromedriver.storage.googleapis.com/104.0.5112.79/chromedriver_linux64.zip
  103.0.5060.134 https://chromedriver.storage.googleapis.com/103.0.5060.134/chromedriver_linux64.zip
  ...
```

### use with version

```shell
python -m selenium_setup --ver ...
```
