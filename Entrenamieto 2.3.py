# La Lactosa S.A.S.

import pulp as lp

# CONJUNTOS

PELICULAS=['Titanic','Inception','Pulp Fiction','Fight club']

PARQUEADEROS=['Oro','Platino','Plata','Bronce','VIP']

FRANJAS=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]


# PARAMETROS
# Duración de la pelicula m∈M
duracion={'Titanic':7,'Inception':6,'Pulp Fiction':6,'Fight club':5}

#Número minimo de proyecciones diarias de la pelicula  m∈M
min_proyecciones={'Titanic':1,'Inception':5,'Pulp Fiction':2,'Fight club':3}

#Asistencia para la película m∈M en la franja f∈F
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


# variables de decicion
lista_auxiliar_indices =[]
for m in PELICULAS:
    for p in PARQUEADEROS:
        for f in FRANJAS:
            lista_auxiliar_indices.append((m, p, f))
            
            
#Define si se esta proyectando la pelicula m∈M en el parqueadero p∈P en la franja f ∈F
x = lp.LpVariable.dicts('proyeccion', lista_auxiliar_indices, 0, None, lp.LpBinary)
#Define si se inicia la proyección de la pelicula m∈M en el parqueadero p∈P en la franja f ∈F
y = lp.LpVariable.dicts('inicio_proyeccion', lista_auxiliar_indices, 0, None, lp.LpBinary)

#Crear problema
prob = lp.LpProblem('AutoCine', lp.LpMaximize)

#Funcion Objetivo

prob+=lp.lpSum(y[(m, p, f)]*asistencia[(m,f)]for m in PELICULAS for p in PARQUEADEROS for f in FRANJAS)

#Restricciones

#Garantizar que en una sala solo se esté proyectando una película a la vez
for p in PARQUEADEROS:
    for f in FRANJAS:
        prob+=lp.lpSum(x[(m,p,f)]for m in PELICULAS)<=1

#Garantizar que una película se proyecte al menos una cantidad especifica de veces durante el día
for m in PELICULAS:
    prob+=lp.lpSum(y[(m,p,f)]for p in PARQUEADEROS for f in FRANJAS )<=min_proyecciones[m]


#Garantizar que no se inicie la proyección de una película en más de un parqueadero al tiempo

for f in FRANJAS:
    for m in PELICULAS:
        prob+=lp.lpSum(y[(m,p,f)]for p in PARQUEADEROS)<=1
    
#Modele la(s) condición(es) sobre la duración de una película

        
#Resolver el problema
prob.solve()

#Estado del problema
print("Status: ",lp.LpStatus[prob.status])

#Funcion Objetivo

print('El costo total es: ', lp.value(prob.objective))











    