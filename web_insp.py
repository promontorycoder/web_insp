#! /usr/bin/env python3

# Import GUI modules
from tkinter import *
from tqdm import tqdm

# Import web page data search function modules
import builtwith
import whois
from bs4 import BeautifulSoup

# Import operating system function module(s)
import re
import os
import time

# Import web page gathering modules
import requests
import urllib
import urllib.request
from urllib.request import urlopen
from urllib.parse import urljoin, urlparse

# Import image manipulation modules
from PIL import Image, ImageTk

# Import data file and database modules
import json


# Establish our GUI
root = Tk()

# Define our GUI
root.geometry('800x900')
root.configure(bg='gray7')
root.resizable(1,1)
root.title("Web Inspector")


# Create Functions

# Function to feed text from os commands to tkinter text widget    
def get_info(arg):
    
    print(tow.get("1.0", "current lineend"))
    

# Function to print builtwith and whois info to tkinter text widget
def info(url):
    
    # Define variables for builtwith and whois module implemented data
    build_info = builtwith.parse(url)
    whois_info = whois.whois(url)
    
    # Collect variable data and insert in tkinter text widget
    tow.insert(END, "Information for the following web address: \n")
    tow.insert(END, url)
    tow.insert(END, '\n')
    tow.insert(END, build_info)
    tow.insert(END, '\n')
    tow.insert(END, whois_info)


# Function to print html title search results to tkinter text widget
def print_title(url):
    
    # Call module 'requests' to gather html data via url
    r = requests.get(url)
    # Store and parse gathered data via BeautifulSoup module
    soup = BeautifulSoup(r.text, 'lxml')
    
    # try / except function to gather / display title information
    try:
        web_title = soup.title.text # BeautifulSoup function for title
        tow.insert(END, '\n')
        tow.insert(END, web_title)
        
    except Exception as err:    # Handle exceptions
        tow.insert(END, '\n')
        tow.insert(END, err)    # Print error msg to tkinter text widget
        msg = "Please enter a valid file web url and try again ..."
        tow.insert(END, '\n')
        tow.insert(END, msg)


# Function to print html body text to tkinter text widget
def print_body(url):
    
    try:    
        req = requests.get(url).text
        soup = BeautifulSoup(req, 'lxml')
        
        msg = soup.get_text() # BeautifulSoup module function for html body
        
        tow.insert(END, msg)
                        
    except Exception as err:
        tow.insert(END, '\n')
        tow.insert(END, err)    # Print error msg to tkinter text widget


# Function to print html tag search results to tkinter text widget
def show_html_tags(url):
    
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
        
    try:
        for tag in soup.find_all(True): # BeautifulSoup function for all tags
            msg = tag.name
            tow.insert(END, tag.name)
            tow.insert(END, '\n')
                    
    except Exception as err:
        tow.insert(END, '\n')
        tow.insert(END, err)    


# Function to test web address connectivity and print results to tk text widget
def web_response(url):
    
    response = requests.get(url)
    
    
    if response.status_code == 200: # requests module check url status code
        tow.insert(END, '\n')
        tow.insert(END, "Successful Connection to Web Address ...")
        
    elif response.status_code == 404:
        tow.insert(END, '\n')
        tow.insert(END, "Web address: NOT FOUND ")
        
    else:
        tow.insert(END, "\nWeb address: NOT FOUND ")
            
    
# Function searches html headers and prints to tkinter text widget
def show_headers(url):
    
    response = requests.get(url)
    
    try:
        headers = response.headers # requests module function find headers
        header_content = response.headers['Content-Type']
        tow.insert(END, '\n')
        tow.insert(END, headers)
        tow.insert(END, '\n')
        tow.insert(END, header_content)
        
    except Exception as err:
        tow.insert(END, '\n')
        tow.insert(END, err)


# Function finds all url links in web page and prints to tkinter text widget
def show_urls(url):
    
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'lxml')
    
    try:
        for link in soup.find_all('a'): # BeautifulSoup find all 'a' tags (html)
            msg = link.get('href')  # qualify results with 'href' string
            tow.insert(END, msg)
            tow.insert(END, '\n')
            
    except Exception as err:
        tow.insert(END, '\n')
        tow.insert(END, err)


# Function finds all img tags in web page and prints to tkinter text widget
def get_img_tags(url):
    
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    web_images = []
    
    try:
        for item in soup.find_all('img'): # BeautifulSoup gather 'img' tags
            msg = (item['src']) # qualify results with 'src' string
            tow.insert(END, msg)
            tow.insert(END, '\n')
            web_images.append(msg)                   
            
    except Exception as err:
        tow.insert(END, '\n')
        tow.insert(END, err)
        
    return web_images


