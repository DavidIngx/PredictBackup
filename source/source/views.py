from django.http import HttpResponse
from django.shortcuts import loader, render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model
import pathlib
import pandas as pd
import seaborn as sns
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten
from keras.optimizers import Adam, SGD, Adamax
from keras.models import load_model

print(tf.__version__)


def simple_upload(request):
    os.chdir("/media/linux")
    drives = os.popen("ls","r")
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'load_dataset.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'load_dataset.html',{
    'drives':drives,})



def read_file(request):
    url = request.POST["url"]
    xd = pd.read_excel("http://localhost:8000"+url).astype(str)
    xd["dos"] = xd["dos"].str.replace(' ','')
    mysql=0
    for y in xd.dos:
        if(y =='./BachilleratoVirtual'):
            mysql=1

    if(mysql == 1):

        xd = xd[xd.dos != './BachilleratoVirtual']
        xd = xd[xd.dos != './Biblioteca_Nuevo']
        xd = xd[xd.dos != './Adviser']
        xd = xd[xd.dos != './Diplomados']
        xd = xd[xd.dos != './Helpdesk']
        xd = xd[xd.dos != './IMC']
        xd = xd[xd.dos != './Intranet']
        xd = xd[xd.dos != './Koha']
        xd = xd[xd.dos != './MiNube']
        xd = xd[xd.dos != './PaginaUGC']
        xd = xd[xd.dos != './ReservasCmav']
        xd = xd[xd.dos != './Soporte']
        xd = xd[xd.dos != './SoporteOld']
        xd = xd[xd.dos != './Univirtual']
        xd = xd[xd.dos != './VirtualUlagranco']
        xd = xd[xd.dos != './Juridico']

    else:

        xd = xd[xd.dos != './AUDITORIA']
        xd = xd[xd.dos != './export']
        xd = xd[xd.dos != './export/ICEBERG']
        xd = xd[xd.dos != './RMAN/TCONTROL_NEW']
        xd = xd[xd.dos != './RMAN/UGCDB']
        xd = xd[xd.dos != './RMAN/migra']
        xd = xd[xd.dos != './RMAN/ICEBERG']
        xd = xd[xd.dos != './RMAN']
        xd = xd[xd.dos != './RMAN/TCONTROL']
        xd = xd[xd.dos != './export/UGCDB']
        xd = xd[xd.dos != './export/TCONTROL']
        xd = xd[xd.dos != './export/PRUEBA']
        xd = xd[xd.dos != './export/RMAN']

    xd = xd[xd.dos != './lost+found']
    xd = xd[xd.dos.str.contains('logs', na=False) == False ]
    xd = xd[xd.dos.str.contains('.log', na=False) == False ]
    xd = xd[xd.dos.str.contains('SystemVolumeInformation', na=False) == False ]
    xd = xd[xd.dos.str.contains('NIIF', na=False) == False ]
    xd = xd[xd.dos.str.contains('scripts', na=False) == False ]
    xd = xd[xd.dos.str.contains('script', na=False) == False ]
    xd = xd[xd.dos.str.contains('LOG', na=False) == False ]
    xd = xd[xd.dos.str.contains('RECYCLE', na=False) == False ]
    xd = xd[xd.dos.str.contains('pdf', na=False) == False ]
    xd = xd[xd.dos.str.contains('nan', na=False) == False ]
    xd = xd[xd.dos.str.contains('./lost+found', na=False) == False ]
    xd = xd[xd.dos.str.contains('.dll', na=False) == False ]
    xd = xd[xd.dos.str.contains('AUDITORIA', na=False) == False ]
    xd = xd[xd.dos.str.contains('_NEW', na=False) == False ]
    xd = xd[xd.dos.str.contains('PRUEBA', na=False) == False ]

    if(mysql == 0):
        xd4 = pd.DataFrame(xd.dos.str.split('/',3).tolist(), columns=["Raiz","SubDir","SubDir2","Nombre"])
    else:
        xd4 = pd.DataFrame(xd.dos.str.split('/',3).tolist(),columns=["Raiz","SubDir2","Nombre"])
        xd4.insert(loc=1, column='SubDir', value="2")

    xd["uno"] = xd["uno"].str.replace(' ',',')
    xd["uno"] = xd["uno"].str.replace(',,',',')
    xd["uno"] = xd["uno"].str.replace(',,,,',',')
    xd["uno"] = xd["uno"].str.replace('[',',')
    xd["uno"] = xd["uno"].str.replace(',','/')
    xd["uno"] = xd["uno"].str.replace('///','/')
    xd["uno"] = xd["uno"].str.replace('//','/')

    if(mysql == 0 ):
        xd5 = pd.DataFrame(xd.uno.str.split('/',4).tolist())
        xd5 = xd5.rename(columns={1: "Tamaño", 2: "Mes", 3:"Dia", 4:"Año"})
        xd5 = xd5.drop(columns=[0])
    else:
        xd5 = pd.DataFrame(xd.uno.str.split('/',6).tolist(), columns=["0","Tamaño", "Mes", "Dia","Año"])
        xd5 = xd5.drop(columns=['0'])

    xd5["Tamaño"] = xd5["Tamaño"].astype(int)

    xd5["Raiz"]=xd4["Raiz"]
    xd5["SubDir"]=xd4["SubDir"]
    xd5["SubDir2"]=xd4["SubDir2"]
    xd5["Nombre"]=xd4["Nombre"]

    xd5["Mes"] = xd5["Mes"].astype(str)

    xd5["Mes"] = xd5["Mes"].str.replace('Jan','1')
    xd5["Mes"] = xd5["Mes"].str.replace('Feb','2')
    xd5["Mes"] = xd5["Mes"].str.replace('Mar','3')
    xd5["Mes"] = xd5["Mes"].str.replace('Apr','4')
    xd5["Mes"] = xd5["Mes"].str.replace('May','5')
    xd5["Mes"] = xd5["Mes"].str.replace('Jun','6')
    xd5["Mes"] = xd5["Mes"].str.replace('Jul','7')
    xd5["Mes"] = xd5["Mes"].str.replace('Aug','8')
    xd5["Mes"] = xd5["Mes"].str.replace('Sep','9')
    xd5["Mes"] = xd5["Mes"].str.replace('Oct','10')
    xd5["Mes"] = xd5["Mes"].str.replace('Nov','11')
    xd5["Mes"] = xd5["Mes"].str.replace('Dec','12')

    xd5["Raiz"] = xd5["Raiz"].str.replace('.','0') #Raiz = 0
    if(mysql == 0):
        xd5["SubDir"] = xd5["SubDir"].str.replace('export','0') #export = 0
        xd5["SubDir"] = xd5["SubDir"].str.replace('RMAN','1') #RMAN = 0
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('ICEBERG','1') #ICEBERG = 1
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('RMAN','2') #RMAN = 2
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('TCONTROL','3') #TCONTROL = 3
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('UGCDB','4') # UGCDB = 4
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('migra','5') # migra = 5

    else:
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('BachilleratoVirtual','8') #BachilleratoVirtual = 8
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Biblioteca_Nuevo','9') #Biblioteca_Nuevo = 9
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Adviser','7') #Adviser = 7
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Diplomados','10') #Diplomados = 10
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Helpdesk','11') #Helpdesk = 11
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('IMC','12') #IMC = 12
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Intranet','13') #Intranet = 13
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Koha','14') #Koha = 14
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('MiNube','15') #MiNube = 15
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('PaginaUGC','16') #PaginaUGC = 16
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('ReservasCmav','17') #ReservasCmav = 17
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('SoporteOld','19') #SoporteOld = 19
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Soporte','18') #Soporte = 18
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Univirtual','20') #Univirtual = 20
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('VirtualUlagranco','21') #VirtualUlagranco = 21
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Juridico','22') #VirtualUlagranco = 22

    count=0;
    for row in xd5["Año"]:

        if (row == 2017 ):
            print()

        else:
            xd5.loc[count, 'Año'] = 2018
        count+=1;


    xd5["Tamaño"] = xd5["Tamaño"].astype(int)
    xd5["Mes"] = xd5["Mes"].astype(int)
    xd5["Dia"] = xd5["Dia"].astype(int)
    xd5["Año"] = xd5["Año"].astype(int)
    xd5["Raiz"] = xd5["Raiz"].astype(int)
    xd5["SubDir"] = xd5["SubDir"].astype(int)
    xd5["SubDir2"] = xd5["SubDir2"].astype(int)
    xd5["Nombre"] = xd5["Nombre"].astype(str)

    count=0;
    for row in xd5["Mes"]:

        if (row == 10 ):
            xd5.loc[count, 'Año'] = 2017
        if (row == 11 ):
            xd5.loc[count, 'Año'] = 2017
        if (row == 12 ):
            xd5.loc[count, 'Año'] = 2017




        count+=1;

    filedb = pd.read_csv('/home/linux/PredictBackup/source/media/db.csv')
    filedb = pd.concat([filedb, xd5],ignore_index=True)

    filedb.to_csv('/home/linux/PredictBackup/source/media/db.csv',index=False)

    mylist = zip(xd5["Tamaño"].tail(), xd5["Mes"].tail(), xd5["Dia"].tail(), xd5["Año"].tail(), xd5["Raiz"].tail(), xd5["SubDir"].tail(), xd5["SubDir2"].tail(), xd5["Nombre"].tail())


    return render(request, 'showfile.html', {
                            'dataframe': mylist,
                            'select':url,
})


