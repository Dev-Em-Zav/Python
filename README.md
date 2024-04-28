# Evaluation Web Scrapping

Version 1 

This repository allow to dowload information from wikipedia. 
The main pages to starct data are:

 Site Estado de los Estados Unidos - [link]('https://es.wikipedia.org/wiki/Estado_de_los_Estados_Unidos')

 Site Entidades federativas de México por superficie, población y densidad [link] ('https://es.wikipedia.org/wiki/Anexo:Entidades_federativas_de_M%C3%A9xico_por_superficie,_poblaci%C3%B3n_y_densidad')

The information use Panda Framework and the Openpyxl library to export the information to Excel. 
It is configurated to extract each table in different excel files. Openpyxl allow to write and word with differents sheets in the same file.


## Installation


Use the package manager [pip](https://pip.pypa.io/en/stable/) to install :
 
 1. webdriver-manager 4.0.1 
 Library to simplify management of binary drivers for different browsers.

 ```bash
pip install webdriver-manager
```
        - librería       : webdriver-manager 4.0.1
        - Comando        : pip install webdriver-manager
        - Documentación  : https://pypi.org/project/webdriver-manager/


  2. Pandas      

  Pandas: powerful Python data analysis toolkit
```bash
pip install pandas
```
        - librería       : pandas 2.2.2
        - Comando        : pip install pandas
        - Documentación  : https://pandas.pydata.org/pandas-docs/stable/



  3. Openpyxl

Openpyxl is a Python library to read/write Excel 2010 xlsx/xlsm/xltx/xltm files.
```bash
pip install openpyxl
```

        - librería       : openpyxl 3.1.2
        - Comando        : pip install openpyxl
        - Documentación  : https://openpyxl.readthedocs.io/en/stable/


  4. selenium 4.20.0
```bash
pip install selenium
```
The selenium package is used to automate web browser interaction from Python.


        - librería       : selenium 4.20.0
        - Comando        : pip install selenium
        - Documentación  : https://selenium.dev




## USAGE 

### USA

```python
import estadosUnidosData


#DECLARAR VARIABLE DE LA CLASE
U = USA(nav='CHR')

#TIME LOGIN
# TRANSACCION PARA INGRESAR CON USUARIO
begin_1 = time.time()    # TESTEAR TIEMPOS DE EJECUCIÓN 
U.test_login_wikipedia('Test_dev_em','+KT@,WRk9LRu#cJ')
end_1 = time.time()      # tESTEAR tIEMPOS DE EJECUIÓN CON FINAL
print("LOGIN TIME:", end_1 - begin_1)


#EXTRAER TABLA DE LA ENTIDADES USA
# Extrae los elementos con ayuda del dataframe de Panda.
U.extractTableData_USA()

#----------------- 

#EXTRACCION DE LOS ESTADOS
# La información se extrae en formato de lista con todos los elementos de la tabla
TestState = U.extractAllStates()

#EXTRACCION DE CAMPO DE ETIMOLOGIA
#NOTA: SE REQUIERE UNA LISTA DE ESTADOS PARA SU EXTRACCION.
# La transaccion tambien puede guardar un archivo con la inforcación en formato TXT
TestEti = U.allDataStateEtim(TestState)

```



### MEXICO

```python
import mexicoData


#DECLARAR VARIABLE DE LA CLASE
# NAV -'MOZ' PARA MOZILLA
# NAV -'CHR' PARA CHROME
M = MEXICO(nav='CHR')

#TIME LOGIN
# TRANSACCION PARA INGRESAR CON USUARIO
begin_1 = time.time()    # TESTEAR TIEMPOS DE EJECUCIÓN 
U.test_login_wikipedia('Test_dev_em','+KT@,WRk9LRu#cJ')
end_1 = time.time()      # tESTEAR tIEMPOS DE EJECUIÓN CON FINAL
print("LOGIN TIME:", end_1 - begin_1)


#----------------- 

#EXTRACCION DE LOS ESTADOS
# La información se extrae en formato de lista con todos los elementos de la tabla
TestState = M.extractAllStates()

#EXTRACCION DE CAMPO DE ETIMOLOGIA
#NOTA: SE REQUIERE UNA LISTA DE ESTADOS PARA SU EXTRACCION.
# La transaccion tambien puede guardar un archivo con la inforcación en formato TXT
TestEti = M.allDataStateToponomia(TestState)


#EXTRACCION PRIMERA TABLA DE LA PÁGINA
M.extractTableData_Mex()

#EXTRACCION  TABLA DE LA PROYECCION
M.extractTableData_Mex_Proyeccion()

#EXTRACCION TABLA DE CENSO
M.extractTableData_Mex_Censo()

#EXTRACCION DE LAS 3 TABLAS
M.extraeTodasTablas()

```





## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

