from flask import Flask, render_template, request
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Endpoint
url = 'http://obpreprod.sidesoftcorp.com/comreivicpreprod/org.openbravo.service.json.jsonrest/MaterialMgmtStorageDetail'

@app.route('/', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        auth = HTTPBasicAuth(username, password)

        parametros = {
            '_selectedProperties': 'id,product,storageBin,attributeSetValue,uOM,quantityOnHand',
            '_where': 'quantityOnHand>0'
        }

        respuesta = requests.get(url, params=parametros, auth=auth)

        if respuesta.status_code == 200:
            datos = respuesta.json()['response']['data']

            total_registros = len(datos)
            total_productos = len(set(item['product'] for item in datos))

           
            # Productos con unidad de medida diferente a "UNIDAD" (ignorando mayúsculas/minúsculas)
            productos_con_uom_diferente = [item for item in datos if item['uOM$_identifier'].lower() != 'unidad']


            productos_ordenados = sorted(datos, key=lambda x: x['quantityOnHand'], reverse=True)[:10]

            return render_template('index.html', total_registros=total_registros, total_productos=total_productos,
                                   productos_con_uom_diferente=productos_con_uom_diferente, productos_ordenados=productos_ordenados)

        else:
            error = "Error al autenticar o al obtener los datos"
            return render_template('index.html', error=error, total_registros=0, total_productos=0,
                                   productos_con_uom_diferente=[], productos_ordenados=[])

    return render_template('index.html', total_registros=0, total_productos=0,
                           productos_con_uom_diferente=[], productos_ordenados=[])

if __name__ == '__main__':
    app.run(debug=True)
