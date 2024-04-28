
import selenium
import pandas as pd
import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#https://pypi.org/project/webdriver-manager/


from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager



class MEXICO:

    def __init__(self,nav = "MOZ"):
        
        self.url = 'https://es.wikipedia.org/wiki/Anexo:Entidades_federativas_de_M%C3%A9xico_por_superficie,_poblaci%C3%B3n_y_densidad'
        self.urlState = 'https://es.wikipedia.org/wiki/'

        if (nav.upper() == 'CHR'):
            options = webdriver.ChromeOptions()
            self.driver = webdriver.Chrome(options=options)
            self.driver.get(self.url)

        elif (nav.upper() == 'MOZ'):
            options = webdriver.FirefoxOptions()
            self.driver = webdriver.Firefox(options=options)
            self.driver.get(self.url)



    '''
    FUNCION DEDICADA PARA INGRESAR A WIKIPEDIA
    SE DEBE PASAR EL USUARIP  Y LA CONTRASEÑA COMO STRING
    SE PUEDE ELEGIR EL NAVEGADOR.
    '''

    def test_login_wikipedia(self, usuario, contraseña ):

        url= 'https://es.wikipedia.org/w/index.php?returnto=Wikipedia%3APortada&title=Especial:Entrar&centralAuthAutologinTried=1&centralAuthError=Not+centrally+logged+in'
    
        self.driver.get(url)

        #Parametros de entrada
        tag_user    = self.driver.find_element(By.ID, 'wpName1')
        tag_user.send_keys(usuario)

        tag_pasword = self.driver.find_element(By.ID, 'wpPassword1')
        tag_pasword.send_keys(contraseña)

        btn_login = self.driver.find_element(By.ID, 'wpLoginAttempt')
        btn_login.click()

        self.driver.get(self.url) #Esto permite ir directamente a la página de EUA
        self.driver.implicitly_wait(3)



  
    '''
    FUNCIONES EXTRAS
    ESTE METODO PERMITE PODER EXTRAER LOS DATOS DIRECTAMENTE DE LA TABLA 
    '''

    #FUNCION DE AJUSTE PARA REMOVER NUMERO DE UN UNA LISTA
    def eliminateNumbersNames(self, listNames):
        newList=[]
        for l in listNames:
            newList.append(''.join([i for i in l if not i.isdigit()]) )
        return newList 

    #FUNCION DE AJUSTE PARA REMOVER NUMERO DE UN STRING
    def eliminateNumbersName(self, Name):
        return ''.join([i for i in Name if not i.isdigit()])

    #FUNCION DE ELIMINACIÓN DE EMPTIES A NULL PARA CARGA DE SQL
    def eliminateEmpty(self, arrayData):
        old_item = ''
        new_item = 'NULL'
        return [new_item if item == old_item else item for item in arrayData]

    

        



    """
    FUNCION DE EXTRACCION DE LISTA DE ESTADOS
    """     

    def extractAllStates(self):

        statesList =[]
        self.driver.get(self.url)
        self.driver.implicitly_wait(5)

    
        all_States = self.driver.find_elements(By.XPATH,
                                                    ("//div/Table[@class='sortable jquery-tablesorter']/tbody/tr/td[4]"))
        
        for _s in all_States:
            if(_s.text !="Población" and _s.text !="Nombre" ):
                statesList.append((_s.text))
        
        return self.eliminateNumbersNames(statesList)


    """
    FUNCION DE EXTRACCION DE DATOS DE LA
    TOPONOMIA DE LOS ESTADOS 
    """      

    def dataState(self,state):
        arrData=[]
        stateUrl = self.urlState + state
        self.driver.get(stateUrl)
        try:
            Toponomia = self.driver.find_elements(By.XPATH, "//p[preceding-sibling::h2[1]/span[text()='Toponimia']] [./following-sibling::h2]")

      
            for p in Toponomia:
                arrData.append(p.text)
                #print(p.text)        
            #print(arrData)
            return {state:arrData}
        except:
            return{state:'No data'}


    def allDataStateToponomia(self, states, genFile=True, ordAsc =False):
        arrData=[]
        states.sort() if ordAsc else states
        print(states)
        for s in states:
            arrData.append(self.dataState(s))
        
        if genFile:
            with open(r'Topologia_MEX.txt', 'w',encoding='utf-8-sig') as fp:
                for item in arrData:
                    fp.write("%s\n" % item)

            print('DATOS EXTRAIDOS')
        return arrData

    '''

    ----------------------------------------------------------------

    FUNCION DE EXTRACCION DE TABLAS DE MÉXICO
    SE USA DATAFRAME DE PANDA PARA PODER DESCARGAR LA INFORMACIÓN.
    
    ----------------------------------------------------------------
    
    '''

    def extractTableData_Mex(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(5)


        '''
        SELECCIONA CON LA PARTE PRINCIPAL DE LA INFORMACIÓN
        TRAS UN ANALISIS DE LA TABLA LA ESTRUCTURA PRESENTA LOS PRIMEROS DOS RENGLONES DEL CUERPO 
        DE LATABLA CON TÍTULOS

        '''

        _XpathBody =  "//Table[@class='sortable jquery-tablesorter']/tbody"
        tbody = self.driver.find_element(By.XPATH, _XpathBody)
        filas = tbody.find_elements(By.TAG_NAME, "tr")

        dataBody = []
        control=1
        for fila in filas: 

            if control > 2:
                celdas = fila.find_elements(By.TAG_NAME,('td'))
                datos_filas = [celda.text for celda in celdas]
                control +=1
            else:
                control +=1
                continue

            if len(datos_filas) != 10 :
                datos_filas.insert(6,datos_filas[5])
                dataBody.append(datos_filas)
            else:     
                dataBody.append(datos_filas)

        for d in dataBody:
            d[3]= self.eliminateNumbersName(d[3])
        

        df = pd.DataFrame(dataBody, columns=[
                "SUPERFICIE",
                "POBLACION",
                "DENSIDAD (Hab/km2)",

                "NOMBRE", 
                "SUPERFICIE KM2",
                "SUPERFICIE %",
                
                "ESTIMACION 2020",
                "2015 (HAB/KM2)",

                "CAPITAL",
                "POBLACION 2020",
                "POSICION POBLACIÓN",
                "ORDEN"
                ]
                )
        try:
            df.to_csv('Mexico_a.csv',index=False,encoding='utf-8-sig')
        except:
            df.to_csv('Mexico_a_problem.csv',index=False,encoding='utf-8-sig') 
        

        print("ARCHIVO EXPORTADO")


    #//Table[preceding::h3/span[@id='Censos_(INEGI)_1900-2020']] [./following-sibling::h3]


    def extractTableData_Mex_Censo(self ):

            self.driver.get(self.url)
            self.driver.implicitly_wait(5)

            dataHead    =   []
            dataBody    =   []

            XpathTable = "//Table[preceding::h3/span[@id='Censos_(INEGI)_1900-2020']] [./following-sibling::h3]"
            _Table = self.driver.find_element(By.XPATH, XpathTable) 



            _XpathHead =  _Table.find_element(By.TAG_NAME,  "thead")
            _XpathBody =  _Table.find_element(By.TAG_NAME,  "tbody")

            # EXTRAE LOS TITULOS DE LA TABLA
            rowtitles = _XpathHead.find_element(By.XPATH,('//thead/tr[2]'))
            titles = rowtitles.find_elements(By.TAG_NAME,'th')
            datos_titles =  [title.text for title in titles]


            # EXTRAE LOS DATOS DEL CUERPO
            filas = _XpathBody.find_elements(By.TAG_NAME, "tr")

            for fila in filas: 

                celdas = fila.find_elements(By.TAG_NAME,('td'))
                datos_filas = [celda.text for celda in celdas]
                dataBody.append(datos_filas)

            for d in dataBody:
                d[1]= self.eliminateNumbersName(d[1])
            

            df = pd.DataFrame(dataBody, columns=datos_titles
                    )
            try:
                df.to_csv('Mexico_b.csv',index=False,encoding='utf-8-sig')
                print("ARCHIVO EXPORTADO")
            except:
                df.to_csv('Mexico_b_problem.csv',index=False,encoding='utf-8-sig') 
            

                



    def extractTableData_Mex_Proyeccion(self ):

        self.driver.get(self.url)
        self.driver.implicitly_wait(5)

        dataHead    =   []
        dataBody    =   []

        XpathTable = "//Table[preceding::h3/span[@id='Proyecciones_de_población_2010-2030_(CONAPO)']][./following-sibling::div]"
        _TableP = self.driver.find_element(By.XPATH, XpathTable ) 

        _XpathHead =  _TableP.find_element(By.TAG_NAME,  "thead")
        _XpathBody =  _TableP.find_element(By.TAG_NAME,  "tbody")

        control= 1
        # EXTRAE LOS TITULOS DE LA TABLA
        rowtitlesP = _XpathHead.find_elements(By.TAG_NAME,('tr'))
        
        for row in rowtitlesP:
            if control != 1:
                titles = row.find_elements(By.TAG_NAME,'th')
                datos_titles =  [title.text for title in titles]
                control += 1  
            else:
                control += 1    


        # EXTRAE LOS DATOS DEL CUERPO
        filas = _XpathBody.find_elements(By.TAG_NAME, "tr")

        for fila in filas: 

            celdas = fila.find_elements(By.TAG_NAME,('td'))
            datos_filas = [celda.text for celda in celdas]
            dataBody.append(datos_filas)

        for d in dataBody:
            d[1]= self.eliminateNumbersName(d[1])
        

        df = pd.DataFrame(dataBody, columns=datos_titles
                )
        try:
            df.to_csv('Mexico_c.csv',index=False,encoding='utf-8-sig')
            print("ARCHIVO EXPORTADO")
        except:
            df.to_csv('Mexico_c_problem.csv',index=False,encoding='utf-8-sig') 
        

            


    def extraeTodasTablas(self):
        self.extractTableData_Mex_Proyeccion()
        self.extractTableData_Mex_Censo()
        self.extractTableData_Mex()



    # def extractTableData_Mex_SameClass(self, XpathTable ):

    #     self.driver.get(self.url)
    #     self.driver.implicitly_wait(5)

    #     dataHead    =   []
    #     dataBody    =   []
    #     nameFiles   =   ['b','c']
    #     control     = 0


    #     _xPathTables = self.driver.find_elements(By.XPATH, XpathTable ) 

    #     for table in _xPathTables:

    #         _XpathHead =  table.find_element(By.TAG_NAME,  "thead")
    #         _XpathBody =  table.find_element(By.TAG_NAME,  "tbody")

    #         # EXTRAE LOS TITULOS DE LA TABLA

    #         rowtitles = _XpathHead.find_element(By.XPATH,('//thead/tr[2]'))
    #         titles = rowtitles.find_elements(By.TAG_NAME,'th')
    #         datos_titles =  [title.text for title in titles]
    #         print(datos_titles)


    #         # EXTRAE LOS DATOS DEL CUERPO
    #         filas = _XpathBody.find_elements(By.TAG_NAME, "tr")

    #         for fila in filas: 

    #             celdas = fila.find_elements(By.TAG_NAME,('td'))
    #             datos_filas = [celda.text for celda in celdas]
    #             dataBody.append(datos_filas)

    #         for d in dataBody:
    #             d[1]= self.eliminateNumbersName(d[1])
            

    #         df = pd.DataFrame(dataBody, columns=datos_titles
    #                 )
    #         try:
    #             df.to_csv('Mexico_'+ nameFiles[control] +'.csv',index=False,encoding='utf-8-sig')
    #         except:
    #             df.to_csv('Mexico_'+ nameFiles[control] +'_problem.csv',index=False,encoding='utf-8-sig') 
            

    #         print("ARCHIVO EXPORTADO")


    # ----------------------------------------------------------------------



# M = Mexico()
# #M.test_login_wikipedia('Test_dev_em','+KT@,WRk9LRu#cJ')
# testEstados = M.extraeTodasTablas()



