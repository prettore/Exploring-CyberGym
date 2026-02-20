# rotas

from app import app, db
from flask import render_template, url_for, request, redirect, session
from markupsafe import escape

import subprocess
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(BASE_DIR, "scripts", "parser.py")

@app.route("/", methods=["GET", "POST"])
def homepage():

    context = {}

    print(request.method)

    if request.method == "POST":
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True
        )
        session["output"] = result.stdout.strip()
        return redirect(url_for("homepage"))

    output = session.pop("output", None)
    return render_template("index.html", context=context, output=output)

'''
# Formato não recomendado
@app.route("/contato_old", methods=['GET', 'POST'])
def contato_old():
    context = {}
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa')
        context.update({'pesquisa': pesquisa})
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        assunto = request.form['assunto']
        mensagem = request.form['mensagem']

        contato = Contato(
            nome=nome,
            email=email,
            assunto=assunto,
            mensagem=mensagem
        )

        db.session.add(contato)
        db.session.commit()
    return render_template("contato_old.html", context=context)

# Formato recomendado
@app.route("/contato", methods=['GET', 'POST'])
def contato():
    form =  ContatoForm()
    context = {}
    if form.validate_on_submit():
        form.save()
        return redirect(url_for("homepage"))

    return render_template("contato.html", context=context, form=form)

@app.route("/contato/lista")
def contatoLista():

    if request.method == "GET":
        pesquisa = request.args.get('pesquisa', '')

    dados = Contato.query.order_by('nome')
    if pesquisa != '':
        dados = dados.filter_by(nome=pesquisa)

    print(dados)

    context = {'dados': dados.all()}

    return render_template("contato_lista.html", context=context)
'''