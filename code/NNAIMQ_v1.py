############################################################################
                    #    #  #    #    ##     #####   ####
                    # #  #  # #  #   #  #      #    #    #
                    #  # #  #  # #  ######     #    #    #
                    #    #  #    # #      #  #####   #### #
#---------------------------------------------------------------------------
# Original NNAIMQ code (V 1.0), 2021, University of Oviedo
# Author (s): M. Gallegos in collaboration with J.M. Guevara-Vela and
# A. M. Pendas.
#
# Version (1.1) 2023. Université de Rouen
# Autor             : VCastor.
############################################################################
#                             Hello World part                             #
print("")
print("Hello,\nI'm the version 1.1")
print("""
┌┐┌ ┌┐┌ ┌─┐ ┬ ┌┬┐ ┌─┐
│││ │││ ├─┤ │ │││ │ ┤┐
┘└┘ ┘└┘ ┴ ┴ ┴ ┴ ┴ └─┘└─
""")
############################################################################
#                          Libraries that we need                          #
libraries, tflibraries = [], []
libraries.append('import os')
libraries.append('import sys')
libraries.append('import pathlib')
libraries.append('import subprocess')
libraries.append('import numpy as np')
libraries.append('import pandas as pd')
libraries.append('import seaborn as sns')
libraries.append('import matplotlib.pyplot as plt')
libraries.append('from random import randint')
tflibraries.append('import tensorflow as tf')
tflibraries.append('from tensorflow import keras')
tflibraries.append('from tensorflow.keras import Sequential')
tflibraries.append('from tensorflow.keras.layers import Dense')
tflibraries.append('from tensorflow.keras.layers import Flatten')

#   Import libraries with te quiero demasiado
from tqdm import tqdm
for i in tqdm(range(len(libraries)), ncols=100, desc="Importing libraries   :: "):
    exec(libraries[i])

for i in tqdm(range(len(tflibraries)), ncols=100, desc="Importing Tensor Flow :: "):
    exec(tflibraries[i])

