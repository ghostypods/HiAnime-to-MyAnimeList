from tkinter import *
from tkinter import filedialog
import xml.etree.ElementTree as ET
from time import sleep

current_xml = None


def select_download_location(tree):
    # Open a "Save As" dialog and get the selected file path
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xml",
        filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
    )

    if file_path:
        label.config(text=f"File will be saved at: {file_path}")
        sleep(2)
        # Here you can save your file to the selected path
        with open(file_path, "wb") as mal_file:
            label.config(text="Please wait...")
            tree.write(mal_file)  # Write the tree to an XML file

        label.config(text="XML file created!")


def create_xml(imported_xml):
    label.config(text="Please wait...")

    # Create the root element
    myanimelist = ET.Element('myanimelist')

    # Create child elements
    myinfo = ET.SubElement(myanimelist, 'myinfo')
    user_export_type = ET.SubElement(myinfo, 'user_export_type')
    user_export_type.text = '1'

    for folder in imported_xml.findall('folder'):
        anime_status = folder.find('name').text
        for data in folder.findall('data'):
            for item in data.findall('item'):
                anime_title = item.find('name').text
                anime_link = item.find('link').text
                anime_id = anime_link.split('/')[-1]

                anime = ET.SubElement(myanimelist, 'anime')
                series_animedb_id = ET.SubElement(anime, 'series_animedb_id')
                series_animedb_id.text = f"{anime_id}"
                series_title = ET.SubElement(anime, 'series_title')
                series_title.text = f'<![CDATA[ {anime_title} ]]>'
                my_status = ET.SubElement(anime, 'my_status')
                my_status.text = f"{anime_status}"
                update_on_import = ET.SubElement(anime, 'update_on_import')
                update_on_import.text = "1"

    # Create a tree object from the root element
    tree = ET.ElementTree(myanimelist)
    select_download_location(tree)


def select_folder():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if file_path:  # If a folder is selected, display the path
        label.config(text=f"Selected Folder: {file_path}")

        global current_xml
        current_xml = ET.parse(file_path)

    else:
        label.config(text=f"File not found")


def use_xml_data():
    global current_xml
    if current_xml is not None:
        root = current_xml.getroot()

        for folder in root.findall('folder'):
            for name in folder.findall('name'):
                if name.text == 'Plan to watch':
                    name.text = "Plan to Watch"

                    global file_path
                    current_xml.write(file_path, encoding='utf-8', xml_declaration=True)

        create_xml(root)


window = Tk()
window.title("XML to MAL XML")
window.geometry("600x400")

title_label = Label(window, text="XML to MAL XML Converter!", font=('Helvetica', 30, 'normal'))
title_label.pack(pady=10)

credit_label = Label(window, text="by ghostypods on Githuhb", font=('Helvetica', 15, 'normal'))
credit_label.pack(pady=(0, 10))

note_text = Label(window,
                  text="Note: This app has only been tested with hianimez.to, so this may not work for other websites",
                  background='red', foreground='white')
note_text.pack()

description = Label(window,
                    text="Convert your exported hianime anime list XML file into a MyAnimeList compatible XML file!")
description.pack()

steps = Label(
    window,
    text="Steps:\n"
    "1. Download your hianime.to XML file with 'Group by folder' toggeled on\n"
    "2. Import the file below\n"
    "3. Save your new MAL XML wherever you want on your computer\n"
    "4. Import your MAL XML file into MyAnimeList",
    justify="left"
)
steps.pack(padx=(55,0), pady=(0, 10), anchor='w')

# Button to open the folder selection dialog
select_file_button = Button(window, text="Select File", command=select_folder)
select_file_button.pack(pady=10)

# Label to display the selected folder path
label = Label(window, text="No file selected")
label.pack(pady=10)

convert_button = Button(window, text="Convert to MAL XML", command=use_xml_data)
convert_button.pack(pady=20)

window.mainloop()
