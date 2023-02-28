import asyncio
import aiohttp
from urllib.parse import urlparse
import sys
from os import sep
from sys import stderr

from bs4 import BeautifulSoup

from timeit import timeit


#funcion para coger imagenes html

def get_images_src_from_html(html_doc):    
    """Recupera todo el contenido de los atributos src de las etiquetas img"""   
    soup = BeautifulSoup(html_doc, "html.parser")    
    return (img.get('src') for img in soup.find_all('img'))

#recuperar las URI de las imagenes

def get_uri_from_images_src(base_uri, images_src):    
    """Devuelve una a una cada URI de la imagen a descargar"""    
    parsed_base = urlparse(base_uri)    
    for src in images_src:    
        parsed = urlparse(src)    
        if parsed.netloc == '':    
            path = parsed.path    
            if parsed.query:    
                path += '?' + parsed.query    
            if path[0] != '/':    
                if parsed_base.path == '/':    
                    path = '/' + path    
                else:    
                    path = '/' + '/'.join(parsed_base.path.split('/')   
[:-1]) + '/' + path    
            yield parsed_base.scheme + '://' + parsed_base.netloc + path  
        else:    
            yield parsed.geturl() 


async def main(uri):  
     async with aiohttp.ClientSession() as session:  
        async with session.get(uri) as response:  
             if response.status != 200:                   return None  
             if response.content_type.startswith("text/"):  
                 return await response.text()  
             else:  
                return await response.read()    
             
asyncio.run(main("http://www.formation-python.com/")) 