def read_disk(request):

    drive = request.POST["disk"]
    drive = drive.replace('\r\n','')
    os.chdir("/media/linux/"+drive)
    #os.chdir("/home/linux/Documents/oracle")
    command = os.popen("tree  -D  -f -s -i ","r")
    xd = pd.DataFrame(columns=['inicio'])

    for line in command:
        xd = xd.append({'inicio': line}, ignore_index=True)

    xd = xd[xd.inicio != '.\n']
    xd = xd[xd.inicio != '\n']
    xd = xd[xd.inicio.str.contains('directories', na=False) == False ]
    xd = pd.DataFrame(xd.inicio.str.split(']',2).tolist(), columns=["uno","dos"])
    xd["dos"] = xd["dos"].str.replace(' ','')
    xd["dos"] = xd["dos"].str.replace('\n','')

    mysql=0
    for y in xd.dos:
        if(y =='./BachilleratoVirtual'):
            mysql=1
            print(mysql)

    if(mysql == 1):

        xd = xd[xd.dos != './BachilleratoVirtual']
        xd = xd[xd.dos != './Biblioteca_Nuevo']
        xd = xd[xd.dos != './Adviser']
        xd = xd[xd.dos != './Diplomados']
        xd = xd[xd.dos != './Helpdesk']
        xd = xd[xd.dos != './IMC']
        xd = xd[xd.dos != './Intranet']
        xd = xd[xd.dos != './Koha']
        xd = xd[xd.dos != './MiNube']
        xd = xd[xd.dos != './PaginaUGC']
        xd = xd[xd.dos != './ReservasCmav']
        xd = xd[xd.dos != './Soporte']
        xd = xd[xd.dos != './SoporteOld']
        xd = xd[xd.dos != './Univirtual']
        xd = xd[xd.dos != './VirtualUlagranco']
        xd = xd[xd.dos != './Juridico']
    else:

        xd = xd[xd.dos != './AUDITORIA']
        xd = xd[xd.dos != './export']
        xd = xd[xd.dos != './export/ICEBERG']
        xd = xd[xd.dos != './RMAN/TCONTROL_NEW']
        xd = xd[xd.dos != './RMAN/UGCDB']
        xd = xd[xd.dos != './RMAN/migra']
        xd = xd[xd.dos != './RMAN/ICEBERG']
        xd = xd[xd.dos != './RMAN']
        xd = xd[xd.dos != './export/UGCDB']
        xd = xd[xd.dos != './export/TCONTROL']
        xd = xd[xd.dos != './export/PRUEBA']
        xd = xd[xd.dos != './export/RMAN']
        xd = xd[xd.dos != './RMAN/RMAN']
        xd = xd[xd.dos != './RMAN/TCONTROL']
        xd = xd[xd.dos != './export/migra']



    xd = xd[xd.dos != './lost+found']
    xd = xd[xd.dos != './n']
    xd = xd[xd.dos.str.contains('logs', na=False) == False ]
    xd = xd[xd.dos.str.contains('.log', na=False) == False ]
    xd = xd[xd.dos.str.contains('SystemVolumeInformation', na=False) == False ]
    xd = xd[xd.dos.str.contains('NIIF', na=False) == False ]
    xd = xd[xd.dos.str.contains('scripts', na=False) == False ]
    xd = xd[xd.dos.str.contains('script', na=False) == False ]
    xd = xd[xd.dos.str.contains('LOG', na=False) == False ]
    xd = xd[xd.dos.str.contains('RECYCLE', na=False) == False ]
    xd = xd[xd.dos.str.contains('pdf', na=False) == False ]
    xd = xd[xd.dos.str.contains('nan', na=False) == False ]
    xd = xd[xd.dos.str.contains('./lost+found', na=False) == False ]
    xd = xd[xd.dos.str.contains('.dll', na=False) == False ]
    xd = xd[xd.dos.str.contains('AUDITORIA', na=False) == False ]
    xd = xd[xd.dos.str.contains('_NEW', na=False) == False ]
    xd = xd[xd.dos.str.contains('PRUEBA', na=False) == False ]

    if(mysql == 0):
        xd4 = pd.DataFrame(xd.dos.str.split('/',3).tolist(), columns=["Raiz","SubDir","SubDir2","Nombre"])
    else:
        xd4 = pd.DataFrame(xd.dos.str.split('/',3).tolist(),columns=["Raiz","SubDir2","Nombre"])
        xd4.insert(loc=1, column='SubDir', value="2")

    xd["uno"] = xd["uno"].str.replace(' ',',')

    xd["uno"] = xd["uno"].str.replace(',,',',')
    xd["uno"] = xd["uno"].str.replace(',,,,',',')
    xd["uno"] = xd["uno"].str.replace('[',',')
    xd["uno"] = xd["uno"].str.replace(',','/')
    xd["uno"] = xd["uno"].str.replace('///','/')
    xd["uno"] = xd["uno"].str.replace('//','/')


    if(mysql == 0 ):
        xd5 = pd.DataFrame(xd.uno.str.split('/',6).tolist(), columns=["0","Tamaño", "Mes", "Dia","Año"])

        xd5 = xd5.drop(columns=["0"])
    else:
        xd5 = pd.DataFrame(xd.uno.str.split('/',6).tolist(), columns=["0","Tamaño", "Mes", "Dia","Año"])
        xd5 = xd5.drop(columns=['0'])



    xd5["Raiz"]=xd4["Raiz"]
    xd5["SubDir"]=xd4["SubDir"]
    xd5["SubDir2"]=xd4["SubDir2"]
    xd5["Nombre"]=xd4["Nombre"]

    xd5["Mes"] = xd5["Mes"].astype(str)

    xd5["Mes"] = xd5["Mes"].str.replace('Jan','1')
    xd5["Mes"] = xd5["Mes"].str.replace('Feb','2')
    xd5["Mes"] = xd5["Mes"].str.replace('Mar','3')
    xd5["Mes"] = xd5["Mes"].str.replace('Apr','4')
    xd5["Mes"] = xd5["Mes"].str.replace('May','5')
    xd5["Mes"] = xd5["Mes"].str.replace('Jun','6')
    xd5["Mes"] = xd5["Mes"].str.replace('Jul','7')
    xd5["Mes"] = xd5["Mes"].str.replace('Aug','8')
    xd5["Mes"] = xd5["Mes"].str.replace('Sep','9')
    xd5["Mes"] = xd5["Mes"].str.replace('Oct','10')
    xd5["Mes"] = xd5["Mes"].str.replace('Nov','11')
    xd5["Mes"] = xd5["Mes"].str.replace('Dec','12')

    xd5["Raiz"] = xd5["Raiz"].str.replace('.','0') #Raiz = 0
    if(mysql == 0):
        xd5["SubDir"] = xd5["SubDir"].str.replace('export','0') #export = 0
        xd5["SubDir"] = xd5["SubDir"].str.replace('RMAN','1') #RMAN = 0
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('ICEBERG','1') #ICEBERG = 1
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('RMAN','2') #RMAN = 2
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('TCONTROL','3') #TCONTROL = 3
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('UGCDB','4') # UGCDB = 4
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('migra','5') # migra = 5

    else:
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('BachilleratoVirtual','8') #BachilleratoVirtual = 8
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Biblioteca_Nuevo','9') #Biblioteca_Nuevo = 9
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Adviser','7') #Adviser = 7
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Diplomados','10') #Diplomados = 10
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Helpdesk','11') #Helpdesk = 11
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('IMC','12') #IMC = 12
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Intranet','13') #Intranet = 13
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Koha','14') #Koha = 14
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('MiNube','15') #MiNube = 15
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('PaginaUGC','16') #PaginaUGC = 16
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('ReservasCmav','17') #ReservasCmav = 17
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('SoporteOld','19') #SoporteOld = 19
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Soporte','18') #Soporte = 18
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Univirtual','20') #Univirtual = 20
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('VirtualUlagranco','21') #VirtualUlagranco = 21
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Juridico','22') #VirtualUlagranco = 22

        xd5["Tamaño"] = xd5["Tamaño"].astype(int)
        xd5["Mes"] = xd5["Mes"].astype(int)
        xd5["Dia"] = xd5["Dia"].astype(int)
        xd5["Año"] = xd5["Año"].astype(int)
        xd5["Raiz"] = xd5["Raiz"].astype(int)
        xd5["SubDir"] = xd5["SubDir"].astype(int)
        xd5["SubDir2"] = xd5["SubDir2"].astype(int)
        xd5["Nombre"] = xd5["Nombre"].astype(str)

    count=0;
    for row in xd5["Mes"]:

        if (row == 10 ):
            xd5.loc[count, 'Año'] = 2017
        if (row == 11 ):
            xd5.loc[count, 'Año'] = 2017
        if (row == 12 ):
            xd5.loc[count, 'Año'] = 2017


        count+=1;

    filedb = pd.read_csv('/home/linux/PredictBackup/source/media/db.csv')
    filedb = pd.concat([filedb, xd5],ignore_index=True)

    filedb.to_csv('/home/linux/PredictBackup/source/media/db.csv',index=False)



    mylist = zip(xd5["Tamaño"].tail(), xd5["Mes"].tail(), xd5["Dia"].tail(), xd5["Año"].tail(), xd5["Raiz"].tail(), xd5["SubDir"].tail(), xd5["SubDir2"].tail(), xd5["Nombre"].tail())

    return render(request, 'showfile.html', {
                            'dataframe': mylist,
                            'select':drive, })



