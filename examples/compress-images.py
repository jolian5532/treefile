import xml.dom.minidom
import os

dom = xml.dom.minidom.parse("public.xml")

root = dom.documentElement
exts = dom.getElementsByTagName("extention")

imgs = [".png",".jpg",".jpeg",".gif"]

for ext in exts:
    extension_text = ext.firstChild.data.strip()
    if extension_text in imgs:
        path = ext.parentNode.getElementsByTagName("path")[0].firstChild.nodeValue
        os.system(f"convert {path} -quality 70 {path}")
