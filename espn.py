from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from flask import Flask, render_template, request, redirect, url_for

from flask import Flask, render_template, request
app = Flask(__name__)


def abrir_espn():
    options = Options()
    driver = webdriver.Chrome(options=options)

    driver.set_window_position(1040,1090)
    driver.get('https://www.espn.com.br')
    driver.refresh()

    wait = WebDriverWait(driver, 50)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="global-search-trigger"]')))

    buscar = driver.find_element(By.XPATH, '//*[@id="global-search-trigger"]')
    buscar.click()

    with open('nome.txt', 'r') as f:
        player1 = f.read()
        search = driver.find_element(By.XPATH, '//*[@id="global-search-input"]')
        search.send_keys(player1)

    time.sleep(0.3)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="global-search"]/div/input[2]')))

    lupa = driver.find_element(By.XPATH, '//*[@id="global-search"]/div/input[2]')
    lupa.click()

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.player__Results__Item')))

    player = driver.find_element(By.CSS_SELECTOR, 'li.player__Results__Item')
    player.click()

    wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Ficha dos jogos')))

    gamelog = driver.find_element(By.LINK_TEXT, 'Ficha dos jogos')
    gamelog.click()

    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[1]/div[1]/div/div[2]/div[3]/div/div/div/div/div[2]/table/tbody')))

    elemento = driver.find_element(By.XPATH, '//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[1]/div[1]/div/div[2]/div[2]/div/div/div/div/div[2]/table/tbody')
    valor = elemento.text
    valor = valor.split()

    driver.execute_script("window.scrollBy(0, 550);")
    time.sleep(1)
    driver.quit()

    sub_listas = [valor[i:i+20] for i in range(0, len(valor),20)]

    stats_formatadas = []
    
    for x in sub_listas:
        lista_temporaria = []
        lista_temporaria.append(str(x[0]) + " " + str(x[1]))
        lista_temporaria.append(str(x[2]) + " " + str(x[3]))
        lista_temporaria.append(str(x[4]) + " " + str(x[5]))
        for i in range(6, min(20, len(x))):  # verifica se x tem pelo menos 20 elementos
            lista_temporaria.append(x[i])
        stats_formatadas.append(lista_temporaria)

    stats_formatadas.pop()

    print(stats_formatadas)
    return stats_formatadas

@app.route('/')
def just():
    return render_template('just.html')
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    with open(f'nome.txt', 'w') as f:
        f.write(name)
    stats_formatadas = abrir_espn()  # Armazene o retorno de abrir_espn() em uma variável

    html_inicio = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>P&aacute;gina de Estat&iacute;sticas</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='design_pag2.css') }}">
    </head>
    <body>
    """

    html_fim = """
    </body>
    </html>
    """

    cabecalho = ["DATE", "ADV", "RESULTADO", "MIN", "FG", "FG%", "3PT", "3P%", "FT", "FT%", "REB", "V", "BLK", "STL", "PF", "TO", "PTS"]

    html_corpo = "<table><tr>"
    for item in cabecalho:
        html_corpo += '<th>'+ str(item) + "</th>"
    html_corpo += "</tr>"

    for lista in stats_formatadas:
        html_corpo += "<tr>"
        for item in lista:
            html_corpo += '<td>'+ str(item) + "</td>"
        html_corpo += "</tr>"
    html_corpo += "</table>"

    html_completo = html_inicio + html_corpo + html_fim

    with open('templates/html_completo.html', 'w', encoding='utf-8', errors='ignore') as f:
        f.write(html_completo)
    return render_template('html_completo.html')

if __name__ == '__main__':
    app.run(debug=True)