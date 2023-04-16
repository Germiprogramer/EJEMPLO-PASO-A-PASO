from bs4 import BeautifulSoup
import asyncio
from urllib.parse import urlparse
import aiohttp
from os import sep
import sys

def get_images_src_from_html(html_doc):    
    """Recupera todo el contenido de los atributos src de las etiquetas img"""   
    soup = BeautifulSoup(html_doc, "html.parser")    
    return (img.get('src') for img in soup.find_all('img'))

imagen1 = get_images_src_from_html("<html><body><img src='http://www.formation-python.com/formation-python.png' /></body></html>")

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
                    path = '/' + '/'.join(parsed_base.path.split('/')   [:-1]) + '/' + path    
            yield parsed_base.scheme + '://' + parsed_base.netloc + path  
        else:    
            yield parsed.geturl() 

#imagen2 = get_uri_from_images_src("http://www.formation-python.com/", imagen1)

#DESCARGAR EN MODO ASÍNCRONO
#esta funcion te retorna el html de la pagina web
async def main(uri):  
     async with aiohttp.ClientSession() as session:  
        async with session.get(uri) as response:  
             if response.status != 200:                   
                 return None  
             if response.content_type.startswith("text/"):  
                 return await response.text()  
             else:  
                return await response.read()   

#print(asyncio.run(main("http://www.formation-python.com/")))

async def wget(session, uri):  
    async with session.get(uri) as response:  
        if response.status != 200:  
            return None  
        if response.content_type.startswith("text/"):  
            return await response.text()  
        else:  
            return await response.read()
        
async def download(session, uri):  
    content = await wget(session, uri)  
    if content is None:  
        return None  
    with open(uri.split(sep)[-1], "wb") as f:  
        f.write(content)  
        return uri 

#PARSEAR EN MODO ASÍNCRONO 

async def get_images_src_from_html(html_doc):
    """Recupera todo el contenido de los atributos src de las etiquetas img"""
    soup = BeautifulSoup(html_doc, "html.parser")
    for img in soup.find_all('img'):
        #yield es como un retrun pero no finaliza la funcion
        yield img.get('src')
        #await se usa para esperar a que se ejecute la funcion
        await asyncio.sleep(0.001)

async def get_uri_from_images_src(base_uri, images_src):  
    """Devuelve una a una cada URI de imagen a descargar"""  
    parsed_base = urlparse(base_uri)  
    async for src in images_src:  
        parsed = urlparse(src)  
        if parsed.netloc == '':  
            path = parsed.path  
            if parsed.query:  
                path += '?' + parsed.query  
            if path[0] != '/':  
                if parsed_base.path == '/':  
                    path = '/' + path  
                else:  
                    path = '/' + '/'.join(parsed_base.path.split('/')[:-1]) + '/' + path  
            yield parsed_base.scheme + '://' + parsed_base.netloc + path  
        else:  
            yield parsed.geturl()  
        await asyncio.sleep(0.001) 

async def get_images(session, page_uri):
    html = await wget(session, page_uri)
    if not html:
        print("Error al descargar", sys.stderr)
        return None
    images_src_gen = get_images_src_from_html(html)
    images_uri_gen = get_uri_from_images_src(page_uri, images_src_gen)
    async for image_uri in images_uri_gen:
        print("Descarga de %s" % image_uri)
        #para hacer llamadas asincronas dentro de una funcion asincrona
        await download(session, image_uri)

async def main():  
    web_page_uri = 'http://www.formation-python.com/'  
    async with aiohttp.ClientSession() as session:  
        await get_images(session, web_page_uri) 

#descargar una imagen dada una uri

async def main():
    uri = ""
    async with aiohttp.ClientSession() as session:
        await download(session, uri)

asyncio.run(main())
