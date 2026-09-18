# Assignment---The-Polite-Scraper
FlyRank Assignment

# Books to Scrape

A small Python web scraper built for practicing respectful and reliable web-data collection.

## Target Classification

**Site:** [Books to Scrape](https://books.toscrape.com/)

**Why:** Books to Scrape is a fictional bookstore created as a safe sandbox for beginners to practice web scraping and for developers to validate scraping technologies.

**Scope:** The scraper will collect data from the first 3 catalogue pages only. Each catalogue page contains up to 20 books, so the target is 60 books in total.

**Data collected:** Book title, price, availability, rating, and other fields required by the assignment.

**Why this is appropriate:** This target is appropriate because the site explicitly identifies itself as a scraping sandbox designed for scraping practice rather than a real commercial bookstore.

## Robots.txt Check

Requested:

`https://books.toscrape.com/robots.txt`

Result:

**no robots file found**

The missing `robots.txt` file was recorded as a site observation, not as permission to scrape.

