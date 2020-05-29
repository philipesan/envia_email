import os
from flask import Flask, render_template, request, redirect, url_for, make_response
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


app = Flask(__name__)

api_key = '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'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encerramento')
def encerramento():
    return render_template('encerramento.html')

@app.route('/envio', methods=['POST', 'OPTIONS'])
def envio():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
    elif request.method == "POST":
        dados = request.get_json()
        mensagem = Mail(
        from_email= dados['remetente'],
        to_emails= dados['destinatario'],
        subject= dados['assunto'],
        html_content= dados['mensagem'])
        try:
            sg = SendGridAPIClient(api_key)
            resposta = sg.send(mensagem)
            print(resposta.status_code)
            print(resposta.body)
            print(resposta.headers)
            encerramento()
        except Exception as e:
            print(e)
            return 503

def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(debug=True, port=80)