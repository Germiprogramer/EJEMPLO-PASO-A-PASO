import requests

url_imagen = "https://golang.org/doc/gopher/appenginegophercolor.jpg" # El link de la imagen
nombre_local_imagen = "go.jpg"

#descargar un jpg
def descargar_imagen(url_imagen, nombre_local_imagen):
    imagen = requests.get(url_imagen).content
    with open(nombre_local_imagen, 'wb') as handler:
        handler.write(imagen)

descargar_imagen(url_imagen, nombre_local_imagen)