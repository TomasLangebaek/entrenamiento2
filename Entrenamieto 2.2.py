# La Lactosa S.A.S.

import pulp as lp

# CONJUNTOS

LOCALES=['Chapinero','La Candelaria','Av 7','Av Jiménez']

UNIVERSIDADES=['Javeriana','Rosario','Tadeo','Central']


# PARAMETROS
# Cantidad maxima de panaderos un local
panaderos={'Chapinero':20,'La Candelaria':15,'Av 7':10,'Av Jiménez':5}

#osto diario de mantenimiento [COP]   en un local 
costo_mantenimiento={'Chapinero':250000,'La Candelaria': 165000 ,'Av 7':300000,'Av Jiménez':150000}


costo_envio={('Chapinero','Javeriana'):0.3,('Chapinero','Rosario'):1.5,('Chapinero','Tadeo'):0.9,
   ('Chapinero','Central'):0.4,('La Candelaria','Javeriana'):1.1,('La Candelaria','Rosario'):0.4,
   ('La Candelaria','Tadeo'):0.2,('La Candelaria','Central'):1,('Av 7','Javeriana'):0.1,
   ('Av 7','Rosario'):1.7,('Av 7','Tadeo'):1.9,('Av 7','Central'):0.2,
   ('Av Jiménez','Javeriana'):1.7,('Av Jiménez','Rosario'):0.1,('Av Jiménez','Tadeo'):0.3,
   ('Av Jiménez','Central'):1.6}


desempeno={'Alejandro':1,'Alfaima':7,'Andrés':4,'Ariadna':9,'Benji':7,'Camila':6,'Camilo':7,'César':9,'Cristian':7,'Daniel C':5,'Daniel Y':10,'Diana':6,'Felipe':6,'Freddy':8,'Jimmy':9,'Johan':8,'Juan Diego':8,'Juan E':3,'Juliana':6,'Lucia':3,'María Paulina':5,'Santiago':6,'Saúl':10,'Sofía':4,'Valentina':6,'Vivian':7}
# Costo de transporte de proveedores a planta
b={('SUTATAUSA','UBATE'):16.5,('SUTATAUSA','CAJICA'):30.9,
   ('CARMEN DE CARUPA','UBATE'):19.7,('CARMEN DE CARUPA','CAJICA'):46.2,
   ('COGUA','UBATE'):27.1,('COGUA','CAJICA'):10.8,
   ('SOPO','UBATE'):38.3,('SOPO','CAJICA'):15.6}

# Costo de transporte de plantas a clientes
e={('UBATE','VILLAPINZON'):33.4,('UBATE','SUESCA'):37.8,('UBATE','ZIPAQUIRA'):28.1,('UBATE','PACHO'):54.7,('UBATE','CHOCONTA'):24.8,('UBATE','NEMOCON'):28.3,
   ('CAJICA','VILLAPINZON'):42.7,('CAJICA','SUESCA'):26.3,('CAJICA','ZIPAQUIRA'):10.5,('CAJICA','PACHO'):33.4,('CAJICA','CHOCONTA'):34.1,('CAJICA','NEMOCON'):18.9}

# Demanda de los clientes por cada tipo de leche
d={('VILLAPINZON','ENTERA'):13802,('VILLAPINZON','DESCREMADA'):1131,('VILLAPINZON','DESLACTOSADA'):2677,
   ('SUESCA','ENTERA'):10032,('SUESCA','DESCREMADA'):4193,('SUESCA','DESLACTOSADA'):1223,
   ('ZIPAQUIRA','ENTERA'):120353,('ZIPAQUIRA','DESCREMADA'):44322,('ZIPAQUIRA','DESLACTOSADA'):10521,
   ('PACHO','ENTERA'):18899,('PACHO','DESCREMADA'):1751,('PACHO','DESLACTOSADA'):3594,
   ('CHOCONTA','ENTERA'):44368,('CHOCONTA','DESCREMADA'):4960,('CHOCONTA','DESLACTOSADA'):1404,
   ('NEMOCON','ENTERA'):7930,('NEMOCON','DESCREMADA'):2576,('NEMOCON','DESLACTOSADA'):1525}

# variables de decicion
x=lp.LpVariable.dicts(name='Litros_leche_plantas_a_clientes', indexs=[(l,p,c)for l in TIPOS_DE_LECHE for p in PLANTAS for c in CLIENTES])

lista_auxiliar =[]
for  l in TIPOS_DE_LECHE:
    for p in PLANTAS:
        for c in CLIENTES:
            lista_auxiliar.append((l,p,c))
            
x=lp.LpVariable.dicts(name='Litros_leche_plantas_a_clientes', indexs=lista_auxiliar, lowBound= 0, cat=lp.LpContinuous)

lista_auxiliar_indices =[]
for v in PROVEEDORES:
    for p in PLANTAS:
        lista_auxiliar_indices.append((v,p))
            
            
z=lp.LpVariable.dicts(name='Litros_leche_proveedores_plantas', indexs=lista_auxiliar_indices, lowBound= 0, cat=lp.LpContinuous)

#Crear problema
prob =lp.LpProblem(name="Transporte", sense =lp.LpMinimize)

#Funcion Objetivo

prob+=lp.lpSum(e[(p,c)]*lp.lpSum(x[(l,p,c)]for l in TIPOS_DE_LECHE)for p in PLANTAS for c in CLIENTES)+lp.lpSum(b[(v,p)]*z[(v,p)]for v in PROVEEDORES for p in PLANTAS)

#Restricciones

#Balance de Produccion

for p in PLANTAS:
    prob+=lp.lpSum(z[(v, p)]for v in PROVEEDORES)== lp.lpSum(x[(l,p,c)]for c in CLIENTES for l in TIPOS_DE_LECHE ), "Balance_de_preduccion"+str(p)

#Capacidad

for v in PROVEEDORES:
    prob+=lp.lpSum(z[(v, p)]for p in PLANTAS)<=k[v], "Capacidad_proveedor"+str(v)


#Demanda

for c in CLIENTES:
    for l in TIPOS_DE_LECHE:
        prob+=lp.lpSum(x[(l,p,c)]for p in PLANTAS)>=d[(c,l)], "Demanda_cliente"+str(c)+"por_tipo"+str(l)
        
#Resolver el problema
prob.solve()

#Estado del problema
print("Status: ",lp.LpStatus[prob.status])

#Funcion Objetivo

print(f 'El costo total es:{lp.value(prob.objective)} ')











    