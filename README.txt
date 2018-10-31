This repository provides the tools to scrape Subreddits via python and store them in a csv file. Much of the content comes from https://www.datacamp.com/community/tutorials/scraping-reddit-python-scrapy, but I made enough modification that I think it deserves its own github repo.

The main changes that I made were:
 - shell.nix file for consistent dependencies using the nix package manager
 - Made the script robust to addition of promotional content on the Subreddit
 - Give user easy control over number of posts rather than number of pages 
 - Other organizational changes to the structure of the code

To run the software: 
 1. install nix by running `curl https://nixos.org/nix/install | sh`
   (or just install the dependencies via your favorite package manager)
 2. enter the nix shell by running `nix-shell shell.nix`
 3. edit the variables in scrape.py to your liking (eg subreddit and post count)
 4. run `python scrape.py` to generate scraped.csv
 5. open scraped.csv with a valid encoding -- for me what works is Character set as 'System' and Language as 'English (USA)'
