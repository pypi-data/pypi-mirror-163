
# Proxy Ninja
Python3 Module to get https or socks(4) proxies by scraping the web.
## Installation
Before installing the module , please install the ChromiumDriver as following debian/kali
```bash
    sudo apt-get update && sudo apt-get full-upgrade -y
    sudo apt-get install chromium-driver
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the module.
if not installed, install it using the following command.
```bash
sudo apt-get install python3-pip
```

> It is advised to install the python requirements in a virtual environment, for that install the venv package.

```bash
    python3 -m pip install venv
    python3 -m venv env
    source env/bin/activate
```
After that run the following commands:
```bash
  python3 -m pip install <pkg> -U
```
    
## Usage/Examples
-----------------------------------------
#### Usage:

==> Download the proxies.

```python
#!/usr/bin/python3
from proxy_ninja import fetch_proxies

fetch_proxies(PROXY_TYPE, OUTPUT_FILENAME, OUTPUT_FORMAT)
```
- PROXY_TYPE: https/socks
- OUTPUT_FILENAME: Enter the filename
- OUTPUT_FORMAT: txt/json

-- proxies gonna save in parent dir.

#### Example:
```python
#!/usr/bin/python3
from proxy_ninja import fetch_proxies

fetch_proxies("socks", "socks_proxy", "json")
```

==> Get proxies as json
```python
#!/usr/bin/python3
from proxy_ninja import proxies_json

json_list = proxies_json(PROXY_TYPE)
print(json_list)
```
- PROXY_TYPE: https/socks

> This will gonna return a list.

#### Example:
```python
#!/usr/bin/python3
from proxy_ninja import proxies_json

json_list = proxies_json("https")
print(json_list)
```

## Features

- ChromeDriver to scrape the site.
- Stealth Profle implmented.
- Save output in txt or json format.
- User Friendly. :D


## License

[MIT](https://choosealicense.com/licenses/mit/)


## Feedback

If you have any feedback, please reach out to us at akalucifr@protonmail.ch
