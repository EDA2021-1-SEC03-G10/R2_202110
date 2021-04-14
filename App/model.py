"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mg
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos



def newCatalog():
    """
    Inicializa el catálogo de videos. Crea una lista vacia para guardar
    todos los videos. Adicionalmente crea una lista vacia para guardar el título, el canal, 
    fecha de tendencia, pais, vistas, me gusta, no me gusta. Retorna el catalogo inicializado.
    title, cannel_title, trending_date, country, views, likes, dislikes
    """
    catalog = {'videos': None,
               'channels': None,
               'categories':None,
               'categoriesId':None,
               'countries':None,
               'tags': None}

    catalog['videos'] = lt.newList('SINGLE_LINKED', compareVideoId)

    catalog['videoIds'] = mp.newMap(375923,
                                   maptype='CHAINING',
                                   loadfactor=6.0,
                                   comparefunction=compareMapVideoIds)
    
    catalog['channels'] =  mp.newMap(37633,
                                maptype='CHANING',
                                loadfactor=4.00,
                                comparefunction=comparechannels)
        
    catalog['countries'] = mp.newMap(13,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=comparecountries)

    catalog['tags'] = mp.newMap(141761,
                                maptype='CHANING',
                                loadfactor=6.00,
                                comparefunction=comparetags)

    catalog['categories'] = mp.newMap(37,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=comparecategories)

    catalog['categoriesId'] = mp.newMap(37,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=compareCategoryIds)

    return catalog

# Funciones para agregar informacion al catalogo

def addVideo(catalog, video):
    if video['category_id'] == "":
        return

    lt.addLast(catalog['videos'], video)
    mp.put(catalog['videoIds'], video['video_id'], video)
    tags = video['tags'].split("|")
    for tag in tags:
        addVideoTag(catalog, tag.strip(), video)
    addVideoChannel(catalog,video)  
    addVideoCountry(catalog,video)

    categoryIds = catalog['categoriesId']
    if (video['category_id'] == ''):
        return
    categoryId = int(video['category_id'])
    entry = mp.get(categoryIds, str(categoryId))
    categoryname = me.getValue(entry)["name"]
    existcategory = mp.contains(categoryIds, categoryId)
    if existcategory:
        entry = mp.get(categoryIds, categoryId)
        category = me.getValue(entry)
    else:
        category = newCategory(categoryId,categoryname)
        mp.put(categoryIds, categoryId, category)
    lt.addLast(category['videos'], video)

    categories = catalog["categories"]
   

    existcategoryname = mp.contains(categories, categoryname)
    if existcategoryname:
        entry = mp.get(categories, categoryname)
        category = me.getValue(entry)
    else:
        category = newCategory(categoryId,categoryname)
        mp.put(categories, categoryname, category)
    lt.addLast(category['videos'], video)

def addVideoChannel(catalog, video):
    """
    Esta funcion adiciona un video a la lista de videos que
    fueron publicados en un canal especifico.
    
    """
    try:
        channels = catalog['channels']
        if (video['channel_title'] == ''):
            return

        videochannel = video['channel_title']    
        existchannel = mp.contains(channels, videochannel)
        if existchannel:
            entry = mp.get(channels, videochannel)
            channel = me.getValue(entry)
        else:
            channel = newChannel(videochannel)
            mp.put(channels, videochannel, channel)
        lt.addLast(channel['videos'], video)
    except Exception:
        return None

def newChannel(videochannel):
    """
    Esta funcion crea la estructura de videos asociados
    a un canal.
    """
    entry = {'channel': "", "videos": None}
    entry['channel'] = videochannel
    entry['videos'] = lt.newList('SINGLE_LINKED', compareChannels)
    return entry   
    
  
    # #mp.put(catalog['categoriesId'], video['category_id'], video)
    


    
def addVideoCountry(catalog, video):
    """
    Esta funcion adiciona un video a la lista de videos que
    fueron publicados en un país especifico.
    
    """
    try:
        countries = catalog['countries']
        if (video['country'] == ''):
            return

        videocountry = video['country']    
        existcountry = mp.contains(countries, videocountry)
        if existcountry:
            entry = mp.get(countries, videocountry)
            country = me.getValue(entry)
        else:
            country = newCountry(videocountry)
            mp.put(countries, videocountry, country)
        lt.addLast(country['videos'], video)
    except Exception:
        return None

def newCountry(videocountry):
    """
    Esta funcion crea la estructura de videos asociados
    a un país.
    """
    entry = {'country': "", "videos": None}
    entry['country'] = videocountry
    entry['videos'] = lt.newList('SINGLE_LINKED', compareCountries)
    return entry 