#   No warnings pirnted
os.environ['KMP_WARNINGS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

############################################################################
#                           Definimos lo definible                         #
def grepcut(re, file):
    """
    This function take a regular expresion and a file to obtein the command
    to find the line or lines where the regular expresion is in the file.
    $ grep -n "regular expresion" file.somewhere | cut -f1 -d:
    """
    cmdgrep = 'grep -n "' + re + '" ' + file
    cmdgrep = cmdgrep + ' | cut -f1 -d:'
    return cmdgrep

def adfsporadf(geomfile):
    """
    This function analize the ADF output to know if it is an output from a
    Single Point or a Geometry Optimization calculation.
    """
    cmdsp  = grepcut('SINGLE POINT CALCULATION', geomfile)
    cmdopt = grepcut('GEOMETRY OPTIMIZATION', geomfile)
    try:
        spline = int(os.popen(cmdsp).read())
    except:
        spline = 0
    try:
        optline = int(os.popen(cmdopt).read())
    except:
        optline = 0
    archivo   = open(geomfile, 'r', encoding="ISO-8859-1")
    datalines = archivo.readlines()
    #   How many atoms the systme has ?
    cmdnatoms = grepcut("Total System Charge", geomfile)
    if spline:
        atoline = int(os.popen(cmdnatoms).read()) - 3
    if optline:
        atoline = os.popen(cmdnatoms).read()
        atoline = atoline.split('\n')
        atoline = int(atoline[0]) - 3
    natoms = datalines[atoline]
    natoms = natoms.split()
    natoms = int(natoms[0])
    #   Start like a xyz file
    contents = str(natoms) + '\nADF output\n'
    #   Where are the coordinates ?
    if spline:
        cmd = grepcut("Geometry", geomfile)
        iline = int(os.popen(cmd).read()) + 4
    if optline:
        cmd = grepcut("Optimized geometry:", geomfile)
        iline = int(os.popen(cmd).read()) + 7
    #   All the atoms
    for i in range(iline, iline+natoms):
        linen = datalines[i]
        linen = linen.split()
        #   atom    x   y
        for j in range(1, 4):
            contents += str(linen[j]) + '  '
        #   z and skip to next line
        contents += str(linen[4])
        contents += '\n'
    archivo.close()
    #   Temporal file to write the coordinates
    tmpfile = geomfile.replace("out", "xyz")
    f = open(tmpfile, 'w')
    f.write(contents)
    f.close()
    return contents

def xyzoradf(geomfile):
    """
    This function will analise if the input is a ADF output or a xyz file. In
    case that it is a ADF output will call a function to anilise it.
    """
    archivo   = open(geomfile, 'r', encoding="ISO-8859-1")
    firstline = archivo.readline()
    try:
        natoms = int(firstline)
    except:
        natoms = 0
    if (natoms > 0):
        contents = archivo.read()
        xyzfiletmp = geomfile
        tmpf = False
    else:
        contents = adfsporadf(geomfile)
        xyzfiletmp = geomfile.replace("out", "xyz")
        tmpf = True
    archivo.close()
    #      contents of the coordinates in xyz format
    #      temporal file name
    #      Boolean the temporal file was written (?)
    return contents, xyzfiletmp, tmpf

def abba(agneta='=', bjorn='Trinidad', benny='*', frida=72):
    """
    This function just has some parameters to print
    """
    fb = "{:" + str(benny) + "^" + str(frida) + "}"
    a  = agneta*frida
    b  = fb.format(bjorn)
    print(a)
    print(b)
    print(a)

def norm(x,mean,std):
    y=np.empty_like(x)
    y[:]=x
    y=np.transpose(y)
    counter=0
    for i in y:
        y[counter,:]=(y[counter,:]-mean[counter])/(std[counter])
        counter=counter+1
    y=np.transpose(y)
    return y

############################################################################
#   The System to analise should be listed in a plain text file
list_geom = sys.argv[1]
tmpstr    = "Reading the geometry files from :: " + str(list_geom)
print("")
abba('=', tmpstr, '*', len(tmpstr))
tmpstr = ("The system(s) (is/are):")
print("")
abba('=', tmpstr, '*', len(tmpstr))
archivo = open(list_geom, 'r', encoding="ISO-8859-1")
systems = archivo.readlines()
for i in range(len(systems)):
    print(systems[i])
archivo.close()

############################################################################
#                        Numpy and Pandas options                          #
np.set_printoptions(threshold=sys.maxsize)
pd.set_option("display.max_rows", None, "display.max_columns", None)

############################################################################
#====             mean and std files will be loaded                    ====#

mean_stdv = ('mean_C', 'std_C', 'mean_H', 'std_H', 'mean_O', 'std_O', 
             'mean_N', 'std_N')
mean_stdf = ('"nnqC.mean"', '"nnqC.std"', '"nnqH.mean"', '"nnqH.std"',
             '"nnqO.mean"', '"nnqO.std"', '"nnqN.mean"', '"nnqN.std"')

for i in tqdm(range(len(mean_stdf)), ncols=99, desc="Statistics data :: "):
    exec("%s = np.loadtxt(%s, dtype='f')" % (mean_stdv[i], mean_stdf[i]))

print("Statistics data :: Loaded successfully ✅")
print("")

############################################################################
#====                 Neural Networks will be loaded                   ====#

model = ("model_C", "model_H", "model_O", "model_N")
nnq   = ("'nnqC.h5'", "'nnqH.h5'", "'nnqO.h5'", "'nnqN.h5'")
model_C = tf.keras.models.load_model('nnqC.h5')

for i in tqdm(range(len(model)), ncols=99, desc="Neural Networks :: "):
    exec("%s = tf.keras.models.load_model(%s)" % (model[i], nnq[i]))

print("Neural Networks :: Loaded successfully ✅")
print("")

############################################################################
col_c = 129
col_h = 132
col_o = 111
col_n = 112
colname_c=['AtomNum']
colname_h=['AtomNum']
colname_o=['AtomNum']
colname_n=['AtomNum']
for i in range(1,col_c+1):
    colname_c.append('g' + str(i))
for i in range(1,col_h+1):
    colname_h.append('g' + str(i))
for i in range(1,col_o+1):
    colname_o.append('g' + str(i))
for i in range(1,col_n+1):
    colname_n.append('g' + str(i))
column_names_c=colname_c
column_names_h=colname_h
column_names_o=colname_o
column_names_n=colname_n
############################################################################
#                 Start the loop for all system to analise                 #
with open(list_geom) as f34:
    for geomline in f34:
        geom = geomline.rstrip('\n') 
        geom = geom.replace(' ', '')
        tmpname = "Computing the ACSF descriptor for file" + str(geom)
        abba('=', tmpname, '*', len(tmpname))
        contents, xyzf, tmpfbool = xyzoradf(geom)
        
        size=len(geom)
        nombre=geom[:size-4]
        #   Be careful with the executable
        subprocess.check_call([r"./SSFC_arm.exe", xyzf, nombre])
        
        acsf_list=[]
        acsf_list.append(nombre + ".acsf")
        acsf_list.append(nombre + "_C.acsf")
        acsf_list.append(nombre + "_H.acsf")
        acsf_list.append(nombre + "_O.acsf")
        acsf_list.append(nombre + "_N.acsf")
        for i in acsf_list:
            with open(i,'r+') as fopen:
                string = ""
                for line in fopen.readlines():
                    string = string + line[:-2] + "\n"
            
            with open(i,'w') as fopen:
                fopen.write(string)
        ######################################################
        # C ATOMS
        ######################################################
        print("Starting prediction of C atoms")
        if (os.stat(acsf_list[1]).st_size != 0) :
           raw_C = pd.read_csv(acsf_list[1],names=column_names_c,na_values="?",
                                     comment='\t',sep=",",skipinitialspace=True)
           dataset_C = raw_C.copy()
           dataset_C = dataset_C.dropna()
           data_C=dataset_C
           data_C_stats=data_C.describe()
           data_C_stats.pop("AtomNum")
           data_C_stats=data_C_stats.transpose()
           data_C_labels=data_C.pop('AtomNum')
           normed_C=norm(data_C,mean_C,std_C)
           C_predictions=model_C.predict(normed_C).flatten()
        ######################################################
        # H ATOMS
        ######################################################
        print("Starting prediction of H atoms")
        if (os.stat(acsf_list[2]).st_size != 0) :
           raw_H = pd.read_csv(acsf_list[2],names=column_names_h,na_values="?",
                                     comment='\t',sep=",",skipinitialspace=True)
           dataset_H = raw_H.copy()
           dataset_H = dataset_H.dropna()
           data_H=dataset_H
           data_H_stats=data_H.describe()
           data_H_stats.pop("AtomNum")
           data_H_stats=data_H_stats.transpose()
           data_H_labels=data_H.pop('AtomNum')
           normed_H=norm(data_H,mean_H,std_H)
           H_predictions=model_H.predict(normed_H).flatten()
        ######################################################
        # O ATOMS
        ######################################################
        print("Starting prediction of O atoms")
        if (os.stat(acsf_list[3]).st_size != 0) :
           raw_O = pd.read_csv(acsf_list[3],names=column_names_o,na_values="?",
                                     comment='\t',sep=",",skipinitialspace=True)
           dataset_O = raw_O.copy()
           dataset_O = dataset_O.dropna()
           data_O=dataset_O
           data_O_stats=data_O.describe()
           data_O_stats.pop("AtomNum")
           data_O_stats=data_O_stats.transpose()
           data_O_labels=data_O.pop('AtomNum')
           normed_O=norm(data_O,mean_O,std_O)
           O_predictions=model_O.predict(normed_O).flatten()
        ######################################################
        # N ATOMS
        ######################################################
        print("Starting prediction of N atoms")
        if (os.stat(acsf_list[4]).st_size != 0) :
           raw_N = pd.read_csv(acsf_list[4],names=column_names_n,na_values="?",
                                     comment='\t',sep=",",skipinitialspace=True)
           dataset_N = raw_N.copy()
           dataset_N = dataset_N.dropna()
           data_N=dataset_N
           data_N_stats=data_N.describe()
           data_N_stats.pop("AtomNum")
           data_N_stats=data_N_stats.transpose()
           data_N_labels=data_N.pop('AtomNum')
           normed_N=norm(data_N,mean_N,std_N)
           N_predictions=model_N.predict(normed_N).flatten()
        ########################################################
        # MOLECULAR CHARGE
        ########################################################
        molec_charge=0.0
        if (os.stat(acsf_list[1]).st_size != 0) :
         for i in C_predictions:
            molec_charge=molec_charge+i
        if (os.stat(acsf_list[2]).st_size != 0) :
         for i in H_predictions:
            molec_charge=molec_charge+i
        if (os.stat(acsf_list[3]).st_size != 0) :
         for i in O_predictions:
            molec_charge=molec_charge+i
        if (os.stat(acsf_list[4]).st_size != 0) :
         for i in N_predictions:
            molec_charge=molec_charge+i
        print("Total Molecular Charge", molec_charge)
        #########################################################
        # OUTPUT FILES
        #########################################################
        cargas_output=nombre+".charge"
        with open(xyzf) as f:
             lineas = f.readlines()[2:]
        etiqueta=[]
        for line in lineas:
            valores=line.split()
            etiqueta.append(valores[0])
        vector=[]
        contador=0
        contador_c=0
        contador_h=0
        contador_o=0
        contador_n=0
        for i in etiqueta:
            if (i == "C"):
              vector.append(C_predictions[contador_c])
              contador_c+=1
            elif (i=="H"):
              vector.append(H_predictions[contador_h])
              contador_h+=1
            elif (i=="O"):
              vector.append(O_predictions[contador_o])
              contador_o+=1
            elif (i=="N"):
              vector.append(N_predictions[contador_n])
              contador_n+=1
            contador+=1
        contador=0
        vector=np.array(vector)
        contador=0
        num=1
        with open(cargas_output, 'w') as fout:
             fout.write(" Atom Number " + "  Atom Label  " + "   Charge   " + "\n")
             for i in etiqueta:
                fout.write('{:^13}'.format(str(num)) + '{:^14}'.format(str(i))
                               + f'{vector[contador]:+.6f}' + "\n")
                contador+=1
                num+=1

############################################################################
#             Clean the acsf files and if we use a temporal file           #
for i in range(len(acsf_list)):
    os.remove(acsf_list[i])
if tmpfbool:
    os.remove(xyzf)