# Function finds all images in web page and downloads images to local drive
def images_main(filepath, url):
    
    imgs = get_all_images(url)      # Call slave function: get_all_images
    for img in imgs:
        download(img, filepath)         # Call slave function: download
    

# Function finds all image urls in web page and delivers to images_main
def get_all_images(url):
    
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"): # Progress bar
        img_url = img.attrs.get("src")
        if not img_url:
            continue
        img_url = urljoin(url, img_url) # Call module to create final url
        
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        if is_valid(img_url):       # Call slave function: is_valid
            urls.append(img_url)
    return urls


# Function checks if url is valid, addressable url
def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


# Function downloads target images to folder from urls via images_main
def download(url, filepath):

    if not os.path.isdir(filepath): # If file path not given, create folder
        os.makedirs(filepath)
        
    response = requests.get(url, stream=True) # Stream for large files
    # gather integer of file size
    file_size = int(response.headers.get("Content-Length", 0))
    # Separate image file name from url
    filename = os.path.join(filepath, url.split("/")[-1])
    # Create variable for storing progress of progress bar
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", 
        total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress:
            f.write(data)               # Write downloaded file to local drive
            progress.update(len(data))  # Update progress with each loop
        msg = "Downloading " + filename + " to folder ...\n"
        tow.insert(END, msg)
        tow.insert(END, "\nImage Downloads Completed ...")
            

# Function is work in progress: to open windows and show downloaded image files
def show_images(filepath):

    # Instructions for navigating pictures
    tow.insert(END, "\nMouse Left Button Click to go to next image.")
    tow.insert(END, "\nMouse Right Button Click to go to previous image.")

    # Create separate tkinter window for images
    image_win = Toplevel(root)
    image_win.title("Image")
    image_win.geometry("400x400")
    image_win.configure(bg='gray7')
        
    
    
    files = os.listdir(filepath)
    
    pics = []
    
    images_forward = []
    images_back = []
    
    for f in files:
        pics.append(filepath + f)
    
    tow.insert(END, "\nImage files contained in folder ... \n")
    tow.insert(END, filepath)
    
    for pic in pics:
        
        img = ImageTk.PhotoImage(Image.open(pic))
        images_forward.append(img)
        
    # for pic in pics:
        # tow.insert(END, pic)
        # tow.insert(END, '\n')
        
    def back(event):
        try:
            pop = images_back.pop()
            img_label.config(image = pop)
            images_forward.append(pop)
        except Exception as err:
            tow.insert(END, "\nLast Image: Left Mouse Button to Go Forward.")
    
    def forward(event):
        try:
            pop = images_forward.pop()
            img_label.config(image = pop)
            images_back.append(pop)
        except Exception as err:
            tow.insert(END, "\nLast Image: Right Mouse Button to Go Backward.")
    
    img_label = Label(image_win)
    img_label.pack(side = BOTTOM, pady = 10)        
    try:
        img_label.config(image=images_forward[0])
        
    except IndexError as err:
        tow.insert(END, err)
        tow.insert(END, "\nFolder appears to be empty ...")
    
    img_label.bind("<Button-1>", lambda event: forward(event))
    img_label.bind("<Button-3>", lambda event: back(event))
    

def search_output_text(search_criteria):
    
    idx = '1.0'
    while 1:
        idx = tow.search(search_criteria, idx, nocase=1, stopindex=END)
        if not idx: break
        lastidx = '%s+%dc' % (idx, len(s))
        tow.tag_add('found', idx, lastidx)
        idx = lastidx
        tow.see(idx)
    tow.tag_config('found', foreground='red')


def print_output_text(filepath, filename):

    
    new_file = (filepath + filename + '.txt')
     
    date = time.strftime('%B %d, %Y')
    clock_time = time.strftime('%I:%M %p')
     
    phrase1 = ("                   'Web Page Inspector' \n" + 
        "                    Author: promontorycoder \n" + 
        "                    Author Email: promontorycoder@tutanota.com \n" +
        "                    GitHub: https://github.com/promontorycoder \n" +
        "\nWeb Page Inspection Results Produced On ")
    phrase2 = " at "
    
    doc_write = (phrase1 + date + phrase2 + clock_time + '\n' + 
        tow.get(1.0, END))
    
    with open(new_file, 'w') as file_object:
        file_object.write(doc_write)


def clear_image_folder(filepath):
    
    tow.insert(END, "\nClearing files from folder in file path ...")
    try:
        
        if not filepath:
            tow.insert(END, "\nPlease enter a folder path and try again: ")
            
        else:
                    
            files = os.listdir(filepath)
            
            del_files = []
            
            for file in files:
                del_files.append(filepath + file)
            
            for file in del_files:
                os.remove(file)
                
            tow.insert(END, "\nCompleted clearing files from folder path ...")
            
    except Exception as err:
        tow.insert(END, err)
        tow.insert(END, "\nFailed to delete files in folder ...")
        

