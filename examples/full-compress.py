## fully compress a static site

import xml.dom.minidom
import os, re
from htmlmin import minify
from csscompressor import compress
from jsmin import jsmin

dom = xml.dom.minidom.parse("public.xml")

root = dom.documentElement
exts = dom.getElementsByTagName("extention")

imgs = [".png",".jpg",".jpeg",".gif",".svg"]
to_webp = [".png"]

def replace_extension(match):
    attr_value = match.group(1)
    return attr_value.replace('.png', '.webp')

for ext in exts:
    extension_text = ext.firstChild.data.strip()

    if extension_text == ".html" or extension_text == ".xml" :
        path = ext.parentNode.getElementsByTagName("path")[0].firstChild.nodeValue     
        with open(path,'r') as file:
            html_content = file.read()
        modified_html = re.sub(r'(src="[^"]*\.(?:png|svg)")', replace_extension, html_content)
        minified_content = minify(modified_html, remove_comments=True, remove_empty_space=True)
        with open(path, 'w') as file:
            file.write(minified_content)

    elif extension_text == ".css":
        path = ext.parentNode.getElementsByTagName("path")[0].firstChild.nodeValue
        
        with open(path, 'r') as file:
            css_content = file.read()
        modified_css = re.sub(r'(url\("[^"]*\.(?:png|svg)"\))', replace_extension, css_content)
        mini_css = compress(css_content)
        with open(path, 'w') as file:
            file.write(mini_css) 

    elif extension_text == ".js":
        path = ext.parentNode.getElementsByTagName("path")[0].firstChild.nodeValue
        with open(path, 'r') as file:
            js_content = file.read()

        compressed_content = jsmin(js_content)

        with open(path, 'w') as file:
            file.write(compressed_content)

    elif extension_text in imgs:
          path = ext.parentNode.getElementsByTagName("path")[0].firstChild.nodeValue
          if extension_text in to_webp:
              pattern = r"\.(png)\b"
              topath = re.sub(pattern, ".webp",path)
              delpath = path
              path = f'"{path}"'
              topath = f'"{topath}"'
              os.system(f"convert {path} -quality 80 {topath}")
              if os.path.exists(delpath):
                  os.remove(delpath)
          else:       
              os.system(f"convert {path} -quality 80 {path}")



