# rotas

from app import app, db
from flask import render_template, url_for, request

from app.models import Contato

from app.forms import ContatoForm

@app.route("/")
def homepage():
    context = {
        'user': 'gabriellll',
        'idade': 20
    }
    return render_template("index.html", context=context)

# Formato não recomendado
@app.route("/contatos_old", methods=['GET', 'POST'])
def contatos_old():
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
@app.route("/contatos", methods=['GET', 'POST'])
def contatos():
    form =  ContatoForm()
    context = {}
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
    return render_template("contato.html", context=context, form=form)
