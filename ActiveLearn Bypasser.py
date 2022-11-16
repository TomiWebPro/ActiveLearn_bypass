from PIL import Image
from fpdf import FPDF
import os
import re
import wget

try:
    print("Hello, this code is used to bypass active learn and download full pdf from it")
    print("Made by TomiWebPro, only for educational purposes\n")
    input_of_website = str(input("enter the website link with jpg at the back: "))
    input_of_minpages = int(input("lowest page number you want to download: "))
    input_of_maxpages = int(input("highest page number you want to download: "))
    input_of_pdfname = str(input("enter the name of the final pdf output: "))
    page_interval = input_of_maxpages - input_of_minpages

    print("The website name is", input_of_website, "from page",
        input_of_minpages, "to page", input_of_maxpages, "good to proceed? (y/n)")
    proceed_check = input()
    print("")

    def check(a):
        if a == "y":
            print("Processing...")
        else:
            x
    
    check(proceed_check)
    all_jpgs_filename = []

    for i in range(page_interval+1):
        formatted_number = format(input_of_minpages+i, '0>3'.format(7))
        replaced_website = re.sub(r'(?<=-).+?(?=.jpg)',
                                formatted_number, input_of_website, flags=re.S)
        filename = wget.download(replaced_website)
        all_jpgs_filename.append(filename)
        print("Downloaded page", input_of_minpages+i)
        #print(all_jpgs_filename)

    print("Assembling all the Pages")
    # get image
    filepath = all_jpgs_filename[0]
    img = Image.open(filepath)

    # get width and height
    width = img.width
    height = img.height

    pdf = FPDF('L', 'pt', (height, width))
    pdf.set_auto_page_break(0)

    pdf.l_margin = 0
    pdf.r_margin = 0
    pdf.t_margin = 0
    pdf.b_margin = 0

    for img in all_jpgs_filename:
        pdf.add_page()
        image=img
        pdf.image(image,w=width,h=height)

    final_input = input_of_pdfname + ".pdf"
    pdf.output(final_input)
    
    print("\nBypass download success!")
    print("Filename",final_input,"is stored in the current directory")

except:
    print("Something went wrong in the process, Please Re-run the program")

#test it out
#IG Computer Science Textbook
#https://resources.pearsonactivelearn.com/r01/r0104/r010452/r01045272/current/OPS/images/1045272-023.jpg

#IG Russia History Textbook
#https://resources.pearsonactivelearn.com/r00/r0074/r007427/r00742798/current/OPS/images/9780435185435-031.jpg
