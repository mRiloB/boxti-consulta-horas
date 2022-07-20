import pandas as pd
from datetime import datetime
import ssl
from fastapi import FastAPI
ssl._create_default_https_context = ssl._create_unverified_context

app = FastAPI()


def fmt(dt: str) -> str:
    dt = int(dt)
    return f'0{dt}' if dt < 10 else dt


def create_url(mini: str, mfim: str) -> str:
    dt = datetime.now()
    mini = mini if mini else str(dt.month - 1)
    mfim = mfim if mfim else str(dt.month)
    url = f'https://www.boxti.com.br/bs/_rotinaBS/consultaHorasDev.php?dataInicio=2022-{fmt(mini)}-21&dataFim=2022-{fmt(mfim)}-20'
    return url


@app.get("/")
def read_root():
    return {"version": "v1.0.5"}


@app.get("/consultar")
def show_all(mesInicio: str = '', mesFim: str = ''):
    url = create_url(mesInicio, mesFim)
    data = pd.read_html(url)
    table = data[0]
    arr_table = [value.array for _, value in table.iterrows()]
    
    ret = [
        {
            'dev': item[0],
            'totais': {'qtd': item[1], 'porc': item[2]},
            'boxti': {'qtd': item[3], 'porc': item[4]},
            'clientes': {'qtd': item[5], 'porc': item[6]},
            'faturadas': {'qtd': item[7], 'porc': item[8]}
        }
        for item in arr_table
    ]

    return ret