def load_dataset(request):
    url = request.POST["url"]
    return render(request, "prueba.html",{"url":url})


def train_view(request):
    dataset = pd.read_csv("http://127.0.0.1:8000/media/db3.csv")
    subdir = dataset.pop('SubDir2')
    subdirprin = dataset.pop('SubDir')
    dataset['RMAN'] = (subdirprin == 1)*1.0
    dataset['export'] = (subdirprin == 0)*1.0
    dataset['MySQL'] = (subdirprin == 2)*1.0
    dataset['ICEBERG'] = (subdir == 1)*1.0
    dataset['RMANINT'] = (subdir == 2)*1.0
    dataset['TCONTROL'] = (subdir == 3)*1.0
    dataset['UGCDB'] = (subdir == 4)*1.0
    dataset['migra'] = (subdir == 5)*1.0
    dataset['Adviser'] = (subdir == 7)*1.0
    dataset['BachilleratoVirtual'] = (subdir == 8)*1.0
    dataset['Biblioteca_Nuevo'] = (subdir == 9)*1.0
    dataset['Diplomados'] = (subdir == 10)*1.0
    dataset['Helpdesk'] = (subdir == 11)*1.0
    dataset['IMC'] = (subdir == 12)*1.0
    dataset['Intranet'] = (subdir == 13)*1.0
    # dataset['Koha'] = (subdir == 14)*1.0
    dataset['MiNube'] = (subdir == 15)*1.0
    dataset['PaginaUGC'] = (subdir == 16)*1.0
    dataset['ReservasCmav'] = (subdir == 17)*1.0
    dataset['Soporte'] = (subdir == 18)*1.0
    dataset['SoporteOld'] = (subdir == 19)*1.0
    dataset['Univirtual'] = (subdir == 20)*1.0
    dataset['VirtualUlagranco'] = (subdir == 21)*1.0
    dataset['Juridico'] = (subdir == 22)*1.0
    namefile = dataset.pop('Nombre')
    dataset["Tamaño"] /= 1000000000
    train_dataset = dataset.sample(frac=0.9,random_state=0)
    test_dataset = dataset.drop(train_dataset.index)
    sns_plot = sns.pairplot(train_dataset[["Tamaño", "Dia", "Mes"]], diag_kind="kde")
    sns_plot.savefig("/home/linux/PredictBackup/source/media/analisis.png")
    train_stats = train_dataset.describe()
    train_stats.pop("Tamaño")
    train_stats = train_stats.transpose()
    train_labels = train_dataset.pop('Tamaño')
    test_labels = test_dataset.pop('Tamaño')

    def norm(x):
        return (x - train_stats['mean']) / train_stats['std']

    normed_train_data = norm(train_dataset)
    normed_test_data = norm(test_dataset)

    def build_model():
        model = Sequential()
        model.add(Dense(64, activation="relu", input_shape=[len(train_dataset.keys())]))
        model.add(Dense(1))
        optimizer = Adamax(0.0007)
        model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])
        return model

    model = build_model()
    example_batch = normed_train_data[:10]
    example_result = model.predict(example_batch)

    # Display training progress by printing a single dot for each completed epoch
    class PrintDot(keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs):
            if epoch % 100 == 0: print('')
            print('.', end='')

    EPOCHS = 10

    history = model.fit(
      normed_train_data, train_labels,
      epochs=EPOCHS, validation_split = 0.2, verbose=0,
      callbacks=[PrintDot()])
    model.save('/home/linux/PredictBackup/source/media/my_model.h5')
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch


    def plot_history(history):
        plt.figure()
        plt.xlabel('Epoch')
        plt.ylabel('Mean Abs Error [Tamaño]')
        plt.plot(hist['epoch'], hist['mean_absolute_error'],
               label='Train Error')
        plt.plot(hist['epoch'], hist['val_mean_absolute_error'],
               label = 'Val Error')
        plt.legend()
        plt.ylim([0,0.5])
        plt.savefig('/home/linux/PredictBackup/source/media/absolute.png')
        plt.figure()
        plt.xlabel('Epoch')
        plt.ylabel('Mean Square Error [$Tamaño^2$]')
        plt.plot(hist['epoch'], hist['mean_squared_error'],
               label='Train Error')
        plt.plot(hist['epoch'], hist['val_mean_squared_error'],
               label = 'Val Error')
        plt.legend()
        plt.ylim([0,1.5])
        plt.savefig('/home/linux/PredictBackup/source/media/squared.png')

    plot_history(history)




    return render(request, "train.html")

