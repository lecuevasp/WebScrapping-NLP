def fn_buscar_libro():
    # Importar módulos
    import requests
    from punctuation import Punctuation
    import lxml.html as html
    import pandas as pd
    # url a buscalibre
    url = "https://www.buscalibre.cl/libros/search?q="
    # Ingrese término a buscar
    buscar = input('Este es un buscador ejecutable de Busca Libre.\nEscriba lo que quiere buscar: ')
    # Remover puntuaciones
    buscar = Punctuation.remove(buscar)
    # Unir termino de busqueda
    buscar = "+".join(buscar.split())
    # url
    url = url+buscar
    # Crear lista de datos vacia
    autores_list = []
    titulos_list = []
    editoriales_list = []
    descuentos_list = []
    precios_anteriores_clp_list = []
    precios_actuales_clp_list = []
    paginas_webs_list = []

    #Revisar correcta conexión a sitio web (Response [200] : Está OK)
    obtener_pagina = requests.get(url)
    obtener_pagina_utf8 = obtener_pagina.content.decode('utf-8')
    parsear_pagina = html.fromstring(obtener_pagina_utf8)

    for i in [1]+parsear_pagina.xpath('//span[@class="pagnLink"]/a/text()'):
        #Revisar correcta conexión a sitio web (Response [200] : Está OK)
        obtener_pagina = requests.get(url+'&page='+str(i))
        obtener_pagina_utf8 = obtener_pagina.content.decode('utf-8')
        parsear_pagina = html.fromstring(obtener_pagina_utf8)

        # Pasear autores
        autores = parsear_pagina.xpath('//div[@class="autor"]')
        # Obtener texto de parseo autores
        autores = [autore.text for autore in autores]
        #autores_list.append(autores)

        # Pasear títulos
        titulos = parsear_pagina.xpath('//h3[@class="nombre margin-top-10 text-align-left"]')
        # Obtener texto de parseo títulos
        titulos = [titulo.text for titulo in titulos]
        # Quitar espacios en blanco
        titulos = [titulo.strip() for titulo in titulos]
        #titulos_list.append(titulos)

        # Pasear editoriales
        editoriales = parsear_pagina.xpath('//div[@class="autor color-dark-gray metas hide-on-hover"]')
        # Obtener texto de parseo editoriales
        editoriales = [editorial.text for editorial in editoriales]
        # Quitar espacios en blanco
        editoriales = [editorial.strip() for editorial in editoriales]
        #editoriales_list.append(editoriales)

        # Pasear descuentos
        descuentos = parsear_pagina.xpath('//div[@class="descuento-v2 color-white position-relative"]')
        # Obtener texto de parseo descuentos
        descuentos = [descuento.text for descuento in descuentos]
        #descuentos_list.append(descuentos)

        # Pasear precios_anteriores
        precios_anteriores = parsear_pagina.xpath('//p/del')
        # Obtener texto de parseo precios_anteriores
        precios_anteriores = [precio_anterior.text for precio_anterior in precios_anteriores]
        # Tranformar a entero
        precios_anteriores_clp = [int(precio.replace('$ ','').replace('.','')) if precio is not None else precio for precio in precios_anteriores ]
        #precios_anteriores_clp_list.append(precios_anteriores_clp)

        # Pasear precios_actuales
        precios_actuales = parsear_pagina.xpath('//p/strong')
        # Obtener texto de parseo precios_actuales
        precios_actuales = [precio_actual.text for precio_actual in precios_actuales]
        # Tranformar a entero
        precios_actuales_clp = [int(precio.replace('$ ','').replace('.','')) if precio is not None else precio for precio in precios_actuales ]
        #precios_actuales_clp_list.append(precios_actuales_clp)

        # Pasear paginas_webs
        paginas_webs = parsear_pagina.xpath('//*[@id="content"]/div/div/a/@href')
        #paginas_webs_list.append(paginas_webs)

        autores_list.append(autores)
        titulos_list.append(titulos)
        editoriales_list.append(editoriales)
        descuentos_list.append(descuentos)
        precios_anteriores_clp_list.append(precios_anteriores_clp)
        precios_actuales_clp_list.append(precios_actuales_clp)
        paginas_webs_list.append(paginas_webs)
    
    df = pd.DataFrame({'autores' : [c for i in range(len(autores_list)) for c in autores_list[i]],
                       'titulos' : [c for i in range(len(titulos_list)) for c in titulos_list[i]],
                       'editoriales' : [c for i in range(len(editoriales_list)) for c in editoriales_list[i]],
                       'descuentos':[c for i in range(len(descuentos_list)) for c in descuentos_list[i]],
                       'precios_anteriores_clp':[c for i in range(len(precios_anteriores_clp_list)) for c in precios_anteriores_clp_list[i]],
                       'precios_actuales_clp':[c for i in range(len(precios_actuales_clp_list)) for c in precios_actuales_clp_list[i]],
                       'paginas_webs':[c for i in range(len(paginas_webs_list)) for c in paginas_webs_list[i]]}).sort_values('precios_actuales_clp')
    
    df.to_excel('../datos_salida/'+buscar+'.xlsx', index=False)


def run():
    fn_buscar_libro()
        
if __name__  == '__main__':
    run()