# Function to clear text from tkinter text widget window
def clear_output():
    tow.delete(1.0, END)


# Function to clear web address (url) tkinter entry text box
def clear_url():
    entry_url.delete(0, 'end')
    

# Function to clear search criteria tkinter entry text box
def clear_search_info():
    entry_search_info.delete(0, 'end')    


# Function to clear file path tkinter entry text box
def clear_filepath():
    entry_filepath.delete(0, 'end')


# Function to clear file name tktinter entry text box
def clear_filename():
    entry_filename.delete(0, 'end')


# Function exits program
def Exit():
    exit()


# Create tkinter text window widget
tow = Text(root, 
    height=35, 
    width=85, 
    borderwidth=1, 
    relief='ridge', 
    bg='gray7', 
    fg='lime green'
    )
    
# Place tkinter text box widget on the root window
tow.place(x=50, y=200)

# Create tkinter scrollbar for text output widget
scrollbar = Scrollbar(root)

# Place the scrollbar on the tkinter root window
scrollbar.place(x=760, y=475)

# Configure commands for scrollbar and tie to text output widget
tow.config(yscrollcommand=scrollbar.set)
scrollbar.config(
    command=tow.yview, 
    bg='gray7', 
    activebackground='lime green', 
    highlightcolor='lime green', 
    width=15
    )


# Create tkinter entry boxes for the root window
# Create tkinter entry box for gathering web address (url)
entry_url = Entry(root, 
    font = 'arial 10', 
    width=40, 
    bg='gray7', 
    fg='lime green'
    )

# Create tkinter entry box for gathering search criteria    
entry_search_info = Entry(root, 
    font = 'arial 10', 
    width = 40, 
    bg='gray7', 
    fg='lime green'
    )

# Create tkinter entry box for gathering file path    
entry_filepath = Entry(root, 
    font = 'arial 8', 
    width = 40, 
    bg='gray7', 
    fg='lime green'
    )

# Create tkinter entry box for gathering file name    
entry_filename = Entry(root, 
    font = 'arial 8', 
    width = 40, 
    bg='gray7', 
    fg='lime green'
    )
    
# Place tkinter entry boxes on the root window
entry_url.place(x=50, y=50)
entry_search_info.place(x=50, y=100)
entry_filepath.place(x=425, y=50)
entry_filename.place(x=425, y=100)


# Create message Labels for the root window
# Create msg label for web address (url) tkinter entry box
label_url = Label(root, 
    text = "Enter a web address: ", 
    font = 'arial 12', 
    bg='gray7', 
    fg='lime green'
    )

# Create msg label for search criteria tkinter entry box    
label_search_info = Label(root,
    text = "Enter for Output Search: ", 
    font = 'arial 12', 
    bg='gray7', 
    fg='lime green'
    )

# Create msg label for file path tkinter entry box    
label_filepath = Label(root, 
    text = "Enter a file path:",
    font = 'arial 10', 
    bg='gray7', 
    fg='lime green'
    )

# Create msg label for file name tkinter entry box    
label_filename = Label(root, 
    text = "Enter a file name with extension:", 
    font = 'arial 10',  
    bg='gray7', 
    fg='lime green'
    )

# Place Labels on the root window
label_url.place(x=50, y=25)
label_search_info.place(x=50, y=75)
label_filepath.place(x=425, y=25)
label_filename.place(x=425, y=75)

# Create Buttons
# Button: EXIT, function: Exit
btn_exit = Button(root, 
    command = Exit,
    width=6, 
    padx=2, 
    pady=1, 
    text = 'EXIT', 
    font = 'arial 10 bold', 
    bg = 'OrangeRed'
    )

# Button: SEARCH, tkinter search entry box, function: search_website   
btn_info = Button(root, 
    command = lambda: info(entry_url.get()), 
    text = 'INFO', 
    font = 'arial 10', 
    bg='lime green', 
    fg='gray7'
    )

# Button: Clear Output, tkinter text widget, function: clear_output    
btn_clear_output = Button(root, 
    command = clear_output, 
    text = 'Clear Output', 
    font = 'arial 10', 
    bg='gray7', 
    fg='lime green'
    )

# Button: CLEAR, tkinter web address entry box, function: clear_url
btn_clear_url = Button(root, 
    command = clear_url, 
    text = 'CLEAR', 
    font = 'arial 7', 
    bg='gray7', 
    fg='lime green'
    )

