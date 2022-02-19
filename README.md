# Crawl pepper.pl website using Python and Selenium tools

A sample script that downloads data from the pepper.pl website and saves this data to a text file and xml file.

The script goes through a certain number of pagination pages.

The script writes to files:
- Titles special offer
- Prices
- Urls
- The name of the store
- Thumbnail address and creates addresses for photos in higher resolution
- W przypadku braku ceny lub nazwy sklepu generuję wyjątek w pliku.