import pandas as pd
import numpy as np
import plotly.express as px
import os


# función que convierte periodo en numero de pagos al año

def periodo(pagos):
    if pagos == 'quincenal':
        n=15/360
    elif pagos == 'mensual':
        n=30/360
    elif pagos == 'bimestral':
        n=60/360
    elif pagos == 'trimestral':
        n=90/360
    elif pagos == 'cuatrimestral':
        n=120/360
    elif pagos == 'semestral':
        n=180/360
    elif pagos == 'anual':
        n=1
    return(n)

def anualidad(t,i,pagos):
    an=((1-(1+i*periodo(pagos))**(-t/periodo(pagos)))/(i*periodo(pagos)))
    return(an)



def getURL_SVG(monto):
    # monto del prestamo
    #monto=float(input("Monto a invertir: "))
    
    #tiempo en años 
    #t=int(input("Años en los que planea pagar el crédito: "))
    t=5
    # tasa de interés credito expreasada en porcentaje
    #i=(int(input("Tasa de interés del crédito: "))/100)
    i=4

    # periodicidad con la que el usuario pagará el credito (quincenal, mensual, bimestral, 
    # trimestral, cuatrimestral, semestral, anual)
    #pagos = str(input("Periodicidad de los pagos del crédito: "))
    pagos="trimestral"

    # tasa fectiva por periodo (la tasa efectiva se refiere a la tasa de interes que se pagará en cada pago)
    tasa_efectiva = round(i*periodo(pagos),8)

    # anualidad (función que me permite determinar el monto del pago)
    pa=monto/anualidad(t,i,pagos)

    plazo=[str(int(360*periodo(pagos))) +' días']*int((1/periodo(pagos))*t)
    anio=sorted(list(range(1,(t+1)))*int(1/periodo(pagos)))
    pago=list(range(1,(t*int(1/periodo(pagos))+1)))
    Mont=[round(pa,2)]*t*int(1/periodo(pagos))

    SI=[monto]
    Int=[round(tasa_efectiva*SI[0],2)]
    pag=[Mont[0]-Int[0]]
    SF=[SI[0]-pag[0]]

    for i in range(1,int(1/periodo(pagos))*t):
                    SI=SI + [round(SF[i-1],2)]
                    Int=Int + [round(tasa_efectiva*SI[i],2)]
                    pag=pag + [round(Mont[0]-Int[i],2)]
                    SF=SF + [round(SI[i]-pag[i],2)]
                    


    d={'Plazo': plazo,'Año': anio,'No_pago': pago, 'Saldo_Inicial':SI, 'Pago_Capital': pag, 
    'Pago_Interes': Int, 'Monto_pago': Mont, 'Saldo_Final': SF}
    df = pd.DataFrame(d)
    Costo=df['Pago_Interes'].sum()
    df

    No_pagos=pago*3
    amort=SF + pag + Int
    tipo=['Saldo']*int(1/periodo(pagos))*t+['Pago Amortización']*int(1/periodo(pagos))*t+['Interés']*int(1/periodo(pagos))*t

    d={'No pago': No_pagos, 'Pago':amort,'Tipo':tipo}
    df = pd.DataFrame(d)

    long_df = px.data.medals_long()

    fig = px.bar(df, x="No pago", y="Pago", color="Tipo")

    print("Path at terminal when executing this file")
    print(os.getcwd() + "\n")

    url="fig_prestamos.svg"
    fig.write_image("investart/static/img/"+url)
    return url
#print(getURL_SVG(1000))

