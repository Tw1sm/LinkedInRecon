LinkedInRecon
=============
## Overview ##
Scrape employee names/titles off LinkedIn and output to a CSV file. Essentially a python port of this Burpsuite extension by Carrie Roberts: https://github.com/clr2of8/GatherContacts.

## Install ##
```bash
pip3 install -r requirements.txt
```
## Usage ##
usage: linkedinrecon.py [-h] -c COMPANY [-p PAGES] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -c COMPANY, --company COMPANY
                        Target company
  -p PAGES, --pages PAGES
                        Number of result pages to iterate through (100 per
                        page). Default of 5
  -o OUTPUT, --output OUTPUT
                        name and path of output csv
