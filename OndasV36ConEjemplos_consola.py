from __future__ import division  #Para que las divisiones den bien!
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 01:21:15 2014

@author: Ionatan@gmail.com
"""



"""

Notas Generales sobre el programa:

    Este programa fue desarrollado en el marco de la materia F2Quimicos para mostrar ejemplos de polarizacion
    
    El programa permite definir objetos (polarizadores y medios) y las ondas que se desan graficar.
    
    Cosas pendientes:
        - Que cuando se marca LaminaOnda al crear una lamina calcule automaticamente la longitud que debe tener en terminos de una lamina de onda completa (a medio hacer!)
        - Que dentro de un medio muestre cada componente de la onda en el eje rapido y el lento, o en el x e y. Hay que implementar alguna manra de mostra tramos generados in situ
        - Que se pueda colocar marcas espaciales donde muestre el estado de la onda para todo tiempo (como hace en el extremo del eje)
        - Mejorar la creacion de las ondas circulares para que puedan ser elipticas (revisar cuentas de como habria que hacerlo!) 
        - Incluir la opcion de no mostrar ciertos tramos de ciertas ondas
        - Habilitar la opcion de que las ondas empiecen y terminen. 
        

"""


"""

    Nota!! Hay un error,
    
        Parametros['VistaFrente']=True
        CrearOnda(Tipo='Circular+')
        CrearObjeto('Polarizador',15,Angulo=np.pi/3) Da mal! Algo no esta bien en alguna cuenta.
