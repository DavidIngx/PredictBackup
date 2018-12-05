from django.http import HttpResponse
from django.shortcuts import loader, render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd
import os
import numpy as np

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
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('BachilleratoVirtual','3') #BachilleratoVirtual = 3
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Biblioteca_Nuevo','4') #Biblioteca_Nuevo = 4
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Adviser','2') #Adviser = 2
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Diplomados','5') #Diplomados = 5
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Helpdesk','6') #Helpdesk = 6
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('IMC','7') #IMC = 7
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Intranet','8') #Intranet = 8
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Koha','9') #Koha = 9
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('MiNube','10') #MiNube = 10
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('PaginaUGC','11') #PaginaUGC = 11
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('ReservasCmav','12') #ReservasCmav = 12
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('SoporteOld','14') #SoporteOld = 14
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Soporte','13') #Soporte = 13
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Univirtual','15') #Univirtual = 15
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('VirtualUlagranco','16') #VirtualUlagranco = 16
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Juridico','17') #VirtualUlagranco = 16

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

    mylist = zip(xd5["Tamaño"], xd5["Mes"], xd5["Dia"], xd5["Año"], xd5["Raiz"], xd5["SubDir"], xd5["SubDir2"], xd5["Nombre"])

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
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('BachilleratoVirtual','3') #BachilleratoVirtual = 3
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Biblioteca_Nuevo','4') #Biblioteca_Nuevo = 4
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Adviser','2') #Adviser = 2
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Diplomados','5') #Diplomados = 5
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Helpdesk','6') #Helpdesk = 6
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('IMC','7') #IMC = 7
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Intranet','8') #Intranet = 8
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Koha','9') #Koha = 9
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('MiNube','10') #MiNube = 10
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('PaginaUGC','11') #PaginaUGC = 11
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('ReservasCmav','12') #ReservasCmav = 12
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('SoporteOld','14') #SoporteOld = 14
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Soporte','13') #Soporte = 13
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Univirtual','15') #Univirtual = 15
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('VirtualUlagranco','16') #VirtualUlagranco = 16
        xd5["SubDir2"] = xd5["SubDir2"].str.replace('Juridico','17') #VirtualUlagranco = 16

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



    mylist = zip(xd5["Tamaño"], xd5["Mes"], xd5["Dia"], xd5["Año"], xd5["Raiz"], xd5["SubDir"], xd5["SubDir2"], xd5["Nombre"])

    return render(request, 'showfile.html', {
                            'dataframe': mylist,
                            'select':drive, })



def load_dataset(request):
    url = request.POST["url"]
    return render(request, "prueba.html",{"url":url})
