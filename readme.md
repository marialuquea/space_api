# CENTRO DIAGONAL QUIRURGICO API

Este API recibe valores de piel y envia valores de laser. 

### Instrucciones to run locally

1. Crear un environment `conda create -n cdq_api`
1. Activar el environment `conda activate cdq_api`
1. Install dependencies: `pip install -r requirements.txt`
1. `flask run -p 8000`
1. Descargar [Postman Desktop](https://www.postman.com/downloads/)
1. Hacer un GET: `http://127.0.0.1:5000/ping` y ver un `pong`
1. Hacer un GET: `http://127.0.0.1:5000/laser` y ver un `yes this works`
1. Hacer un POST: `http://127.0.0.1:5000/laser?zona=CARA&edad=20-30&fototipo=1&lentigos=1&melasma=1&pecas=1&purpura=1&telangiectasias=1&laxitud=1&elastosis=1&cicatrices_acne=1&quistes_miliares=1&arrugas_superficiales=1&arrugas_cruzadas=1&arrugas_profundas=1&atrofia_grasa=1&surcos_nasogenianos=1&poros=1`