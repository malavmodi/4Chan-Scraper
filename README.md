# 4Chan-Scraper
Scrapes a given board catalog on 4Chan for all comments, files, and associated metadata with help of the BASC 4Chan Python Library.

Installation:
------------
git clone https://github.com/malavmodi/4Chan-Scraper.git <br/>
pip3 install -r requirements.txt <br/>

Commands:
---------
**--board_name**: Board from 4Chan to Scrape (Required)<br/>
**--num_threads**: Number of threads to scrape (Required)<br/>
**--debug**: Additional log output (Optional / Case Insensitive)<br/>

Example Usage:
--------------
* Scraping the first 5 threads of /pol/ <br/>
  * **python 4chan_scraper.py --board_name 'pol' --num_threads 5 --debug 'false'**  <br/>
  
For additional information on usage, run **python 4chan_scraper.py -h** to check options.

Runtime:
-------
When running the script, it will create a folder with all associated data in the current working directory of execution in a hierarchy structure as such:
          
* Thread ID with Subject (if not Null) (**Folder**) <br/>
  * Thread ID files (**Folder**)
    * File Data <br/>
  * CSV with comments/replies from posts <br/>
  * JSON formatted output of thread <br/>
  * File Metadata <br/>
  * Thread Metadata <br/>
              
              
              