def cetes1(monto):
    # monto de inverión
    # multiplo de $10
    # inversión inicial mayor a $100
    # monto=float(input("Monto a invertir: "))
    monto=float(monto)
    # #tiempo en meses (1, 3, 6, 12)
    # t=int(input("Periodo de inversión(1 mes, 3 meses, 6 meses, 12 meses): "))
    t=12
    # #años que quieres invertir tu dinero
    # aniodin=int(input("Años que planea ahorrar: "))
    aniodin=1

    # tasa de interés CETES (podemos ocupar API)
    if t==1:
        i=(4.25/100)*(28/360)
    elif t==3:
        i=(4.32/100)*(91/360)
    elif t==6:
        i=(4.35/100)*(180/360)
    elif t==12:
        i=4.36/100


    periodos=12*aniodin


    ISR=i*monto/3

    intereses1=np.array(range(1,(periodos+1)))*i*monto-ISR
    intereses2=(np.array(range(1,(periodos+1)))*i*monto-ISR)*np.array(range(1,periodos+1))
    r=np.array(range(1,(periodos+1)))*monto

    m1=[monto]*periodos+intereses1.tolist()
    m2=r.tolist()+intereses2.tolist()
    p=list(range(1,(periodos+1)))*2
    inte=['monto']*periodos+['interes']*periodos

    d={'Años': p, 'interes':inte, 'Rendimiento': m1, 'rendimiento':m2}
    df = pd.DataFrame(d)

    long_df = px.data.medals_long()

    fig = px.bar(df, x="Años", y="Rendimiento", color="interes")
    url="fig_cetes1.svg"
    fig.write_image("investart/static/img/"+url)
    return url
#print(cetes1(1000))

def bonos(monto):
    # monto de inverión
    # multiplo de $100
    # inversión inicial mayor a $100
    # monto=float(input("Monto a invertir: "))
    monto=float(monto)
    # #tiempo en años (3, 5, 10, 20, 30
    # t=int(input("Periodo de inversión en años(3, 5, 6, 12): "))
    t=5
    # # tasa de interés Bonos (podemos ocupar API)
    # i=(5.68/100)
    i=5.67
    # lo que va a pagar el bono cada 6 meses (sin descontar ISR)
    interes_semestral=i*monto*182/360

    #constante
    ISR=interes_semestral*0.255282

    # lo que va a pagar el bono cada 6 meses 
    rendimiento_real=interes_semestral-ISR

    m1=np.zeros(t-1).tolist()*2+np.zeros(1).tolist()+[monto]+[rendimiento_real]*t*2
    p=list(range(1,(2*t+1)))*2
    inte=['monto']*t*2+['interes']*t*2

    d={'Meses': p, 'interes':inte, 'Rendimiento': m1}
    df = pd.DataFrame(d)

    print(df['Rendimiento'].sum())

    long_df = px.data.medals_long()

    fig = px.bar(df, x="Meses", y="Rendimiento", color="interes")
    url="fig_bonos.svg"
    fig.write_image("investart/static/img/"+url)
    return url
#print(bonos(1000))
def bondes(monto):
    # monto de inverión
    # multiplo de $100
    # inversión inicial mayor a $100
    monto=float(monto)

    #tiempo en años (5)
    t=5

    # tasa de interés Bondes (podemos ocupar API)
    i=(4.7/100)+np.random.normal(0,0.0005,65)


    # lo que va a pagar el bono cada 28 dias (sin descontar ISR)
    interes_bruto=i*monto*28/366

    #constante
    ISR=monto*0.0145*28/366

    # lo que va a pagar el bono cada 6 meses 
    rendimiento_real=interes_bruto-ISR

    m1=np.zeros(t-1).tolist()*13+np.zeros(12).tolist()+[monto]+rendimiento_real.tolist()
    p=list(range(1,(13*t+1)))*2
    inte=['monto']*t*13+['interes']*t*13

    d={'Periodos': p, 'interes':inte, 'Rendimiento': m1}
    df = pd.DataFrame(d)

    print(df['Rendimiento'].sum())

    long_df = px.data.medals_long()

    fig = px.bar(df, x="Periodos", y="Rendimiento", color="interes")
    url="fig_bondes.svg"
    fig.write_image("investart/static/img/"+url)
    return url