def predict_view(request):
    dataset = pd.read_csv("http://127.0.0.1:8000/media/db3.csv")
    subdir = dataset.pop('SubDir2')
    subdirprin = dataset.pop('SubDir')
    dataset['RMAN'] = (subdirprin == 1)*1.0
    dataset['export'] = (subdirprin == 0)*1.0
    dataset['MySQL'] = (subdirprin == 2)*1.0
    dataset['ICEBERG'] = (subdir == 1)*1.0
    dataset['RMANINT'] = (subdir == 2)*1.0
    dataset['TCONTROL'] = (subdir == 3)*1.0
    dataset['UGCDB'] = (subdir == 4)*1.0
    dataset['migra'] = (subdir == 5)*1.0
    dataset['Adviser'] = (subdir == 7)*1.0
    dataset['BachilleratoVirtual'] = (subdir == 8)*1.0
    dataset['Biblioteca_Nuevo'] = (subdir == 9)*1.0
    dataset['Diplomados'] = (subdir == 10)*1.0
    dataset['Helpdesk'] = (subdir == 11)*1.0
    dataset['IMC'] = (subdir == 12)*1.0
    dataset['Intranet'] = (subdir == 13)*1.0
    # dataset['Koha'] = (subdir == 14)*1.0
    dataset['MiNube'] = (subdir == 15)*1.0
    dataset['PaginaUGC'] = (subdir == 16)*1.0
    dataset['ReservasCmav'] = (subdir == 17)*1.0
    dataset['Soporte'] = (subdir == 18)*1.0
    dataset['SoporteOld'] = (subdir == 19)*1.0
    dataset['Univirtual'] = (subdir == 20)*1.0
    dataset['VirtualUlagranco'] = (subdir == 21)*1.0
    dataset['Juridico'] = (subdir == 22)*1.0
    namefile = dataset.pop('Nombre')
    dataset["Tamaño"] /= 1000000000
    train_dataset = dataset.sample(frac=0.9,random_state=0)
    test_dataset = dataset.drop(train_dataset.index)

    train_stats = train_dataset.describe()
    train_stats.pop("Tamaño")
    train_stats = train_stats.transpose()
    train_labels = train_dataset.pop('Tamaño')
    test_labels = test_dataset.pop('Tamaño')

    def norm(x):
        return (x - train_stats['mean']) / train_stats['std']

    normed_train_data = norm(train_dataset)
    normed_test_data = norm(test_dataset)

    model = load_model('/home/linux/PredictBackup/source/media/my_model.h5')
    test_predictions = model.predict(normed_test_data).flatten()
    plt.scatter(test_labels, test_predictions)
    plt.xlabel('True Values [Tamaño]')
    plt.ylabel('Predictions [Tamaño]')
    plt.axis('equal')
    plt.axis('square')
    plt.xlim([0,plt.xlim()[1]])
    plt.ylim([0,plt.ylim()[1]])
    _ = plt.plot([-100, 100], [-100, 100])
    plt.savefig('/home/linux/PredictBackup/source/media/predict.png')

    return render(request, "predict.html")






