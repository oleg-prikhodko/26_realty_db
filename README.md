# Real Estate Site

Real estate advertisments site with filtering and pagination support

# Quickstart

To set it up for local browsing, install dependencies:
```bash
$ pip install -r requirements.txt
```
Then, create and fill DB with [sample data](https://devman.org/fshare/1503424990/3/) (json filepath argument is used to load data from it, defaults to __ads.json__):
```bash
$ python persistence.py --filepath <json ads filepath>
```
Finally, launch the server:
```bash
$ python server.py
```
Site will be available at [http://localhost:5000]()


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
