# Old-Orijin data migration tool
## Package Description
This repo contains the Orijin SDK package (in /orijin_sdk/).  Clone this repo and install with `pip install -e /path/to/repo/`

See the script `fetch_token.py` for a simple example or `demo.py` for a more in-depth guide to fully utilize this package.

## Setup
**To Run this app you should have python-3.10.1 installed.**

### Create a virtual environment (Optional):
```
py -m venv .venv
./venv/Scripts/activate
```
### Install requirements:
```
pip install -r requirements.txt
```

## Usage
If you have already set up a virtual environment, enter it again by running :
```
./venv/Scripts/activate
```

This package doesn't have a specific usage, rather it is a collection of helpful functions to make building python apps that connect to the Orijin system easier.

An example usage would be to run one of the included scripts:
```
py fetch_token.py
```