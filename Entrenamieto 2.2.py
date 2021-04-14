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











    