"""

import numpy as np
import scipy.constants as pc
import cmath

from fractions import gcd #Lo usa para encontrar maximo comun divisor en el calculo de las laminas
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation
from sys import argv

script, ej_consola = argv
ej_consola = int(ej_consola)



# Define parametros
Parametros = {}

# Parametros primarios
Parametros['ZInicial']=0
Parametros['ZFinal']=30
Parametros['Densidad']=100 #Numeros de puntos por unidad en z
Parametros['NumerodeOndas']=5 #Numero de ondas que deberia entrar si n=1
Parametros['CorrerTramos']=0.1 #Cuanto debe correr los tramos cuando crea objetos nuevos
Parametros['VistaFrente']=False #Determina como se ven los graficos, con True se puede ver de frente para rotar en X e Y, con false se rota entre X y Z, mejor para hacer una vista lateral

#Parametros secundarios (que se deducen de los primarios)
Parametros['LongitudDeOnda']=(Parametros['ZFinal']-Parametros['ZInicial'])/Parametros['NumerodeOndas']
Parametros['Frecuencia']=pc.c/Parametros['LongitudDeOnda']
Parametros['TamanoEjeX']=1
Parametros['TamanoEjeY']=1




#
# Define objetos no animados
#
Lineasfijas=[]

def CrearLineaFija(Extremo1, Extremo2, Color):
    PuntosX=np.linspace(Extremo1[0],Extremo2[0],2)
    PuntosY=np.linspace(Extremo1[1],Extremo2[1],2)
    PuntosZ=np.linspace(Extremo1[2],Extremo2[2],2)
    LineaNueva=[np.asarray([PuntosX, PuntosY, PuntosZ]).T,Color]
    Lineasfijas.append(LineaNueva)


def CrearLineasPolarizador(Posicion,Angulo,Borde=True,Color='black'):
    if Borde:
        CrearLineaFija([Parametros['TamanoEjeX'],Parametros['TamanoEjeY'],Posicion],[Parametros['TamanoEjeX'],-Parametros['TamanoEjeY'],Posicion],Color)
        CrearLineaFija([Parametros['TamanoEjeX'],-Parametros['TamanoEjeY'],Posicion],[-Parametros['TamanoEjeX'],-Parametros['TamanoEjeY'],Posicion],Color)
        CrearLineaFija([-Parametros['TamanoEjeX'],-Parametros['TamanoEjeY'],Posicion],[-Parametros['TamanoEjeX'],Parametros['TamanoEjeY'],Posicion],Color)
        CrearLineaFija([-Parametros['TamanoEjeX'],Parametros['TamanoEjeY'],Posicion],[Parametros['TamanoEjeX'],Parametros['TamanoEjeY'],Posicion],Color)
    Largo=min([Parametros['TamanoEjeX'], Parametros['TamanoEjeY']])
    Largo=0.7*Largo
    CrearLineaFija([Largo*np.cos(Angulo),Largo*np.sin(Angulo),Posicion],[-Largo*np.cos(Angulo),-Largo*np.sin(Angulo),Posicion],Color)

def CrearLineasMedio(PosicionInicial,PosicionFinal,Angulo,Borde,Color='y'):
    if Borde:     
        #Caja inicial        
        CrearLineaFija([Parametros['TamanoEjeX'],Parametros['TamanoEjeY'],PosicionInicial],[Parametros['TamanoEjeX'],-Parametros['TamanoEjeY'],PosicionInicial],Color)
        CrearLineaFija([Parametros['TamanoEjeX'],-Parametros['TamanoEjeY'],PosicionInicial],[-Parametros['TamanoEjeX'],-Parametros['TamanoEjeY'],PosicionInicial],Color)
        CrearLineaFija([-Parametros['TamanoEjeX'],-Parametros['TamanoEjeY'],PosicionInicial],[-Parametros['TamanoEjeX'],Parametros['TamanoEjeY'],PosicionInicial],Color)
        CrearLineaFija([-Parametros['TamanoEjeX'],Parametros['TamanoEjeY'],PosicionInicial],[Parametros['TamanoEjeX'],Parametros['TamanoEjeY'],PosicionInicial],Color)
        #Caja final        
        CrearLineaFija([Parametros['TamanoEjeX'],Parametros['TamanoEjeY'],PosicionFinal],[Parametros['TamanoEjeX'],-Parametros['TamanoEjeY'],PosicionFinal],Color)
        CrearLineaFija([Parametros['TamanoEjeX'],-Parametros['TamanoEjeY'],PosicionFinal],[-Parametros['TamanoEjeX'],-Parametros['TamanoEjeY'],PosicionFinal],Color)
        CrearLineaFija([-Parametros['TamanoEjeX'],-Parametros['TamanoEjeY'],PosicionFinal],[-Parametros['TamanoEjeX'],Parametros['TamanoEjeY'],PosicionFinal],Color)
        CrearLineaFija([-Parametros['TamanoEjeX'],Parametros['TamanoEjeY'],PosicionFinal],[Parametros['TamanoEjeX'],Parametros['TamanoEjeY'],PosicionFinal],Color)
        #Bordes longitudinales
        CrearLineaFija([Parametros['TamanoEjeX'],Parametros['TamanoEjeY'],PosicionInicial],[Parametros['TamanoEjeX'],Parametros['TamanoEjeY'],PosicionFinal],Color)
        CrearLineaFija([Parametros['TamanoEjeX'],-Parametros['TamanoEjeY'],PosicionInicial],[Parametros['TamanoEjeX'],-Parametros['TamanoEjeY'],PosicionFinal],Color)
        CrearLineaFija([-Parametros['TamanoEjeX'],-Parametros['TamanoEjeY'],PosicionInicial],[-Parametros['TamanoEjeX'],-Parametros['TamanoEjeY'],PosicionFinal],Color)
        CrearLineaFija([-Parametros['TamanoEjeX'],Parametros['TamanoEjeY'],PosicionInicial],[-Parametros['TamanoEjeX'],Parametros['TamanoEjeY'],PosicionFinal],Color)
    # Crea dibujo ejes
    Largo=min([Parametros['TamanoEjeX'], Parametros['TamanoEjeY']])
    Largo=0.3*Largo
    CrearLineaFija([Largo*np.cos(Angulo),Largo*np.sin(Angulo),(PosicionFinal+PosicionInicial)//2],[-Largo*np.cos(Angulo),-Largo*np.sin(Angulo),(PosicionFinal+PosicionInicial)//2],Color)
    Largo=0.5*Largo
    CrearLineaFija([Largo*np.cos(Angulo+np.pi/2),Largo*np.sin(Angulo+np.pi/2),(PosicionFinal+PosicionInicial)//2],[-Largo*np.cos(Angulo+np.pi/2),-Largo*np.sin(Angulo+np.pi/2),(PosicionFinal+PosicionInicial)//2],Color)

#
# Define tramos
# Lo elementos de tramos deben tener la estructura: Xinicial, Xfinal, Indicex, Indicey, AnguloIndice, Tipo, AnguloObjeto
#

#Crea la lista vacia
Tramos=[]
Tramo={'Empieza':Parametros['ZInicial'], 'Termina':Parametros['ZFinal'],'Indices':[1,1,0],'Angulo':0,'Nombre':'Zona sin medio','Polarizador':False,'Lamina':False}
Tramos.append(Tramo)

def CrearObjeto (Tipo,Posicion=Parametros['ZFinal']/2,Angulo=0,Largo=0,IndiceX=1,IndiceY=1,Nombre='Predeterminado',Color='black',Borde=True,Mostrar=True,LaminaOndas=False,Frecuencia=Parametros['Frecuencia']):
    if Nombre=='Predeterminado': Nombre=Tipo
    if Tipo=='Polarizador': 
        Polarizador=True
    else:    
        Polarizador=False
    if Tipo=='Lamina': 
        Lamina=True
    else:    
        Lamina=False
    
    if LaminaOndas: #Considera el largo como la cantidad de ondas que debe desfazarse
        #
        # Partimos de que n*Lambda1=Lambda2=L. Pero Lambda1=Lambda0/n1 y Lambda2=Lambda0/n2
        # Se puede llegar que: n2*n=n1*m=L*n1*n2/Lambda0
        # Hay que eliminar el maximo comun divisor.y queda que n1'*n2' es solucion
        # Despejando queda que: L=Lambda0/mcd(n1,n2)
        Factor=1
        if IndiceX % 1 == 0:
            n1=IndiceX
        else: #Redondea el indice a dos decimales para poder trabajr con enteros
            n1=round(IndiceX,2)
            n1=n1*100
            n1=int(n1)
            Factor=Factor*100
        if IndiceY % 1 == 0:
            n2=IndiceY
        else: #Redondea el indice a dos decimales para poder trabajr con enteros
            n2=round(IndiceY,2)
            n2=n2*100
            n2=int(n2)#Para asegurar que no haya error de numero de maquina
            Factor=Factor*100            
        MCD=gcd(n1,n2)
        #Calcula el Lambda0
        Lambda0=pc.c/Frecuencia
        Largo=Lambda0/(MCD*Factor)*Largo
            
    #ACA hay que hacer que si bandera = Ondas, recalcule el largo como la cantidad necesaria segun de cuanas ondas sea la lamian
       
    #Revisa todos los tramos para saber donde agregar el que corresponde. Cuando agrega un tramo corta el que ya esta y agrega el nuevo segun corresponda
    for n in range(len(Tramos)):
        Tramosprevios=Tramos[n]
        if Polarizador:
            if Tramosprevios['Termina']==Posicion:
                if Tramosprevios['Polarizador']: #Se fija si ya hay un polarizador
                    print ('Esta intentando introducir '+Nombre+' donde ya hay un polarizador')
                else:
                    Tramosprevios['Angulo']=Angulo
                    Tramosprevios['Polarizador']=True
                    if Mostrar: CrearLineasPolarizador(Posicion,Angulo,Borde,Color)
                return
            if Tramosprevios['Empieza']<Posicion and Posicion<Tramosprevios['Termina']: # Encuentra el tramo en el q debe agregar el polarizador
                Tramo=Tramosprevios.copy() #Carga los datos del tramo previo para armar la segunda mitad
                Tramosprevios['Termina']=Posicion #Corta el tramo previo hasta la posicion actual
                Tramosprevios['Polarizador']=True #Sobreescribe como termina el tramo
                Tramosprevios['Angulo']=Angulo
                Tramo['Empieza']=Posicion #Corrige la posicion inicial del tramo siguiente que va a crear
                Tramos.append(Tramo)
                if Mostrar: CrearLineasPolarizador(Posicion,Angulo,Borde,Color)
                return
        if Lamina:
            if Tramosprevios['Empieza']<=Posicion and Posicion<Tramosprevios['Termina']: # Encuentra el tramo en el q debe agregar la lamina
                if Tramosprevios['Termina']<Posicion+Largo:
                    print ('Error: Esta intentando colocar '+Nombre+' por sobre varios tramos ya definidos. Si desea colocar un polarizador dentro de un medio, primero cree el medio y luego el polarizador')
                    return
                else: #En este caso se crea el nuevo tramo y los necesarios en el interior del ya existente
                    #Avisa si esta sobreescribiendo otro medio
                    if not Tramosprevios['Indices'][0]==1 or not Tramosprevios['Indices'][1]==1:
                        print ('Precaucion: Esta colocando '+Nombre+' dentro una zona que ya tiene un medio, este medio sobreescribira al anterior')
                    
                    if Tramosprevios['Empieza']==Posicion: # Considera el caso de que empiece donde empezaba el tramo previo
                        #Se fija si simplemente no reemplaza a otro medio
                        #Si habia un polarizador queda
                        if Tramosprevios['Termina']==Posicion+Largo: #En este caso el tramo nuevo reemplaza al anterior perfectamente y simplemente hay que completar la info dle medio
                            Tramosprevios['Indices']=[IndiceX,IndiceY,Angulo]
                            Tramosprevios['Nombre']=Nombre
                            Tramosprevios['Lamina']=True
                        else: #En este caso debe crar un tramo posterior identico al inicial, y agrega el inicial
                            # Agrega el de la lamina
                            Tramo={'Empieza':Posicion,'Termina':Posicion+Largo,'Indices':[IndiceX,IndiceY,Angulo],'Angulo':0,'Nombre':Nombre,'Polarizador':False,'Lamina':True}
                            Tramos.append(Tramo)                                                        
                            Tramosprevios['Empieza']=Posicion+Largo
                    else: #En este caso queda un tramo previo a la lamina, pero puede haber uno posterior o no.
                        if Tramosprevios['Termina']==Posicion+Largo: #En este caso la lamina termina en donde terminaba el tramo anterior
                            #Corta el tramo existente para que cubra la primer parte
                            Tramosprevios['Termina']=Posicion
                            Tramo=Tramosprevios.copy()# Muda la info de la polariacion
                            Tramosprevios['Polarizador']=False
                            Tramosprevios['Angulo']=0
                                                        
                            Tramo['Empieza']=Posicion
                            Tramo['Termina']=Posicion+Largo
                            Tramo['Indices']=[IndiceX,IndiceY,Angulo]
                            Tramo['Lamina']=True
                            Tramo['Nombre']=Nombre
                            Tramos.append(Tramo) #Agrega el tramo de la lamina
                        else: #En este caso debe crar un tramo posterior identico al inicial, y agrega el inicial
                            #Crea el inicial
                            Tramo=Tramosprevios.copy()
                            Tramo['Termina']=Posicion
                            Tramo['Polarizador']=False
                            Tramo['Angulo']=0
                            Tramos.append(Tramo) #Agrego el tramo inicial de los tres
                            #Crea el tramo de la lamina nueva
                            Tramo={'Empieza':Posicion,'Termina':Posicion+Largo,'Indices':[IndiceX,IndiceY,Angulo],'Angulo':0,'Polarizador':False,'Lamina':True,'Nombre':Nombre}
                            Tramos.append(Tramo) #Agrega el tramo de la lamina
                            #Modifica el tramo original para que ocupe el tercer segmento
                            Tramosprevios['Empieza']=Posicion+Largo
                            
                if Mostrar: CrearLineasMedio(Posicion,Posicion+Largo,Angulo,Borde,Color)
                return
    print ('Parece ser que coloco el objeto fuera del rango de valores en el eje Z incluidos en el programa')
    
def getKey(item):
    return item['Empieza']

#    
# Define funciones utiles para el calculo de las ondas, pero que no necesitan ser parte del objeto onda
#
def CalculoTramoEje (A=1,Phase=0,n=1,Frecuencia=Parametros['Frecuencia'],Interlineado=np.linspace(0,10,100),t=0):
    #Prepara los datos        
    c=pc.c
    w=2*np.pi*Frecuencia
    Lambda=1/Frecuencia*c
    k=n*2*np.pi/Lambda
    # Hace el calculo        
    Funcion= A*np.sin(k*Interlineado-w*t+Phase)
    return Funcion

def CalculoFase (Phase=0,n=1,Frecuencia=Parametros['Frecuencia'],Interlineado=np.linspace(0,10,100),t=0):
    #Prepara los datos        
    c=pc.c
    w=2*np.pi*Frecuencia
    Lambda=1/Frecuencia*c
    k=n*2*np.pi/Lambda
    # Hace el calculo        
    Fase= k*(Interlineado[-1])+Phase
    return Fase


def CalculoTramo(Ax=1,Ay=0,Phasex=0,Phasey=0,Tramo={'Empieza':Parametros['ZInicial'], 'Termina':Parametros['ZFinal'],'IndiceX':1,'IndiceY':1,'AnguloIndice':0,'Tipo':'Nada','Angulo':0},Frecuencia=Parametros['Frecuencia'],t=0):
    ZInicial=Tramo['Empieza']
    ZFinal=Tramo['Termina']
    NumeroDePuntos=int(Parametros['Densidad']*(ZFinal-ZInicial))
    Interlineado=np.linspace(0,ZFinal-ZInicial,NumeroDePuntos)
    nx=Tramo['Indices'][0]
    ny=Tramo['Indices'][1]

    if Tramo['Lamina']:
        #En cada eje x e y llega una Amplitud y una fase. Esa amplitud en los versores l y r tiene dos componentes, cada uno con diferente n, que a su vez tienen dos componentes en los x e y del programa
        #Por cade eje hace falta una fase comun a 4 ondas, de a pares x e y comparten el n. 
        #En total hay 8 ondas, 4 por eje, agrupadas de a dos segun fase inicial o n. 
        
        # Reescribo la notacion de los n en rapido y lento
        nl=nx
        nr=ny
        
        #Por alguna razon los vecotres salen de la rotacion como listas de listas! Revisar. 
        AxRotado=Rotacion(Tramo['Indices'][2],[Ax,0])        
        Axl=AxRotado[0][0]
        Axr=AxRotado[1][0]
        AxlAntirotado=Rotacion(-Tramo['Indices'][2],[Axl,0])
        AxrAntirotado=Rotacion(-Tramo['Indices'][2],[0,Axr])
        Axlx=AxlAntirotado[0][0]
        Axly=AxlAntirotado[1][0]
        Axrx=AxrAntirotado[0][0]
        Axry=AxrAntirotado[1][0]
        
        AyRotado=Rotacion(Tramo['Indices'][2],[0,Ay])        
        Ayl=AyRotado[0][0]
        Ayr=AyRotado[1][0]
        AylAntirotado=Rotacion(-Tramo['Indices'][2],[Ayl,0])
        AyrAntirotado=Rotacion(-Tramo['Indices'][2],[0,Ayr])
        Aylx=AylAntirotado[0][0]
        Ayly=AylAntirotado[1][0]
        Ayrx=AyrAntirotado[0][0]
        Ayry=AyrAntirotado[1][0]

        #El primer indice indica la phase inicial a usar, el segundo el n a usar, y el tercero el eje a usar.

        Fxlx=CalculoTramoEje(Axlx,Phasex,nl,Frecuencia,Interlineado,t)
        Fxly=CalculoTramoEje(Axly,Phasex,nl,Frecuencia,Interlineado,t)
        Fxrx=CalculoTramoEje(Axrx,Phasex,nr,Frecuencia,Interlineado,t)
        Fxry=CalculoTramoEje(Axry,Phasex,nr,Frecuencia,Interlineado,t)

        Fylx=CalculoTramoEje(Aylx,Phasey,nl,Frecuencia,Interlineado,t)
        Fyly=CalculoTramoEje(Ayly,Phasey,nl,Frecuencia,Interlineado,t)
        Fyrx=CalculoTramoEje(Ayrx,Phasey,nr,Frecuencia,Interlineado,t)
        Fyry=CalculoTramoEje(Ayry,Phasey,nr,Frecuencia,Interlineado,t)

        Fx=Fxlx+Fxrx+Fylx+Fyrx
        Fy=Fxly+Fxry+Fyly+Fyry
        
        FuncionTramo=np.asarray([Fx,Fy,Interlineado+ZInicial])
        
        Pxl=CalculoFase (Phasex,nl,Frecuencia,Interlineado,t)
        Pxr=CalculoFase (Phasex,nr,Frecuencia,Interlineado,t)
        
        Pyl=CalculoFase (Phasey,nl,Frecuencia,Interlineado,t)
        Pyr=CalculoFase (Phasey,nr,Frecuencia,Interlineado,t)
        

        #Los pasa a notacion compleja
        Cxlx=cmath.rect(Axlx, Pxl)
        Cxly=cmath.rect(Axly, Pxl)
        Cxrx=cmath.rect(Axrx, Pxr)
        Cxry=cmath.rect(Axry, Pxr)

        Cylx=cmath.rect(Aylx, Pyl)
        Cyly=cmath.rect(Ayly, Pyl)
        Cyrx=cmath.rect(Ayrx, Pyr)
        Cyry=cmath.rect(Ayry, Pyr)
        
        Ax=Cxlx+Cxrx+Cylx+Cyrx
        Ay=Cxly+Cxry+Cyly+Cyry
        
        Ax,Phasex=cmath.polar(Ax)
        Ay,Phasey=cmath.polar(Ay)
        
    else:
        FuncionX=CalculoTramoEje(Ax,Phasex,nx,Frecuencia,Interlineado,t)
        FuncionY=CalculoTramoEje(Ay,Phasey,ny,Frecuencia,Interlineado,t)
        FuncionTramo=np.asarray([FuncionX,FuncionY,Interlineado+ZInicial])
        Phasex=CalculoFase (Phasex,nx,Frecuencia,Interlineado,t)
        Phasey=CalculoFase (Phasey,ny,Frecuencia,Interlineado,t)

        
        
    
    # Procesa las amplitudes y las fases
    if Tramo['Polarizador']:
        VectorEntrada=[Ax,Ay]
        VectorRotado=Rotacion(Tramo['Angulo'],VectorEntrada)
        VectorDespues=np.matrix([[1,0],[0,0]])*VectorRotado
        VectorDespues=VectorDespues.ravel().tolist()
        VectorDespues=[VectorDespues[0][0],VectorDespues[0][1]]
        VectorDespuesAntirotado=Rotacion(-Tramo['Angulo'],VectorDespues)        
        Ax=VectorDespuesAntirotado[0][0]
        Ay=VectorDespuesAntirotado[1][0]
        
    return FuncionTramo, Ax, Ay, Phasex, Phasey

def Rotacion(Angulo=0,Vector=[0,0]): #Escribe las componentes que entran en un eje horizonatl vertial, en terminos de un eje rotado el angulo
    Vector=np.matrix(Vector).T
    MatrizRotacion=np.matrix([[np.cos(Angulo),np.sin(Angulo)],[-np.sin(Angulo),np.cos(Angulo)]])
    VectorResultante=MatrizRotacion*Vector    
    return VectorResultante.tolist()
    
    
#
# Define el objeto onda
#
class Onda:

    def __init__ (self,Amplitud=1,Angulo=0,Phase=0,Tipo='Lineal',Frecuencia=Parametros['Frecuencia'],Color='b',Resultante=False,Fuentes=[],Mostrar=True,ZInicial=Parametros['ZInicial'],ZFinal=Parametros['ZFinal'],Nombre='SinNombre',e=1):
        self.Nombre=Nombre
        self.Amplitud=Amplitud
        self.Angulo=Angulo
        self.Phase=Phase
        self.Tipo=Tipo
        self.Frecuencia=Frecuencia
        self.Color=Color
        self.Resultante=Resultante
        #
        # Reconoce las fuentes por el nombre o por el numero
        #
        self.Fuentes=[]
        for Dato in Fuentes:
            if isinstance( Dato, str ):
                for BuscarCadaOnda in Ondas:
                    if BuscarCadaOnda.Nombre==Dato:
                        self.Fuentes.append(BuscarCadaOnda)
            else:
                if isinstance( Dato, int ):
                    self.Fuentes.append(Ondas[Dato])
                else:
                    print ('No se reconocio '+str(Dato)+' como una fuente valida')
        self.Mostrar=Mostrar
        self.Excentricidad=e
        
    def __str__ (self):
        s = 'La Onda: '  + self.Nombre
        s += ' tiene amplitud ' + str(self.Amplitud)
        return s
        
    def CalculoFuncionCompleta(self,t=0):
        if not self.Resultante: 
            FuncionCompleta=[]
            if self.Tipo=='Lineal':
                Ax=self.Amplitud*np.cos(self.Angulo)
                Ay=self.Amplitud*np.sin(self.Angulo)
            else:
                #Revisar!
                Ax=self.Amplitud*np.cos(self.Angulo)+self.Amplitud*np.sin(self.Angulo)*self.Excentricidad
                Ay=self.Amplitud*np.sin(self.Angulo)+self.Amplitud*np.cos(self.Angulo)*self.Excentricidad
                Ax=Ax*(1/(1+self.Excentricidad)) #Renormaliza
                Ay=Ay*(1/(1+self.Excentricidad))
            if self.Tipo=='Lineal':
                Phasex=self.Phase
                Phasey=self.Phase
            if self.Tipo=='Circular+':
                Phasex=self.Phase
                Phasey=self.Phase+np.pi/2
            if self.Tipo=='Circular-':
                Phasex=self.Phase
                Phasey=self.Phase-np.pi/2
            Frecuencia=self.Frecuencia
            for Tramo in Tramos:
                TramoNuevo, Ax, Ay, Phasex, Phasey = CalculoTramo(Ax,Ay,Phasex,Phasey,Tramo,Frecuencia,t)
                FuncionCompleta.extend(TramoNuevo.T)
            self.UltimaFuncion=np.asarray(FuncionCompleta)
        if self.Resultante:
            FuncionCompletaParcial=[]
            for CadaFuente in self.Fuentes:
                OndaParcial=np.asarray(CadaFuente.CalculoFuncionCompleta(t))
                if FuncionCompletaParcial==[]:
                    FuncionCompletaParcial=OndaParcial
                else:
                    FuncionCompletaParcial=FuncionCompletaParcial+OndaParcial
            FuncionCompleta=FuncionCompletaParcial
            FuncionCompleta[:,2]=FuncionCompleta[:,2]/len(self.Fuentes)
        return FuncionCompleta




Ondas=[]

def CrearOnda(Amplitud=1,Angulo=0,Phase=0,Tipo='Lineal',Frecuencia=Parametros['Frecuencia'],Color='b',Resultante=False,Fuentes=[],Mostrar=True,ZInicial=Parametros['ZInicial'],ZFinal=Parametros['ZFinal'],Nombre='SinNombre'):
        OndaNueva=Onda(Amplitud,Angulo,Phase,Tipo,Frecuencia,Color,Resultante,Fuentes,Mostrar,ZInicial,ZFinal,Nombre)
        Ondas.append(OndaNueva)






def Ejemplo(n):
    
    #
    # Ejemplos de combinacion de ondas en ejes X e Y
    #
	
    # Con dos ondas en fase en X e Y creamos una circular
    if n==100:
        CrearOnda(Nombre='OndaX',Mostrar=True)
        CrearOnda(Angulo=np.pi/2,Color='r',Nombre='OndaY',Mostrar=True)
        CrearOnda(Resultante=True,Fuentes=['OndaX','OndaY'],Color='y')
    
    # Hacemos pasar las dos componentes por una lamina para mostrar que cambia la longitus de onda segun el n del medio
    if n==101:
        CrearOnda(Nombre='OndaX',Mostrar=True)
        CrearOnda(Angulo=np.pi/2,Color='r',Nombre='OndaY',Mostrar=True)
        CrearObjeto (Tipo='Lamina',Posicion=10,Largo=7.5,IndiceY=2)
        
    # Mostramos que la resultante pasa de ser lineal a ser circular
    if n==102:
        CrearOnda(Nombre='OndaX',Mostrar=False)
        CrearOnda(Angulo=np.pi/2,Color='r',Nombre='OndaY',Mostrar=False)
        CrearOnda(Resultante=True,Fuentes=['OndaX','OndaY'],Color='y')
        CrearObjeto (Tipo='Lamina',Posicion=10,Largo=7.5,IndiceY=2)
    
    # Si se desfaza una cantidad semientera de onda se invierte la orientacion
    if n==103:
        CrearOnda(Nombre='OndaX',Mostrar=False)
        CrearOnda(Angulo=np.pi/2,Color='r',Nombre='OndaY',Mostrar=False)
        CrearOnda(Resultante=True,Fuentes=['OndaX','OndaY'],Color='y')
        CrearObjeto (Tipo='Lamina',Posicion=10,Largo=9,IndiceY=2)

    # Si se desfaza una cantidad entera de onda no cambia nada
    if n==104:
        CrearOnda(Nombre='OndaX',Mostrar=False)
        CrearOnda(Angulo=np.pi/2,Color='r',Nombre='OndaY',Mostrar=False)
        CrearOnda(Resultante=True,Fuentes=['OndaX','OndaY'],Color='y')
        CrearObjeto (Tipo='Lamina',Posicion=10,Largo=6,IndiceY=2)

    # Porque podemos ver que en el espacio que una componente cumple un periodo la otra hace dos
    if n==105:
        CrearOnda(Nombre='OndaX',Mostrar=True)
        CrearOnda(Angulo=np.pi/2,Color='r',Nombre='OndaY',Mostrar=True)
        CrearOnda(Resultante=True,Fuentes=['OndaX','OndaY'],Color='y',Mostrar=False)
        CrearObjeto (Tipo='Lamina',Posicion=10,Largo=6,IndiceY=2)

        
    if n==0:
        CrearOnda(Nombre='OndaX',Mostrar=False)
        CrearOnda(Angulo=np.pi/2,Color='r',Nombre='OndaY',Mostrar=False)
        CrearOnda(Resultante=True,Fuentes=['OndaX','OndaY'],Color='y')
        CrearObjeto (Tipo='Lamina',Posicion=10,Largo=9,IndiceY=2)
    if n==1:
        CrearOnda()
    if n==2:
        CrearOnda(Angulo=np.pi/2,Color='r')
    if n==3:
        CrearOnda()
        CrearOnda(Angulo=np.pi/2,Color='r')
    if n==4:
        CrearOnda(Angulo=np.pi/4,Color='green')
    if n==5:
        CrearOnda(Nombre='OndaX')
        CrearOnda(Angulo=np.pi/2,Color='r',Nombre='OndaY')
        CrearOnda(Resultante=True,Fuentes=['OndaX','OndaY'],Color='y')
    if n==6:
        CrearOnda(Nombre='OndaX')
        CrearOnda(Angulo=np.pi/3,Color='r',Nombre='OndaY')
        CrearOnda(Resultante=True,Fuentes=['OndaX','OndaY'],Color='y')
    if n==7:
        CrearOnda(Nombre='OndaX',Amplitud=0.5)
        CrearOnda(Angulo=np.pi/3,Color='r',Nombre='OndaY')
        CrearOnda(Resultante=True,Fuentes=['OndaX','OndaY'],Color='y')

    if n==8:
        CrearOnda()
        CrearOnda(Angulo=np.pi/2,Color='r',Phase=np.pi)
        CrearOnda(Angulo=np.pi/2,Color='violet')

    if n==9:
        CrearOnda(Nombre='OndaX')
        CrearOnda(Angulo=np.pi/2,Color='r',Phase=np.pi,Mostrar=False,Nombre='OndaY')
        CrearOnda(Angulo=np.pi/2,Color='violet',Mostrar=False,Nombre='OndaY-')
        CrearOnda(Resultante=True,Fuentes=['OndaY','OndaY-'],Nombre='Resultante',Color='y')

    if n==10:
        CrearOnda(Nombre='OndaX')
        CrearOnda(Angulo=np.pi/2,Color='r',Phase=np.pi,Mostrar=False,Nombre='OndaY')
        CrearOnda(Angulo=np.pi/2,Color='violet',Mostrar=False,Nombre='OndaY-')
        CrearOnda(Resultante=True,Fuentes=['OndaY','OndaX'],Nombre='Resultante',Color='r')
        CrearOnda(Resultante=True,Fuentes=['OndaY-','OndaX'],Nombre='Resultante',Color='violet')

    if n==11:
        CrearOnda(Nombre='OndaX')
        CrearOnda(Angulo=np.pi/2,Color='r',Phase=np.pi,Mostrar=True,Nombre='OndaY')
        CrearOnda(Angulo=np.pi/2,Color='violet',Mostrar=True,Nombre='OndaY-')
        CrearOnda(Resultante=True,Fuentes=['OndaY','OndaX'],Nombre='Resultante',Color='r')
        CrearOnda(Resultante=True,Fuentes=['OndaY-','OndaX'],Nombre='Resultante',Color='violet')
        
    #
    # Ejemplos de ondas circulares
    #
    if n==12:
        CrearOnda(Nombre='OndaX')
        CrearOnda(Angulo=np.pi/2,Color='r',Phase=np.pi/2,Mostrar=True,Nombre='OndaY')
    if n==13:
        CrearOnda(Nombre='OndaX')
        CrearOnda(Angulo=np.pi/2,Color='r',Phase=np.pi/2,Mostrar=True,Nombre='OndaY')
        CrearOnda(Resultante=True,Fuentes=['OndaY','OndaX'],Nombre='Resultante+',Color='green')
    if n==14:
        CrearOnda(Nombre='OndaX')
        CrearOnda(Angulo=np.pi/2,Color='r',Phase=np.pi/2+np.pi,Mostrar=True,Nombre='OndaY')
        CrearOnda(Resultante=True,Fuentes=['OndaY','OndaX'],Nombre='Resultante-',Color='y')
    if n==15:
        CrearOnda(Nombre='OndaX')
        CrearOnda(Angulo=np.pi/2,Color='r',Phase=-np.pi/2,Mostrar=True,Nombre='OndaY-')
        CrearOnda(Angulo=np.pi/2,Color='green',Phase=np.pi/2,Mostrar=True,Nombre='OndaY+')
        CrearOnda(Resultante=True,Fuentes=['OndaY+','OndaX'],Nombre='Resultante+',Color='green')
        CrearOnda(Resultante=True,Fuentes=['OndaY-','OndaX'],Nombre='Resultante-',Color='r')
    if n==16:
        CrearOnda(Tipo='Circular+')
        CrearOnda(Tipo='Circular-',Color='r')

    #
    # Ejemplos de reconstruccion de ondas lineales con circulares   
    #
    if n==17:
        CrearOnda(Tipo='Circular+',Nombre='C+')
        CrearOnda(Tipo='Circular-',Color='r',Nombre='C-')        
        CrearOnda(Resultante=True,Fuentes=['C+','C-'],Color='green')
    if n==18:
        CrearOnda(Tipo='Circular+',Nombre='C+',Phase=np.pi/2)
        CrearOnda(Tipo='Circular-',Color='r',Nombre='C-',Phase=np.pi/2)        
        CrearOnda(Resultante=True,Fuentes=['C+','C-'],Color='y')
    if n==19:
        CrearOnda(Tipo='Circular+',Nombre='C+')
        CrearOnda(Tipo='Circular-',Color='r',Nombre='C-',Phase=np.pi)        
        CrearOnda(Resultante=True,Fuentes=['C+','C-'],Color='y')
    if n==20:
        CrearOnda(Tipo='Circular+',Nombre='C+')
        CrearOnda(Tipo='Circular-',Color='r',Nombre='C-',Phase=np.pi/2)        
        CrearOnda(Resultante=True,Fuentes=['C+','C-'],Color='y')
    #
    # Ejemplos de ondas elipticas
    #
    if n==21:
        CrearOnda(Nombre='OndaX',Amplitud=0.5)
        CrearOnda(Angulo=np.pi/2,Color='r',Phase=np.pi/2,Mostrar=True,Nombre='OndaY')
        CrearOnda(Resultante=True,Fuentes=['OndaX','OndaY'],Color='y')
    if n==22:
        CrearOnda(Nombre='OndaX')
        CrearOnda(Angulo=np.pi/2,Color='r',Phase=np.pi/3,Mostrar=True,Nombre='OndaY')
        CrearOnda(Resultante=True,Fuentes=['OndaX','OndaY'],Color='y')
    if n==23:
        CrearOnda(Nombre='OndaX',Amplitud=0.5)
        CrearOnda(Angulo=np.pi/2,Color='r',Phase=np.pi/3,Mostrar=True,Nombre='OndaY')
        CrearOnda(Resultante=True,Fuentes=['OndaX','OndaY'],Color='y')    
        
    if n==24:
        CrearOnda(Tipo='Circular+',Nombre='C+',Amplitud=0.5)
        CrearOnda(Tipo='Circular-',Color='r',Nombre='C-')        
        CrearOnda(Resultante=True,Fuentes=['C+','C-'],Color='y')
    if n==25:
        CrearOnda(Tipo='Circular+',Nombre='C+',Amplitud=0.5,Phase=np.pi/3)
        CrearOnda(Tipo='Circular-',Color='r',Nombre='C-')        
        CrearOnda(Resultante=True,Fuentes=['C+','C-'],Color='y')


    #
    # Hacer resumen de ondas
    #

    #
    # Ejemplos de bases arbitrarias
    #
    if n==26:
        Parametros['VistaFrente']=True
        Angulo0=0
        CrearOnda(Nombre='OndaX',Angulo=Angulo0)
        CrearOnda(Nombre='OndaY',Color='r',Angulo=Angulo0+np.pi/2,Mostrar=True)
        CrearOnda(Resultante=True,Fuentes=['OndaX','OndaY'],Color='y')   
    if n==27:
        Parametros['VistaFrente']=True
        Angulo0=np.pi/8
        CrearOnda(Nombre='OndaX',Angulo=Angulo0)
        CrearOnda(Nombre='OndaY',Color='r',Angulo=Angulo0+np.pi/2,Mostrar=True)
        CrearOnda(Resultante=True,Fuentes=['OndaX','OndaY'],Color='y')    
    if n==28:
        Parametros['VistaFrente']=True
        Angulo0=np.pi/4
        CrearOnda(Nombre='OndaX',Angulo=Angulo0)
        CrearOnda(Nombre='OndaY',Color='r',Angulo=Angulo0+np.pi/2,Mostrar=True)
        CrearOnda(Resultante=True,Fuentes=['OndaX','OndaY'],Color='y')   

    #
    # Ejemplos polarizador
    #

    if n==29:
        Parametros['VistaFrente']=True
        CrearOnda()
        CrearObjeto('Polarizador',15)
    if n==30:
        Parametros['VistaFrente']=True
        CrearOnda()
        CrearObjeto('Polarizador',15,Angulo=np.pi/2)
    if n==31:                     
        Parametros['VistaFrente']=True
        CrearOnda()
        CrearObjeto('Polarizador',15,Angulo=np.pi/4)
    if n==32:
        Parametros['VistaFrente']=True
        CrearOnda()
        CrearObjeto('Polarizador',15,Angulo=np.pi/10)
    if n==33:
        Parametros['VistaFrente']=True
        CrearOnda()
        CrearObjeto('Polarizador',15,Angulo=np.pi/10*4)
    if n==34:
        Parametros['VistaFrente']=True
        CrearOnda()
        CrearOnda(Angulo=np.pi/2,Color='r')
        CrearObjeto('Polarizador',15,Angulo=np.pi/10*4)

    #
    # No distingue la fase
    #

    if n==35:
        Parametros['VistaFrente']=True
        CrearOnda()
        CrearOnda(Color='r',Phase=np.pi/2)
        CrearObjeto('Polarizador',15,Angulo=np.pi/10*4)
    if n==36:
        Parametros['VistaFrente']=True
        CrearOnda(Tipo='Circular+')
        CrearObjeto('Polarizador',15,Angulo=np.pi/2)
        
    if n==37:
        Parametros['VistaFrente']=True
        CrearOnda(Nombre='Ondax')
        CrearOnda(Angulo=np.pi/2,Color='r',Nombre='Onday')
        CrearOnda(Resultante=True, Fuentes=['Ondax','Onday'],Color='y')
        CrearObjeto('Polarizador',10,Borde=False)
        CrearObjeto('Polarizador',20,Angulo=np.pi/2,Borde=False)
    if n==38:
        Parametros['VistaFrente']=True
        CrearOnda()
        CrearObjeto('Polarizador',5,Borde=False)
        CrearObjeto('Polarizador',15,Angulo=np.pi/4,Borde=False)
        CrearObjeto('Polarizador',25,Angulo=np.pi/2,Borde=False)


    if n==39:
        Parametros['VistaFrente']=True
        CrearOnda()
        CrearObjeto('Polarizador',10,Borde=False)
        CrearObjeto('Polarizador',11,Angulo=np.pi/20*1,Color='y',Borde=False)
        CrearObjeto('Polarizador',12,Angulo=np.pi/20*2,Color='y',Borde=False)
        CrearObjeto('Polarizador',13,Angulo=np.pi/20*3,Color='y',Borde=False)
        CrearObjeto('Polarizador',14,Angulo=np.pi/20*4,Color='y',Borde=False)
        CrearObjeto('Polarizador',15,Angulo=np.pi/20*5,Color='y',Borde=False)
        CrearObjeto('Polarizador',16,Angulo=np.pi/20*6,Color='y',Borde=False)
        CrearObjeto('Polarizador',17,Angulo=np.pi/20*7,Color='y',Borde=False)
        CrearObjeto('Polarizador',18,Angulo=np.pi/20*8,Color='y',Borde=False)
        CrearObjeto('Polarizador',19,Angulo=np.pi/20*9,Color='y',Borde=False)
        CrearObjeto('Polarizador',20,Angulo=np.pi/2,Borde=False)
		
	if n==41:
		CrearOnda(Nombre='OndaX')
		CrearOnda(Angulo=np.pi/2,Color='r',Phase=np.pi/2,Mostrar=True,Nombre='OndaY')
		CrearOnda(Resultante=True,Fuentes=['OndaY','OndaX'],Nombre='Resultante+',Color='green')

Ejemplo(ej_consola)




# Nota, los polarizadores se definen en funcion de su angulo de transmision, y se mide respecto a X
# Las laminas se definen con su angulo del indice en x respecto al eje x
#CrearObjeto('Polarizador',25,Angulo=np.pi/6*5)
#CrearObjeto('Lamina',11,Largo=6,Angulo=np.pi/3,IndiceX=3,IndiceY=1.5,Color='g')

Tramos=sorted(Tramos,key=getKey) # Ordena los tramos


## 
## Comienza la parte de grafica
##

# Set up figure & 3D axis for animation
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.axis('on')
ax.set_ylabel('y')
if Parametros['VistaFrente']:
    ax.set_xlabel('x')
else:
    ax.set_zlabel('x')


# set up lines and points
#Colores=[]
#for CadaOnda in Ondas:
#    Colores.append(CadaOnda[5]) #Crea una lista de los colores de las ondas moviles
    
ColoresFijos=[]
Colores=[]
for LineaFija in Lineasfijas:
    ColoresFijos.append(LineaFija[1]) #Crea una lista de los colores de las lineas fijas

for CadaOnda in Ondas:
    Colores.append(CadaOnda.Color)
    
Contornos=sum([ax.plot([], [], [], '-', c=c)
             for c in ColoresFijos], [])
lines = sum([ax.plot([], [], [], '-', c=c)
             for c in Colores], [])
pts = sum([ax.plot([], [], [], 'o', c=c)
           for c in Colores], [])


# prepare the axes limits
if Parametros['VistaFrente']:
    ax.set_xlim((-Parametros['TamanoEjeX'],Parametros['TamanoEjeX']))
    ax.set_ylim((-Parametros['TamanoEjeY'],Parametros['TamanoEjeY']))
    ax.set_zlim((Parametros['ZInicial'], Parametros['ZFinal']))
else:
    ax.set_zlim((-Parametros['TamanoEjeX'],Parametros['TamanoEjeX']))
    ax.set_ylim((-Parametros['TamanoEjeY'],Parametros['TamanoEjeY']))
    ax.set_xlim((Parametros['ZInicial'], Parametros['ZFinal']))

# set point-of-view: specified by (altitude degrees, azimuth degrees)
ax.view_init(0,90)

# initialization function: plot the background of each frame
def init():
    #Define lieas moviles
    for line, pt in zip(lines, pts):
        line.set_data([], [])
        line.set_3d_properties([])

        pt.set_data([], [])
        pt.set_3d_properties([])
    for Contorno in Contornos:
        Contorno.set_data([], [])
        Contorno.set_3d_properties([])
        
    return Contornos + lines + pts

# animation function.  This will be called sequentially with the frame number
def animate(i):
    for line, pt, CadaOnda in zip(lines, pts, Ondas): # Dibuja las lineas moviles
        if CadaOnda.Mostrar:
            T=Parametros['ZFinal']/pc.c #Es el tiempo que tarda en llegar la onda de una punta a la otra si n=1
            t=(i*T)/500
            OndaActual = np.asarray(CadaOnda.CalculoFuncionCompleta(t))
            
            xi,yi,zi=OndaActual.T
            if Parametros['VistaFrente']:
                line.set_data(xi, yi)
                line.set_3d_properties(zi)
                pt.set_data(xi[0], yi[0]) #Por alguna razon tira error cuando el vector viene vacio. Revisar
                pt.set_3d_properties(zi[0])
            else:
                line.set_data(zi, yi)
                line.set_3d_properties(xi)
                pt.set_data(zi[0], yi[0]) #Por alguna razon tira error cuando el vector viene vacio. Revisar
                pt.set_3d_properties(xi[0])

    for Contorno, n, in zip (Contornos, range(len(Lineasfijas))): #Dibuja las lineas fijas
        
        LineaFija=Lineasfijas[n]
        Valores=LineaFija[0]
        xi,yi,zi=Valores.T
        if Parametros['VistaFrente']:
            Contorno.set_data(xi, yi)
            Contorno.set_3d_properties(zi)        
        else:
            Contorno.set_data(zi, yi)
            Contorno.set_3d_properties(xi)        
        
#    ax.view_init(30, 0.3 * i)
    fig.canvas.draw()
    return Contornos # lines + pts + 

# instantiate the animator.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=500, interval=30, blit=True)

# Save as mp4. This requires mplayer or ffmpeg to be installed
#anim.save('lorenz_attractor.mp4', fps=15, extra_args=['-vcodec', 'libx264'])

plt.show()
