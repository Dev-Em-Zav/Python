from  estadosUnidosData import USA
from  mexicoData import MEXICO

if __name__ == '__main__':
    M = MEXICO()
    #M.test_login_wikipedia('Test_dev_em','+KT@,WRk9LRu#cJ')
    testEstados = M.extractAllStates()
    dataTopono = M.allDataStateToponomia(testEstados)

