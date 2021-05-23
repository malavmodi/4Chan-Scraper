# 4Chan-Scraper
Scrapes a given board catalog on 4Chan for all comments, files, and associated metadata with help of the BASC 4Chan Python Library.

**UPDATE for Python 3.9+**/ Script Failure
---------------------------
1. Windows Navigation:
```
C:\Users\USER\AppData\Local\Programs\Python\Python3x\Lib\site-packages\basc_py4chan\util.py
```
1. LINUX Navigation:
```
/usr/lib/site-packages/python3.x/site-packages/basc_py4chan/util.py
```
2. Rename HTMLParser dependency from _HTMLParser_

```python
# HTML parser was renamed in python 3.x
try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser
_parser = html.HTMLParser()
```
to the newly named dependency _html_:
```python
# HTML parser was renamed in python 3.x
import html
_parser = html
```

Installation:
------------
Download .zip from the github repo or clone using
```
git clone https://github.com/malavmodi/4Chan-Scraper.git
```
as well as install the required dependencies with pip:
```
pip3 install -r requirements.txt 
```
Commands:
---------
1. **--board_name**
   - Board from 4Chan to Scrape (Required)
2. **--num_threads**: 
   - Number of threads to scrape (Required)
3. **--debug**:
   - Additional log output (Optional / Case Insensitive)

Example Usage:
--------------
_NOTE: For additional information on usage, run **python 4chan_scraper.py -h** to check options._ <br>

* Scraping the first 5 threads of /pol/ 
   - **python 4chan_scraper.py --board_name "pol" --num_threads 5 --debug "False"**  <br/>
  
 

Runtime:
-------
When running the script, it will create a folder with all associated data in the current working directory in a hierarchial structure as such:
          
* Thread ID with Subject (if not Null) (**Folder**) <br/>
  * Thread ID files (**Folder**)
    * File Data <br/>
  * CSV with comments/replies from posts <br/>
  * JSON formatted output of thread <br/>
  * File Metadata <br/>
  * Thread Metadata <br/>