def result_view(request):
    size = int(request.POST["size"])

    dataset = pd.read_csv("http://127.0.0.1:8000/media/db3.csv")
    subdir = dataset.pop('SubDir2')
    subdirprin = dataset.pop('SubDir')
    dataset['RMAN'] = (subdirprin == 1)*1.0
    dataset['export'] = (subdirprin == 0)*1.0
    dataset['MySQL'] = (subdirprin == 2)*1.0
    dataset['ICEBERG'] = (subdir == 1)*1.0
    dataset['RMANINT'] = (subdir == 2)*1.0
    dataset['TCONTROL'] = (subdir == 3)*1.0
    dataset['UGCDB'] = (subdir == 4)*1.0
    dataset['migra'] = (subdir == 5)*1.0
    dataset['Adviser'] = (subdir == 7)*1.0
    dataset['BachilleratoVirtual'] = (subdir == 8)*1.0
    dataset['Biblioteca_Nuevo'] = (subdir == 9)*1.0
    dataset['Diplomados'] = (subdir == 10)*1.0
    dataset['Helpdesk'] = (subdir == 11)*1.0
    dataset['IMC'] = (subdir == 12)*1.0
    dataset['Intranet'] = (subdir == 13)*1.0
    # dataset['Koha'] = (subdir == 14)*1.0
    dataset['MiNube'] = (subdir == 15)*1.0
    dataset['PaginaUGC'] = (subdir == 16)*1.0
    dataset['ReservasCmav'] = (subdir == 17)*1.0
    dataset['Soporte'] = (subdir == 18)*1.0
    dataset['SoporteOld'] = (subdir == 19)*1.0
    dataset['Univirtual'] = (subdir == 20)*1.0
    dataset['VirtualUlagranco'] = (subdir == 21)*1.0
    dataset['Juridico'] = (subdir == 22)*1.0
    namefile = dataset.pop('Nombre')
    dataset["Tamaño"] /= 1000000000
    train_dataset = dataset.sample(frac=0.9,random_state=0)
    test_dataset = dataset.drop(train_dataset.index)

    train_stats = train_dataset.describe()
    train_stats.pop("Tamaño")
    train_stats = train_stats.transpose()
    train_labels = train_dataset.pop('Tamaño')
    test_labels = test_dataset.pop('Tamaño')

    def norm(x):
        return (x - train_stats['mean']) / train_stats['std']



    model = load_model('/home/linux/PredictBackup/source/media/my_model.h5')
    seismeses = pd.read_csv("/home/linux/PredictBackup/source/media/predictgood.csv")
    normed_predict = norm(seismeses)
    prediction_last = model.predict(normed_predict).flatten()
    seismeses["Tamaño"] = prediction_last

    i=0.0
    for suma in prediction_last:
        if(suma < 0):
            suma = suma * -1
        i += suma

    discos = round(i/size)


    return render(request, "result.html",  {'select':discos,})
