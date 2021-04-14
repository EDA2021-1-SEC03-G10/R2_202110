"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def initCatalog():
    """
    Inicializa el catalogo de videos
    """
    return controller.initCatalog()

def printResults(ord_videos): 
    size = lt.size(ord_videos) 
    #if size > sample: 
        #print("Los primeros ", sample, " videos ordenados son:") 
    i=1 
    while i <= size: 
        video = lt.getElement(ord_videos,i) 
        print('Trending_date: ' + video['trending_date'] + ' Title: ' + video['title'] + ' Channel_title: ' + video['channel_title'] + ' publish_time: ' + video['publish_time'] +
                ' views: '+ video['views'] + ' likes: '+ video['likes'] + ' dislikes: '+ video['dislikes']) 
        i+=1

def loadData(catalog):
    """
    Carga los videos en la estructura de datos
    """
    return controller.loadData(catalog)

catalog = None


def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar los videos con más vistas y que son tendencia en un país")
    print("3- Consultar video que ha sido tendencia para un país")
    print("4- Consultar los videos que han estado mas en tendencia en una categoría")
    print("5- Consultar los videos con mas likes dado un país y un tag")
    print("6- Salir")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")

        catalog = initCatalog()
        answer = loadData(catalog)
        print('Videos cargados: ' + str(lt.size(catalog['videos'])))
        print('Categorias cargadas: ' + str(lt.size(catalog['categories'])))
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")


    elif int(inputs[0]) == 2: 
        size = int(input("Indique el número de videos que quiere listar: ")) 
        pais = input ("Ingrese el país para el cual desea realizar la consulta: ")
        categoria = input ("Ingrese la categoría que quiere consultar: ")
        if size > lt.size(catalog['videos']):
            print ("el tamaño de muestra solicitado excede la cantidad de datos de videos cargados")
        else:
            result = controller.sortVideos(catalog, size, pais, categoria.lower()) 

        printResults(result)

    elif int(inputs[0]) == 3:
        country = input ("Ingrese el país para el cual desea realizar la consulta: ")
        [result, count] = controller.getTrendingVideoByCountry(catalog, country)

        video = result
        print( 'Title: ' + video['title'] + ' Channel_title: ' + video['channel_title'] + ' Country: ' + video['country'] + ' Días: '+ str(count))

    elif int(inputs[0]) == 4:
        category= input("Ingrese la categoria que desea consultar: ")
        [result, count]=controller.getTrendingVideoByCategory(catalog,category)
        video = result
        print( 'Title: ' + video[0] + ' Channel_title: ' + video['channel_title'] + ' Category Id: ' + video['category_id'] + ' Días: '+ str(count))

    elif int(inputs[0])==5:
        tag=input("Ingrese el tag: ").lower()
        country=input("Ingrese la Ciudad: ").lower()
        n=input("Ingrese el Numero de videos que desea listar: ").lower()
        video=controller.getTrendingByLikes(catalog, tag, country, n)
        print( 'Title: ' + video['title'] + ' Channel_title: ' + video['channel_title'] + ' Publlish_Time: ' + video['publish_time'] + ' Views: '+ video["views"] + " Likes: " + video["likes"] + " dislikes: "+ video["dislikes"] + "Tags: " + video["tags"])

    else:
        sys.exit(0)
sys.exit(0)
