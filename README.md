# Simple Purchasing Bot

A simple bot to purchase things on the internet.

## Usage

### Prerequisites

- install a selenium webdriver. Currently, only the firefox webdriver is supported. 
It can be installed on macos with `brew install geckodriver`, or on ubuntu with: `sudo apt install firefox-geckodriver`.
- python 3, and pip are both required
- Install the dependencies found in `requirements.txt` - `pip3 install -r requirements.txt`.

### Configuration

The configuration settings will be loaded from `settings.yaml` in the project's root directory. 
An example of this file is given in `settings.yaml.example`. 

| Configuration Name      | Type    | Description                                                  |
| ----------------------- | ------- | ------------------------------------------------------------ |
| `productPollingSeconds` | float   | The amount of time to wait between product availability checks. |
| `productLink`           | string  | The product's url. Currently only amazon urls will work.     |
| `headless`              | boolean | If true, this program will run silently in the background with a headless browser. Otherwise, a browser window will be displayed, and remotely controlled by this program (useful for debugging). |

In addition to these configurations, the script also requires the user's site credentials to make purchases. These are given as command line arguments

### Running

Simply run the `main.py` script, passing in your login credentials as command line arguments:

`main.py --username=<your_user_name> --password=<your_password>`



