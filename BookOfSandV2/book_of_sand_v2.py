"""
TUNIO 2023
Book Of Sands V2
"""

import numpy as np
import threading
import requests
import random
import queue
import time
import os


#%% SETUP
gutenberg_url="https://mirror2.sandyriver.net/pub/gutenberg/cache/epub/" # Mirror
# gutenberg_url="https://www.gutenberg.org/" # OG
max_num_books = 71330 # 58000


#%% UTILS

def request_book(book_num):
    """
    GETs a book, indexed by project gutenberg 'book_num', with nice headers.
    Return the raw request response
    """
    book_num = str(book_num)
    book_base_url = gutenberg_url + book_num
    book_text_url = book_base_url + "/pg[booknumhere].txt.utf8" .replace("[booknumhere]", book_num)
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Accept-Encoding": "unicode",
               "Accept-Language": "en-US,en;1=0.5",
               "Cookie": "bonus=id7460; session_id=7c7d019c522c8362f49d8b61302af1815280a0c5",
               "DNT": "1",
               "HOST": "www.gutenberg.org",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
               }
    r = requests.get(book_text_url, headers=headers)
    return r


def get_meta(book_lines):
    """
    Parses lines of book to extract the book meta data
    Returns title, author, release_date, language strings
    """
    title, author, release_date, language = "    "

    for line in book_lines:
        if "Title:" in line:
            title = line.strip()

        if "Author:" in line:
            author = line.strip()

        if "Release date:" in line:
            release_date = line.strip()

        if "Release Date:" in line:
            release_date = line.strip()

        if "Language:" in line:
            language = line.strip()

    release_date = release_date.split("[EBook")[0].split("[eBook")[0].strip()

    return title, author, release_date, language


def organize_book(r):
    """
    Process the raw request response
    Returns book meta_data, taw string of entire book, and lines of the book,
    """
    book_str = r.content.decode('utf-8')
    book_lines = book_str.splitlines()
    meta_data = get_meta(book_lines) # title, author, release_date, language
    return meta_data, book_str, book_lines,


def get_random_book():
    """
    Pick a random book from the gutenberg library and
    returns book_num, book meta_data, full string of book, and book_lines
    """
    book_num = np.random.randint(max_num_books)
    r = request_book(book_num)

    while r.status_code == 404:
        time.sleep(1)
        book_num = np.random.randint(max_num_books)
        r = request_book(book_num)

    meta_data, book_str, book_lines, = organize_book(r)

    return book_num, meta_data, book_str, book_lines,


def get_page(book_lines, page_len=27):
    """
    Select a page, with number of lines equal to page_len from book_lines
    and return those lines as list of strings
    """
    header = "*** START OF"
    header2 = "***START OF"
    footer = "*** END OF"
    footer2 = "***END OF"

    start_line_no = [idx for idx, s in enumerate(book_lines) if header in s or header2 in s][0]
    end_line_no = [idx for idx, s in enumerate(book_lines) if footer in s or footer2 in s][0]
    random_line = random.randint(start_line_no + 20, max(end_line_no - 20 - page_len, start_line_no + 20))
    random_page_lines = book_lines[random_line : random_line + page_len]

    return random_page_lines


def format_page(meta_data, random_page_lines):
    """
    Makes a single string of random page and meta data
    Ready to be rendered as single block of text
    """
    page = ""
    for line in meta_data:
        page += line + "\n"
    page += "\n\n"
    for line in random_page_lines:
        page += line + "\n"
    return page


def clear():
    """
    Utility to clear the console before displaying next page
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def get_formatted_page_from_random_book():
    """
    Returns a random page from a random book in gutenberg library
    Nicely formatted to be rendered
    """
    book_num, meta_data, book_str, book_lines, = get_random_book()
    random_page_lines = get_page(book_lines, page_len=30)
    page = format_page(meta_data, random_page_lines)
    return page


#%% PAGE BUFFER UTILS

def random_page_thread_worker(ready_page_queue):
    """
    repeatedly requests and adds pages to queue
    blocks if the queue is full
    terminates if 'keep_going' flag is set to false
    """
    t = threading.current_thread()
    while getattr(t, "keep_going", True):
        page = get_formatted_page_from_random_book()
        ready_page_queue.put(page)
        setattr(t, "done_at_least_one", True)
        time.sleep(0.5 * np.random.random())


def init_page_buffer(buflen=30):
    """
    Initializes a buffer, which is a set of workers and a queue
    workers work in parallel to fetch pages
    queue stores the results of each worker
    returns list of workers page_workers, and the queue ready_page_queue
    """
    # Setup
    assert buflen > 0, "buffer length must be at least 1!"
    page_workers = [None] * buflen
    ready_page_queue = queue.Queue(maxsize=buflen) # maxsie CAN be more than num wokers

    # Start one worker, allow it to load one page nicely
    page_workers[0] = threading.Thread(target=random_page_thread_worker, args=[ready_page_queue,],)
    page_workers[0].start()
    while not getattr(page_workers[0], "done_at_least_one", False): time.sleep(0.1)

    # Initialize requests for first few
    first_few = int(buflen*0.15)
    for i in range(1, first_few):
        page_workers[i] = threading.Thread(target=random_page_thread_worker, args=[ready_page_queue,],)
        page_workers[i].start()
        time.sleep(0.1 * np.random.random())
    time.sleep(5) # give these ones a headstart

    # Initialize the rest
    for i in range(first_few, buflen):
        page_workers[i] = threading.Thread(target=random_page_thread_worker, args=[ready_page_queue,],)
        page_workers[i].start()
    time.sleep(2) # wait a bit more for these requests to send fully

    return page_workers, ready_page_queue


def get_page_from_queue(ready_page_queue):
    """
    Fetch a page from the page buffer
    Block if no pages ready
    """
    got_this_page = ready_page_queue.get()
    return got_this_page


def shutdown_page_buffer(page_workers, ready_page_queue):
    """
    Gracefully terminates all workers and emptys buffers for the lols
    """
    for i in range(len(page_workers)):
        setattr(page_workers[i], "keep_going", False)
    del ready_page_queue


#%% Random Test
clear()
print("(TYPE: 'x' then 'ENTER' to exit)")
print("initializing...")
page_workers, ready_page_queue = init_page_buffer()
while True:
    print("loading...")
    page = get_page_from_queue(ready_page_queue)
    clear()
    print(page)
    got_key = input("\n(press enter to turn the page)")
    if got_key == 'x':
        shutdown_page_buffer(page_workers, ready_page_queue)
        break
clear()
print("goodbye")
time.sleep(1)
os._exit(os.X_OK)


#%% OLD ROUTINE
# while True:
#     print("loading...")
#     page = get_formatted_page_from_random_book()
#     clear()
#     print(page)
#     input("\n(press enter to turn the page)")


#%% NEXT STEPS
"""
. Plug this in to a nice design
.

"""