def addVideoTag(catalog, tagname, video):
    """
    Esta función adiciona un libro a la lista de libros publicados
    por un autor.
    Cuando se adiciona el libro se actualiza el promedio de dicho autor
    """
    tags = catalog['tags']
    existtag = mp.contains(tags, tagname)
    if existtag:
        entry = mp.get(tags, tagname)
        tag = me.getValue(entry)
    else:
        tag = newTag(tagname)
        mp.put(tags, tagname, tag)
    lt.addLast(tag['videos'], video)

def newTag(name):
    """
    Crea una nueva estructura para modelar los videos de un tag.
    Se crea una lista para guardar los
    videos de dicho tag.
    """
    tag = {'name': "",
              "videos": None}
    tag['name'] = name
    tag['videos'] = lt.newList('SINGLE_LINKED', compareTagsByName)
    return tag
    
def newCategoryId(categoryId):

    entry = {'categoryId': "", "videos": None}
    entry['categoryId'] = categoryId
    entry['videos'] = lt.newList('SINGLE_LINKED', compareVideoId)

    

    return entry

# Funciones para creacion de datos
def addCategory(catalog, category):
    """
    Adiciona una categoria a la lista de categorías
    """
    c = newCategory(category['id'], category['name'].strip().lower())
    mp.put(catalog['categories'], category['name'].strip().lower(), c)
    mp.put(catalog['categoriesId'], category['id'].strip().lower(), c)


# Funciones de consulta

def getVideosLikesByCategory(catalog,category,n):

    index_category = 1

    while category.lower() not in lt.getElement(catalog["categories"], index_category)["name"].lower() :
        index_category += 1

    id_category = lt.getElement(catalog["categories"],index_category)["id"]

    category = mp.get(catalog['categoriesId'], int(id_category))

    if category:
        result = me.getValue(category)
        result = mg.sort(result, compareVideosLikes)
        result = lt.subList(result, 1, n)
    else:
        result = None

    return result

def newCategory(id, name):
    """
    Esta estructura almancena las categorías utilizados para marcar videos.
    """
    category = {'name': '', 'id': '', 'videos': None}
    category['name'] = name.strip()
    category['id'] = id
    category ['videos'] = lt.newList('SINGLE_LINKED', compareVideoId)
    return category

# Funciones utilizadas para comparar elementos dentro de una lista

def compareTagsByName(keyname, tag):
    """
    Compara dos nombres de tag. El primero es una cadena
    y el segundo un entry de un map
    """
    keyname = keyname.lower()
    tagentry = me.getKey(tag)
    tagentry = tagentry.lower()
    if (keyname == tagentry):
        return 0
    elif (keyname > tagentry):
        return 1
    else:
        return -1

def compareVideoId(video1, video2):
    """
    Compara dos ids de dos videos
    """
    if (video1['video_id'] == video2['video_id']):
        return 0
    elif (video1['video_id'] > video2['video_id']):
        return 1
    else:
        return -1

