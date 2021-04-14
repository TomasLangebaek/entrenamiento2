# La Lactosa S.A.S.

import pulp as lp

# CONJUNTOS

PELICULAS=['Titanic','Inception','Pulp Fiction','Fight club']

PARQUEADEROS=['Oro','Platino','Plata','Bronce','VIP']

FRANJAS=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]


# PARAMETROS
# Cantidad maxima de panaderos un local
duracion={'Titanic':7,'Inception':6,'Pulp Fiction':6,'Fight club':5}

#costo diario de mantenimiento [COP]   en un local 
min_proyecciones={'Titanic':1,'Inception':5,'Pulp Fiction':2,'Fight club':3}

#Costo de envio de un local a una universidad
asistencia={('Titanic',1):73,('Titanic',2):107,('Titanic',3):96,
   ('Titanic',4):78,('Titanic',5):75,('Titanic',6):54,
   ('Titanic',7):105,('Titanic',8):62,('Titanic',9):110,
   ('Titanic',10):115,('Titanic',11):0,('Titanic',12):0,
   ('Titanic',13):0,('Titanic',14):0,('Titanic',15):0,
   ('Titanic',16):0,('Inception',1):102,('Inception',2):109,('Inception',3):128,
   ('Inception',4):108,('Inception',5):115,('Inception',6):113,
   ('Inception',7):119,('Inception',8):129,('Inception',9):128,
   ('Inception',10):126,('Inception',11):117,('Inception',12):0,
   ('Inception',13):0,('Inception',14):0,('Inception',15):0,
   ('Inception',16):0, ('Pulp Fiction',1):79,('Pulp Fiction',2):118,('Pulp Fiction',3):95,
   ('Pulp Fiction',4):107,('Pulp Fiction',5):123,('Pulp Fiction',6):121,
   ('Pulp Fiction',7):110,('Pulp Fiction',8):94,('Pulp Fiction',9):105,
   ('Pulp Fiction',10):127,('Pulp Fiction',11):111,('Pulp Fiction',12):0,
   ('Pulp Fiction',13):0,('Pulp Fiction',14):0,('Pulp Fiction',15):0,
   ('Pulp Fiction',16):0,('Fight club',1):98,('Fight club',2):137,('Fight club',3):147,
   ('Fight club',4):96,('Fight club',5):92,('Fight club',6):108,
   ('Fight club',7):137,('Fight club',8):107,('Fight club',9):138,
   ('Fight club',10):133,('Fight club',11):89,('Fight club',12):119,
   ('Fight club',13):0,('Fight club',14):0,('Fight club',15):0,
   ('Fight club',16):0}

#Demanda diaria en una Univerisdad
demanda={'Javeriana':2745,'Rosario':3965,'Tadeo':4402,'Central':2003}

#Salario diario de un panadero [COP]
salario=90000

#Producción diaria de un panadero [Productos de panaderia]
produccion=300


# variables de decicion

#Define si se compra o no el local
x = lp.LpVariable.dict('Comprar_local', LOCALES, 0, None, lp.LpBinary)
#numero de panaderos en el local l∈L
y = lp.LpVariable.dict('Número_panaeros', LOCALES, 0, None, lp.LpInteger)
#Cantidad de productos enviados del local l∈L a la universidad u∈U
lista_auxiliar_indices =[]
for l in LOCALES:
    for u in UNIVERSIDADES:
        lista_auxiliar_indices.append((l,u))
            
            
z=lp.LpVariable.dicts(name='productos_enviados', indexs=lista_auxiliar_indices, lowBound= 0, cat=lp.LpContinuous)


#Crear problema
prob =lp.LpProblem("Panaderia",lp.LpMinimize)

#Funcion Objetivo

prob+=lp.lpSum(x[l]*costo_mantenimiento[l]for l in LOCALES)+lp.lpSum(y[l]*salario for l in LOCALES)+lp.lpSum(z[(l,u)]*costo_envio[(l,u)] for l in LOCALES for u in UNIVERSIDADES)

#Restricciones

#Cantidad máxima de empleados por local
for l in LOCALES:
    prob+=y[l]<= panaderos[l]*x[l]

#Capacidad

for l in LOCALES:
    prob+=y[l]*produccion>=lp.lpSum(z[(l, u)]for u in UNIVERSIDADES)


#Demanda

for u in UNIVERSIDADES:
    prob+=lp.lpSum(z[(l,u)]for l in LOCALES)>=demanda[u]
        
#Resolver el problema
prob.solve()

#Estado del problema
print("Status: ",lp.LpStatus[prob.status])

#Funcion Objetivo

print('El costo total es: ', lp.value(prob.objective))











    