# Button: CLEAR, tkinter search entry box, function: clear_search_info    
btn_clear_search_info = Button(root,
    command = clear_search_info, 
    text = 'CLEAR', 
    font = 'arial 7', 
    bg='gray7', 
    fg='lime green'
    )

# Button: Print Title, function: print_title    
btn_print_title = Button(root, 
    command = lambda: print_title(entry_url.get()), 
    text = 'Print Title', 
    font = 'arial 10', 
    bg='gray7', 
    fg='lime green'
    )

# Button: Print Body, function: print_body    
btn_print_body = Button(root,
    command = lambda: print_body(entry_url.get()), 
    text = 'Print Body', 
    font = 'arial 10', 
    bg='gray7', 
    fg='lime green'
    )

# Button: CLEAR, function: clear_filepath    
btn_clear_filepath = Button(root, 
    command = clear_filepath, 
    text = 'CLEAR', 
    font = 'arial 7', 
    bg='gray7', 
    fg='lime green'
    )

# Button: CLEAR, function: clear_filename    
btn_clear_filename = Button(root, 
    command = clear_filename, 
    text = 'CLEAR', 
    font = 'arial 7', 
    bg='gray7', 
    fg='lime green'
    )

# Button: TAGS, function: show_html_tags    
btn_show_html_tags = Button(root, 
    command = lambda: show_html_tags(entry_url.get()), 
    text = 'TAGS', 
    font = 'arial 9', 
    bg='orange', 
    fg='gray7'
    )

# Button: RESP, funcion: web_response    
btn_web_response = Button(root, 
    command = lambda: web_response(entry_url.get()), 
    text = 'RESP', 
    font = 'arial 9', 
    bg='yellow', 
    fg='gray7'
    )

# Button: HEADERS, function: show_headers    
btn_show_headers = Button(root, 
    command = lambda: show_headers(entry_url.get()), 
    text = 'HEADERS', 
    font = 'arial 9', 
    bg='orange', 
    fg='gray7'
    )

# Button: URLS, function: show_urls    
btn_show_urls = Button(root, 
    command = lambda: show_urls(entry_url.get()),
    text = 'URLS',
    font = 'arial 9', 
    bg='orange', 
    fg='gray7'
    )

# Button: IMG TAGS, function: get_img_tags    
btn_get_img_tags = Button(root,
    command = lambda: get_img_tags(entry_url.get()), 
    text = 'IMG TAGS',
    font = 'arial 9', 
    bg='yellow', 
    fg='gray7'
    )

# Button: IMG-DWNLD, function: images_main    
btn_dwnload_images = Button(root, 
    command = lambda: images_main(entry_filepath.get(), entry_url.get()), 
    text = 'IMG-DWNLD',
    font = 'arial 9', 
    bg='yellow',
    fg='gray7'
    )

# Button: IMG-SHOW, function: show_images    
btn_show_images = Button(root, 
    command = lambda: show_images(entry_filepath.get()), 
    text = 'IMG-SHOW', 
    font = 'arial 9', 
    bg='purple',
    fg='lime green'
    )
    
btn_print_output_text = Button(root, 
    command = lambda: print_output_text(entry_filepath.get(), entry_filename.get()), 
    text = 'Print Output',
    font = 'arial 10',
    bg='royal blue',
    fg='lime green'
    )
    
btn_search_output_text = Button(root, 
    command = lambda: search_output_text(entry_search_info.get()),
    text = 'Search Output',
    font = 'arial 7',
    bg='lime green',
    fg='gray7'
    )
    
btn_clear_image_folder = Button(root, 
    command = lambda: clear_image_folder(entry_filepath.get()),
    text = 'Clear Img Folder',
    font = 'arial 7', 
    bg='red',
    fg='gray7'
    )
    

# Place each button in the root window
btn_exit.place(x=680, y=810)
btn_info.place(x=50, y=165)
btn_clear_output.place(x=160, y=810)
btn_clear_url.place(x=345, y=48)
btn_clear_search_info.place(x=345, y=98)
btn_print_title.place(x=190, y=165)
btn_print_body.place(x=280, y=165)
btn_clear_filepath.place(x=680, y=48)
btn_clear_filename.place(x=680, y=98)
btn_show_html_tags.place(x=425, y=167)
btn_web_response.place(x=120, y=167)
btn_show_headers.place(x=490, y=167)
btn_show_urls.place(x=585, y=167)
btn_get_img_tags.place(x=425, y=130)
btn_dwnload_images.place(x=515, y=130)
btn_show_images.place(x=620, y=130)
btn_print_output_text.place(x=50, y=810)
btn_search_output_text.place(x=50, y=130)
btn_clear_image_folder.place(x=400, y=810)


# Call main loop for looping through program    
root.mainloop()