def compareMapVideoIds(id, entry):
    """
    Compara dos ids de videos, id es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (id == identry):
        return 0
    elif (id > identry):
        return 1
    else:
        return -1

def compareVideosLikes(video1, video2): 
    if video1['likes'] == "":
        v1 = 0
    else:
        v1 = int(video1['likes'])
    
    if video2['likes'] == "":
        v2 = 0
    else:
        v2 = int(video2['likes'])

    if (v1 > v2):
        return 1
    elif (v1 == v2):
        return 0
    else:
        return -1


def comparechannels(channelname, channel2):
    """
    Compara los canales
    """
    channelname = channelname.lower()
    channelentry = me.getKey(channel2)
    channelentry = channelentry.lower()
    if (channelname == channelentry):
        return 0
    elif (channelname > channelentry):
        return 1
    else:
        return -1

def comparecountries(countryname, country2):
    """
    Compara los paises
    """
    countryname = countryname.lower()
    countryentry = me.getKey(country2)
    countryentry = countryentry.lower()
    if (countryname == countryentry):
        return 0
    elif (countryname > countryentry):
        return 1
    else:
        return -1

def comparetags(tagname, tag2):
    """
    Compara los tags
    """
    tagname = tagname.lower()
    tagentry = me.getKey(tag2)
    tagentry = tagentry.lower()
    if (tagname == tagentry):
        return 0
    elif (tagname > tagentry):
        return 1
    else:
        return -1

def comparecategories(categoryname, category):
    """
    Compara las categorías por el nombre
    """
    categoryname = categoryname.lower()
    catentry = me.getKey(category)
    catentry = catentry.lower()
    if (categoryname == catentry):
        return 0
    elif (categoryname > catentry):
        return 1
    else:
        return -1


def compareCategoryIds(id1, entry):
    """
    Compara los ids de dos categorías
    """

    identry = me.getKey(entry)
    if (int(id1) == int(identry)):
        return 0
    elif (int(id1) > int(identry)):
        return 1
    else:
        return -1

def compareChannels(channel1, channel2):
    """
    Compara los canales
    """
    Channel1 = channel1.lower()
    channelentry = me.getKey(channel2)
    channelentry = channelentry.lower()
    if (channel1 == channelentry):
        return 0
    elif (channel1 > channelentry):
        return 1
    else:
        return -1

def compareCountries(country1, country2):
    """
    Compara los canales
    """
    country1 = country1.lower()
    countryentry = me.getKey(country2)
    countryentry = countryentry.lower()
    if (country1 == countryentry):
        return 0
    elif (country1 > countryentry):
        return 1
    else:
        return -1

def compareVideoViews(video1, video2): 
    if video1['views'] == "":
        v1 = 0
    else:
        v1 = int(video1['views'])
    
    if video2['views'] == "":
        v2 = 0
    else:
        v2 = int(video2['views'])

    if (v1 > v2):
        return -1
    elif (v1 == v2):
        return 0
    else:
        return 1
    
def cmpVideosByCountry(video1, video2):
    """ 
     Devuelve verdadero (True) si los 'views' de video1 son mayores que los del video2 
     Args: 
     video1: informacion del primer video que incluye su valor 'views' 
     video2: informacion del segundo video que incluye su valor 'views' """

    if video1['country'].lower() > video2['country'].lower():
        return True
    return False

def cmpVideosByName(video1, video2):
    if video1['title'].lower() > video2['title'].lower():
        return True
    return False

# Funciones de ordenamiento

def sortVideos(catalog, n, country, category):

    ranked_list = None
    country_mp = mp.get(catalog["countries"], country)
    category_mp = mp.get(catalog["categories"],category)

    if country_mp:
        videos_country = me.getValue(country_mp)["videos"]
        videos_category = me.getValue(category_mp)["videos"]

        index = 1

        result = lt.newList('SINGLE_LINKED', compareVideoId)

        while index <= lt.size(videos_country):
            video = lt.getElement(videos_country,index)
            if ((lt.isPresent(videos_category,video))!=0):
                lt.addLast(result, video)
            index += 1
        
        result2 = mg.sort(result, compareVideoViews)

        ranked_list = lt.subList(result2, 1, n)
    
    return ranked_list

def getTrendingVideoByCountry(catalog, country):
    por_pais= mg.sort (catalog ["videos"], cmpVideosByCountry)

    index_inicio = 1

    while country not in lt.getElement(por_pais, index_inicio)["country"] :
        index_inicio += 1

    index_fin = index_inicio

    while country == lt.getElement(por_pais, index_fin)["country"] :
        index_fin += 1
        if index_fin > lt.size(por_pais):
            break
    
    sub_list = lt.subList(por_pais, index_inicio, index_fin-index_inicio)

    

    por_nombre = mg.sort (sub_list, cmpVideosByName)

    name = ""
    max_index = 0
    max_count = 0
    count = 0
    index = 0
    i = 1

    while i <= lt.size(por_nombre):
        if name.lower() == lt.getElement(por_nombre, i)["title"]:
            count += 1
        else:
            name = lt.getElement(por_nombre, i)["title"]
            index = i
            count = 1
        
        if count > max_count:
            max_index = index
            max_count = count
        i += 1

    return [lt.getElement(por_nombre, max_index), max_count]


def getTrendingVideoByCategory(catalog, category):

    category_mp=mp.get(catalog['categories'],category)
   
    
    if category_mp:
        a=me.getValue(category_mp)

    """por_nombre = mg.sort (a, cmpVideosByName)

    name = ""
    max_index = 0
    max_count = 0
    count = 0
    index = 0
    i = 1

    while i <= lt.size(por_nombre):
        if name.lower() == lt.getElement(por_nombre, i):
            count += 1
        else:
            name = lt.getElement(por_nombre, i)
            index = i
            count = 1
        
        if count > max_count:
            max_index = index
            max_count = count
        i += 1


    return [lt.getElement(por_nombre, max_index), max_count]"""
    return [a,8]
    


def getTrendingByLikes(catalog, tag, country, n):

    ranked_list = None

    country_mp = mp.get(catalog['countries'], country)
    countries = None
    if country_mp:
        countries = me.getValue(country_mp)
    else: 
        print("NO se encontro la ciudad.")
    

    tag_mp= mp.get(countries["tags"], tag)
    tags=None

    if tag_mp:
        tags= me.getValue(tag_mp)
    else:
        print("NO se encontro el tag")

    sorted_list = mg.sort(tags, compareVideosLikes)

    ranked_list = lt.subList(sorted_list, 1, n)

    return ranked_list

    