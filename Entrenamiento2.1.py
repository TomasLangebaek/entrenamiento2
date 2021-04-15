# La Lactosa S.A.S.

import pulp as lp

# CONJUNTOS
NADADORES=['Alejandro','Alfaima','Andres','Ariadna','Benji','Camila','Camilo G','Cesar','Cristian',
'Daniel C','Daniel Y','Diana','Felipe','Freddy','Jimmy','Johan','Juan Diego','Juan E','Juliana',
'Lucia','Maria Paulina','Santiago','Saul','Sofia','Valentina','Vivian'
]
# PARAMETROS
SALARIO={'Alejandro':2100000,'Alfaima':10300000,'Andres':8930000,'Ariadna':9000000,'Benji':13000000,
'Camila':2750000,'Camilo G':6000000,'Cesar':20000000,'Cristian':2300000,'Daniel C':3600000,
'Daniel Y':29000000,'Diana':3100000,'Felipe':5490000,'Freddy':2230000,'Jimmy':5000000,'Johan':15500000,
'Juan Diego':7100000,'Juan E':6700000,'Juliana':2550000,'Lucia':9860000,'Maria Paulina':13000000,
'Santiago':3450000,'Saul':16000000,'Sofia':3000000,'Valentina':3500000,'Vivian':4000000
}

DESEMPEÑO={'Alejandro':1,'Alfaima':7,'Andres':4,'Ariadna':9,'Benji':7,'Camila':6,'Camilo G':7,'Cesar':9,
'Cristian':7,'Daniel C':5,'Daniel Y':10,'Diana':6,'Felipe':6,'Freddy':8,'Jimmy':9,'Johan':8,'Juan Diego':8,
'Juan E':3,'Juliana':6,'Lucia':3,'Maria Paulina':5,'Santiago':6,'Saul':10,'Sofia':4,'Valentina':6,'Vivian':7}

PRESUPUESTO=85000000



# VARIABLES DE DECISION
x = lp.LpVariable.dict('Escoger_nadador', NADADORES, 0, None, lp.LpBinary)

# CREAR EL PROBLEMA

prob = lp.LpProblem('Nadadores', lp.LpMaximize)

# FUNCION OBJETIVO

prob += lp.lpSum(x[n]*DESEMPEÑO[n] for n in NADADORES)

# RESTRICCIONES

# En caso de escoger a Ariadna, debe escoger a Felipe. 
prob += (x['Ariadna']==x['Ariadna'])

#En caso de escoger a Freddy o a Alejandro (o los dos), debe escoger a Daniel C.
prob += ((x['Freddy']+x['Alejandro'])/2<=x['Daniel C'])

      
#Se deben seleccionar máximo dos de los nadadores estándar: Juan Diego, Juan E, Juliana, Sofía o Valentina.
prob += (lp.lpSum([x['Juan Diego'],x['Juan E'],x['Juliana'],x['Sofia'],x['Valentina']])<=2)
    
#En caso de escoger a Camila y Jimmy, se debe escoger a Diana o Alfaima (o las dos).
prob += (x['Camila']+x['Jimmy']<=x['Diana']+x['Alfaima'])
# Satisfacer la demanda de los clientes

#En caso de escoger a Johan o Daniel Y, se debe escoger a Andrés y a Lucia.
prob += ((x['Johan']+x['Daniel Y'])/2<=x['Andres'])

prob += ((x['Johan']+x['Daniel Y'])/2<=x['Lucia'])
        
#Se debe escoger al menos un nadador especial: Vivian, Cristian, María Paulina, Saúl.
prob += (x['Vivian']+x['Cristian']+x['Maria Paulina']+x['Saul'])>=1

#En caso de escoger a Santiago, no se debe escoger a Benji.
prob += (x['Santiago']+x['Benji']<=1)

#No se debe superar el presupuesto
prob += (lp.lpSum(x[n]*SALARIO[n] for n in NADADORES)<=PRESUPUESTO)

# RESOLVER EL PROBLEMA

prob.solve()

# ESTADO DEL PROBLEMA

print('status: ', lp.LpStatus[prob.status])

# FUNCION OBJETIVO
# imprimir la fo
print('El desempeño total es: ', lp.value(prob.objective))

for n in NADADORES:
    if x[n].varValue == 1:
        print(f'Se selecciono el nadador {n}, {SALARIO[n]}')
    else:
        print(f'No se seleccionó el nadador {n} ')


