# BBB.org Scraper: A data mining project!

## Current Features

## Installation

Create a virtual environment if you want to, it's generally not a bad idea.

Use `pip install -r requirements.txt` to fix dependency issues

## Usage
set up the dependencies, edit `internal_config.py` if the SQL database user is not `root`, then run

    python3 main.py CATEGORY

Enter SQL password when prompted

### Optional CLI arguments
`-v` prints verbose output (i.e., outputs debug logs into terminal)  
`-c` uses a config file instead of reading CLI arguments (**not implemented yet**)  
`-l FILENAME` or `--log FILENAME` outputs program logs into a file (default is log.txt)  
`-t TYPE` or `--type TYPE` output to file type (default is SQL. only SQL is implemented at the moment)

`--lim INT` limit the number of companies scraped (**not implemented yet**)  
`--loc LOCATION` scrape companies from a certain country (default: US)
`--acc` get accredited companies only
`--all` scrape all companies in all categories (**not implemented yet**)  

## Database information
![ERD!](erd.png)

----

## current problems
* something is off with the number of companies scraped by categoryscraper...
* Only output to SQL is implemented
* does not handle full hours of operation
* does not check for multiple locations (will produce duplicates instead)
* only the `business_profile` and `categories` tables are populated
* some issues with scraping the company website and BBB rating 

## planned features
* support for scraping charities
* scrape everything option

## version history
2021 apr 02 - now handles arguments!
2021 feb 21 - only scrapes some companies from one category. output only to json

## Credits
* Social media preview: Photo by Markus Spiske on Unsplash
