# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template_string
import csv
import time
import threading
import subprocess

CSV_FILE = "historico.csv"

def ler_historico():
    historico = []
    try:
        with open(CSV_FILE, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 3:
                    historico.append({
                        "timestamp": row[0],
                        "temperatura": float(row[1]),
                        "umidade": float(row[2])
                    })
    except FileNotFoundError:
        return []
    return historico

def executar_leitura():
    while True:
        subprocess.run(["./dht11_read"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Executa o binário
        time.sleep(10)  # Aguarda 10 segundos antes de uma nova leitura

app = Flask(__name__)

@app.route("/dados", methods=["GET"])
def dados():
    historico = ler_historico()
    template = """
    <!DOCTYPE html>
    <html lang='pt'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>Histórico de Leitura</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
            table {
                width: 80%;
                margin: auto;
                border-collapse: collapse;
                background: white;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            th, td {
                padding: 10px;
                border: 1px solid #ddd;
            }
            th {
                background: #007BFF;
                color: white;
            }
        </style>
    </head>
    <body>
        <h1>Histórico de Temperatura e Umidade</h1>
        <table>
            <tr>
                <th>Data e Hora</th>
                <th>Temperatura (°C)</th>
                <th>Umidade (%)</th>
            </tr>
            {% for dado in historico %}
            <tr>
                <td>{{ dado.timestamp }}</td>
                <td>{{ dado.temperatura }}</td>
                <td>{{ dado.umidade }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(template, historico=historico)

if __name__ == "__main__":
    threading.Thread(target=executar_leitura, daemon=True).start()
    app.run(host="0.0.0.0", port=8080, debug=True)
