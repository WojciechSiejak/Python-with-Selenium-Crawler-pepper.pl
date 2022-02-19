from selenium import webdriver
import time
from pprint import pprint
from selenium.webdriver.common.by import By
import xml.etree.cElementTree as ET


xml_doc = ET.Element('root')

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

liczbaStron = input('How many pages you want to crawl?')

id=0

with open("test2.txt", "w" , encoding = "utf-8") as file:  
    
    for i in range(2,liczbaStron):
        time.sleep(0.5)
        driver.get("https://www.pepper.pl/nowe?page="+str(i))
        time.sleep(0.5)
        
        # Titles and links
        products_HTML = driver.find_elements(By.CLASS_NAME, "thread-title--list")
        titles = [ title.get_attribute('title') for title in products_HTML]
        links = [ link.get_attribute('href') for link in products_HTML]
                
        # Prices
        prices_HTML = driver.find_elements_by_class_name('overflow--fade')
        prices = [ price.find_element_by_class_name("thread-price").get_attribute('innerHTML') if price.find_elements_by_class_name('thread-price') else 'BRAK CENY' for price in prices_HTML]  
        # Store
        merchants = [ merchant.find_element_by_class_name("cept-merchant-name").get_attribute('innerHTML') if merchant.find_elements_by_class_name('cept-merchant-name') else 'BRAK NAZWY' for merchant in prices_HTML]  
        # Img
        products_images_HTML = driver.find_elements(By.CLASS_NAME, "cept-thread-img")
        images = [ link.get_attribute('src') for link in products_images_HTML]
        

        for i in range(len(links)):
            file.write("Id: " + str(id) + " Adres: "+ links[i] +" Tytuł: " + titles[i] + " CENA:" + prices[i] + " SKLEP: " + merchants[i] + " IMG: " + images[i] + "\n")
            id = id+1       
            
            product = ET.SubElement(xml_doc, 'product')
            ET.SubElement(product, 'item', id =str(id), price=prices[i]).text = titles[i]
            ET.SubElement(product, 'link').text= links[i]
            ET.SubElement(product,'store').text = merchants[i]
            
            images_xml = ET.SubElement(product, 'images')
            ET.SubElement(images_xml, 'small-image').text = images[i]
            medium_img = images[i].replace('/300x300/', '/768x768/')
            ET.SubElement(images_xml, 'medium-image').text = medium_img
            large_img = images[i].replace('/300x300/', '/1024x1024/')
            ET.SubElement(images_xml, 'large-image').text = large_img

            
    def indent(elem, level=0):
        i = "\n" + level*"  "
        j = "\n" + (level-1)*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for subelem in elem:
                indent(subelem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = j
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = j
        return elem    
            
    file.close()
    indent(xml_doc)
    tree = ET.ElementTree(xml_doc)
    tree.write('sample.xml', encoding='UTF-8', xml_declaration=True)

    
driver.quit()  
