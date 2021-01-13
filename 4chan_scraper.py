#!usr/bin/env python3
#-*- coding: utf-8 -*-

#Dependencies
from datetime import datetime
import urllib.request
import basc_py4chan
import argparse  
import timeit
import json
import csv 
import os

def get_board_info(board_name):
    """Gets Board Information of a given 4Chan Board"""
    board = basc_py4chan.Board(board_name)
    board.refresh_cache(if_want_update = True)
    all_thread_ids = board.get_all_thread_ids() #CLI argument for number of threads to scrape
    board_metadata = (f'Board Title: {board.title}\n'
                      f'Number of Threads Currently: {len(all_thread_ids)}\n'
                      f'Number of Threads to Scrape: {args.num_threads}\n')
    return board, all_thread_ids, board_metadata

def write_thread_data(thread, filepath):
    """Gets information about a given 4Chan thread"""
    if thread.expand() != None:
        thread.expand()
    if thread.update(force = True) != None:
        num_new_posts = thread.update(force = True)
    with open(filepath, 'a', encoding = 'utf-8') as f:
        f.write((f"Thread ID: {thread_id}\n"
                 f"Sticky?: {thread.sticky if thread.sticky != None else 'None'}\n"
                 f"Closed?: {thread.closed}\n"
                 f"Archived: {thread.archived}\n"
                 f"Number of Posts on Thread: {len(thread.posts)}\n"
                 f"JSON URL: {basc_py4chan.Url('pol').thread_api_url(thread_id)}\n"
                 f"Number of Replies on Thread: {len(thread.replies)}\n"
                 f"Number of New Posts: {num_new_posts if num_new_posts > 0 else 0}\n"))

def download_file(post, url, path):
    """Downloads 4Chan Files (Mostly Image-Based)"""
    try:
        urllib.request.urlretrieve(post.file_url, path)
    except Exception as e:
        if args.debug:
            print(f"Error downloading {post.filename}.\n")

def write_file_data(post, filepath): 
    """Gets File Metadata of a given 4Chan Post / File Downloader"""
    with open(filepath, 'a', encoding = 'utf-8') as f:
        if post.has_file:
            f.write((f'Filename: {post.filename}\n'
            f'File Size: {post.file_size} bytes\n'
            f'MD5 Hash: {post.file_md5_hex}\n'
            f'File URL: {post.file_url}\n'
            f'Thumbnail URL: {post.thumbnail_url}\n\n'))
        f.close()

def make_safe_filename(string):
    """Creates a string safe for file naming conventions"""
    safe_char = lambda c: c if c.isalnum() else "_"
    return "".join(safe_char(c) for c in string).rstrip("_")

def download_json_thread(local_filename, url):
    """Download the given JSON file, and pretty-print before outputted"""
    with open(local_filename, 'w', encoding = 'utf-8') as json_file:
        try:
            thread_json_data = json.loads(urllib.request.urlopen(url).read())
            json_file.write(json.dumps(thread_json_data, sort_keys = False, indent = 4, separators=(',', ': ')))
            json_file.close()
        except Exception as e:
            if args.debug:
                print(f'Error downloading {local_filename}.\n')

def mkdir(path, mode):
    """Makes a directory within the filesystem"""
    try:
        if not(os.path.exists(path)):
            os.mkdir(path, mode)
        else:
            if args.debug:
                print(f'"{path}" already created.')
    except Exception as e:
        if args.debug:
            print(f'Failed to create directory {path}.\n')

def write_comments_csv(post, filepath):
    """Create CSV and writes 4Chan comments and replies to it"""
    comment = post.text_comment.encode('utf-8').decode('utf-8')
    with open(filepath, 'a', newline = '', encoding = 'utf-8') as f:
        writer = csv.writer(f)
        if os.stat(filepath).st_size == 0:
            writer.writerow(['post_id', 'date_time', 'subject', 'comment/reply', 'name', 'is_op?', 'url'])
        writer.writerow([post.post_id, post.datetime.strftime("%b-%d-%Y, %H:%M:%S"), post.subject if post.subject != None else 'No Subject',
        '(REPLY) ' + comment if ">>" in comment and not(post.is_op) else comment, post.name.encode('utf-8').decode('utf-8') if post.name != None else 'No Name', 
        post.is_op, post.semantic_url])
    f.close()   
                         
#TODO: 
    # Multithread --> not too important rn
    # Update a thread folder if new data is there ---> important
    #possible bugs with duplicate folders?

if __name__ == "__main__":
    #Parse CLI for Board Name / Toggle Debugging
    parser = argparse.ArgumentParser()
    parser.add_argument("--board_name", type = str, help = "4Chan Board Name", required = True, default = 'pol')
    parser.add_argument("--num_threads", type = int, help = "Number of threads to scrape on 4Chan Board", required = True, choices = range(1, 203), default = 5)
    parser.add_argument("--debug", type = bool, help = "Turn debugging on", required = False, default = False)
    args = parser.parse_args()

    #Get Board Information and Begin Scrape
    board, all_thread_ids, board_metadata = get_board_info(args.board_name)
    print(f'\nBeginning 4Chan Catalog Scrape on /{board.name}/', '\n---------------------------------------')
    print('Current Date and Time:', datetime.now().strftime("%b-%d-%Y, %H:%M:%S"))
    #Parse again for number of threads to scrape

    #Defining file structure paths
    board_name_dir = f'{board.name}/'

    #Print Board Information
    print(board_metadata)
    print('Processing...\n')

    if args.debug:
        print('Subject Names Scraped:\n', '-------------------------')

    #Start runtime execution timer
    start = timeit.default_timer()

    #Create directory for board name
    mkdir(board_name_dir, 0o0666)

    #Check if a given thread is not 404'd
    if board.thread_exists:
        #Loop for each thread in the thread ID list
        for thread_id in all_thread_ids[0: args.num_threads]:       
            thread = board.get_thread(thread_id)

            #Defining additional file structure paths
            if thread.posts != None:
                subject = thread.posts[0].subject
                if args.debug:
                    print(subject)
                if subject != None:
                    thread_id_dir = f'{board.name}/{thread_id} - {make_safe_filename(subject)}'
                else:
                    thread_id_dir = f'{board.name}/{thread_id} - No Subject'
                
                images_dir = f'{thread_id_dir}/{thread_id} files/'

            #Create directory structure for thread
            mkdir(thread_id_dir, 0o0666)
            mkdir(images_dir, 0o0666)  
                        
            # Download JSON for thread via catalog URL
            json_url = basc_py4chan.Url(args.board_name).thread_api_url(thread_id)
            download_json_thread(f'{thread_id_dir}/{thread_id}.json', json_url)            
            
            # Write thread information to .txt
            write_thread_data(thread, f'{thread_id_dir}/{thread_id} - thread metadata.txt')

            #Post Information
            if thread.posts != None:
                for post in thread.posts:

                    #Write comments and replies to CSV file
                    write_comments_csv(post, f'{thread_id_dir}/{thread_id} - comments & replies.csv')

                    #Write file metadata to .txt
                    if post.has_file:
                        write_file_data(post, f'{thread_id_dir}/{thread_id} - file metadata.txt')
                        download_file(post, post.file_url, f'{images_dir}' + post.filename)
    
    #Finish scraping / end runtime execution timer
    end = timeit.default_timer()
    print('\nScraping Complete!')
    print("Total Runtime Execution:", round(end - start, 3), "seconds")