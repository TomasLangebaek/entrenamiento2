# La Lactosa S.A.S.

import pulp as lp

# CONJUNTOS

LOCALES=['Chapinero','La Candelaria','Av 7','Av Jiménez']

UNIVERSIDADES=['Javeriana','Rosario','Tadeo','Central']


# PARAMETROS
# Cantidad maxima de panaderos un local
panaderos={'Chapinero':20,'La Candelaria':15,'Av 7':10,'Av Jiménez':5}

#costo diario de mantenimiento [COP]   en un local 
costo_mantenimiento={'Chapinero':250000,'La Candelaria': 165000 ,'Av 7':300000,'Av Jiménez':150000}

#Costo de envio de un local a una universidad
costo_envio={('Chapinero','Javeriana'):0.3,('Chapinero','Rosario'):1.5,('Chapinero','Tadeo'):0.9,
   ('Chapinero','Central'):0.4,('La Candelaria','Javeriana'):1.1,('La Candelaria','Rosario'):0.4,
   ('La Candelaria','Tadeo'):0.2,('La Candelaria','Central'):1,('Av 7','Javeriana'):0.1,
   ('Av 7','Rosario'):1.7,('Av 7','Tadeo'):1.9,('Av 7','Central'):0.2,
   ('Av Jiménez','Javeriana'):1.7,('Av Jiménez','Rosario'):0.1,('Av Jiménez','Tadeo'):0.3,
   ('Av Jiménez','Central'):1.6}

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

for l in LOCALES:
    if x[l].varValue == 1:
        print(f'Se compro el local {l}, número panaderos {y[l].varValue}')
        for u in UNIVERSIDADES:
            print(f'Se enviaron {z[(l,u)].varValue} productos a la universidad {u}')
    else:
        print(f'No se compró el local {l} ')
    

    