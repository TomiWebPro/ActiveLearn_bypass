from PIL import Image
from fpdf import FPDF
import os
import re
import requests
import threading

print("Hello, this code is used to bypass ActiveLearn and download a full PDF from it.")
print("Made by TomiWebPro, only for educational purposes\n")

input_of_website = str(
    input("Enter the website link with '.jpg' at the end: "))
input_of_minpages = int(
    input("Enter the lowest page number you want to download: "))
input_of_maxpages = int(
    input("Enter the highest page number you want to download: "))
input_of_pdfname = str(input("Enter the name of the final PDF output: "))

page_interval = input_of_maxpages - input_of_minpages

print("The website name is", input_of_website, "from page",
      input_of_minpages, "to page", input_of_maxpages, "Are you ready to proceed? (y/n)")
proceed_check = input()

print("")


def check(a):
    if a == "y":
        print("Processing...")
    else:
        exit()


check(proceed_check)
all_jpgs_filename = []
lock = threading.Lock()
downloaded_pages = 0
total_pages = page_interval + 1


def download_image(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    global downloaded_pages
    with lock:
        downloaded_pages += 1
        print(f"Downloaded page {downloaded_pages}/{total_pages}")
    all_jpgs_filename.append(filename)


threads = []

for i in range(page_interval+1):
    formatted_number = format(input_of_minpages+i, '0>3')
    replaced_website = re.sub(
        r'(?<=-)\d+(?=.jpg)', formatted_number, input_of_website, flags=re.S)
    filename = f"page_{input_of_minpages+i}.jpg"
    thread = threading.Thread(target=download_image,
                              args=(replaced_website, filename))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print("All pages downloaded successfully!")
print("Assembling all the pages...")

# Sort the filenames in ascending order
all_jpgs_filename.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))

# get image dimensions
first_img = Image.open(all_jpgs_filename[0])
width, height = first_img.size

pdf = FPDF('L', 'pt', (height, width))
pdf.set_auto_page_break(0)

pdf.l_margin = 0
pdf.r_margin = 0
pdf.t_margin = 0
pdf.b_margin = 0

for img_filename in all_jpgs_filename:
    pdf.add_page()
    pdf.image(img_filename, w=width, h=height)

final_input = input_of_pdfname + ".pdf"
pdf.output(final_input)

print("\nBypass download success!")
print("Filename", final_input, "is stored in the current directory")

def delete_image(filename):
    # Wait until the file is no longer in use
    while True:
        try:
            with Image.open(filename) as img:
                img.close()  # Close the image explicitly
            os.remove(filename)
            break
        except Exception as e:
            print(f"Failed to remove {filename}: {e}")
            print("Retrying in 1 second...")
            time.sleep(1)

try:
    for img_filename in all_jpgs_filename:
        delete_image(img_filename)
    print("All temporary images removed. \n")
except:
    print("Failed to remove temporary images, please do so manually. \n")

input("Press enter to exit.")
