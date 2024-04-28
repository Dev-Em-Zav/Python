
import selenium
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager



class USA:

    def __init__(self, nav='CHR'):

        self.url  ='https://es.wikipedia.org/wiki/Estado_de_los_Estados_Unidos'
        self.urlNav = ('https://es.wikipedia.org/wiki/')
        

        if (nav.upper() == 'CHR'):
            options = webdriver.ChromeOptions()
            self.driver = webdriver.Chrome(options=options)
            self.driver.get(self.urlNav)
            
        elif (nav.upper() == 'MOZ'):
            options = webdriver.FirefoxOptions()
            self.driver = webdriver.Firefox(options=options)
            self.driver.get(self.urlNav)

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




    '''
    FUNCION DE EXTRACCION DE TABLAS DE USA
    SE USA DATAFRAME DE PANDA PARA PODER DESCARGAR LA INFORMACIÓN.
    '''

    def extractTableData_USA(self):
        self.driver.get(self.url)

        '''
        SELECCIONA CON LA PARTE PRINCIPAL DE LA INFORMACIÓN
        TRAS UN ANALISIS DE LA TABLA LA ESTRUCTURA PRESENTA CELDAS COMBINADAS 
        >>//TD/COL

        CUANDO ESTÁS UTILIZANDO SELENIUM PARA INTERACTUAR CON ELEMENTOS DE UNA TABLA
        QUE CONTIENEN COLSPAN, PUEDE SER UN POCO COMPLICADO PORQUE SELENIUM GENERALMENTE 
        TRABAJA A NIVEL DE ELEMENTO Y NO MANEJA DIRECTAMENTE LA MANIPULACIÓN DE ATRIBUTOS 
        DE TABLA.
        
        POR LO CUAL SE PLANTEA TRABAJAR A ELEMENTO DE /TR DE LA TABLA, AL ENCONTRAR UN VARIACION DE 
        EN LA LONFGITUD DE CADA FILA CONTENIDA EN LA TABLA CON EL PROMEDIO DE ESTA, SE INCERTARIA 
        EL VALOR DE LA POSICIÓN 4 EN LA 5 DEL  EN LA TABLA PARA CONTENER EL MISMO VALOR EN LOS CAMPOS
        DE LA CIUDAD:
                "CAPITAL",
                "CIUDAD MAS POBLADA 2006",
        '''

        _XpathBody =  "//Table[@class='wikitable sortable jquery-tablesorter']/tbody"
        tbody = self.driver.find_element(By.XPATH, _XpathBody)
        filas = tbody.find_elements(By.TAG_NAME, "tr")

        dataBody = []

        for fila in filas:         
            celdas = fila.find_elements(By.TAG_NAME,('td'))
            datos_filas = [celda.text for celda in celdas]
            

            if len(datos_filas) != 10 :
                datos_filas.insert(6,datos_filas[5])
                dataBody.append(datos_filas)
            else:     
                dataBody.append(datos_filas)

        for d in dataBody:
            d[1]= self.eliminateNumbersName(d[1])
        

        df = pd.DataFrame(dataBody, columns=[
                "BANDERA", 
                "ESTADO",
                "NOMBRE OFICIAL",
                "ABREVIACIO",
                "INGRESO A LA UNIO",
                "CAPITAL",
                "CIUDAD MAS POBLADA 2006",
                "POBLACION (2020)",
                "DENSIDAD (Hab/km2)",
                "SUPERFICIE"
                ]
                )
        try:
            df.to_csv('Estados_Unidos_a.csv',index=False,encoding='utf-8-sig')
        except:
            df.to_csv('Estados_Unidos_a_problem.csv',index=False,encoding='utf-8-sig') 
        

        print("ARCHIVO EXPORTADO")




    '''
    EXTRAE UNA LISTA DE LOS ESTADOS DIRECTAMENTE DE LA TABLA
        - HACE UN AJUSTE PARA PODER ELIMINAR LOS NÚMERO DE AQUELLOS QUE LO CONTIENEN
    '''


    def extractAllStates(self):

        # REGRESA A LA PÁGINA PRINCIPAL DE ESTADOS UNIDOS 
        # POR SI SE ENCONTRABA EN OTRA FASE DE EXTRACCIÓN
          
        self.driver.get(self.url)
        self.driver.implicitly_wait(3)

        statesList =[]

        all_States = self.driver.find_elements(By.XPATH,
                                                    ("//Table[@class='wikitable sortable jquery-tablesorter']/tbody/tr/td[2]"))

        for _s in all_States:
            if(_s.text !="Población" and _s.text !="Nombre" ):
                statesList.append( self.eliminateNumbersName(_s.text) )
                #print(self.eliminateNumbersName(_s.text) )
        return (statesList)


    '''
    EXTRAE LA INFORMACIÓN DE UNA LISTA DE ESTADOS. 
    '''

    #EXTRAE LA LISTA COMPLETA DE DATOS DE TODOS LOS ESTADOS EN UNA LISTA
    def allDataStateEtim(self,states, genFile=True):
        arrData=[]
        for s in states:
            arrData.append(self.dataState(s))
        
        if genFile:
            with open(r'Eti_USA.txt', 'w',encoding='utf-8-sig') as fp:
                for item in arrData:
                    fp.write("%s\n" % item)

            print('DATOS EXTRAIDOS')
        return arrData


    #FUNCION DE EXTRACCION DE DATOS  INDIVIDUAL
    def dataState(self,state):
        
        #self.driver.get(self.url)
        stateUrl = self.urlNav + state
        self.driver.get(stateUrl)
        
        arrData=[]

        try:
            data = self.driver.find_elements(By.XPATH, "//p[preceding-sibling::h2[1]/span[text()='Etimología']] [./following-sibling::h2]")

            for p in data:
                arrData.append(p.text)
                #print(p.text)        
            #print(arrData)

            return {state:arrData}
        
        except:
            return {state:'No data'}



'''

U = USA(nav='CHR')

#TIME LOGIN
begin_1 = time.time()

U.test_login_wikipedia('Test_dev_em','+KT@,WRk9LRu#cJ')
end_1 = time.time()
print("LOGIN TIME:", end_1 - begin_1)


#TIME TABLE DATA
begin_2 = time.time()

U.extractTableData_USA()

end_2 = time.time()
print("TABLE TIME:", end_2 - begin_2)


#TIME LIST STATE
begin_3 = time.time()

TestState = U.extractAllStates()
print(TestState)
print("\n \n")

end_3 = time.time()
print("STATES TIME:", end_3 - begin_3)


#TIME LIST STATE
begin_4 = time.time()

TestState = U.allDataStateEtim(TestState)
print(TestState)
print("\n \n")

end_4 = time.time()
print("Eti TIME:", end_3 - begin_3)

'''