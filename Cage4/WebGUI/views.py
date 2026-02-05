from main import *

# rotas
@app.route("/")
def homepage():
    return "Meu flask"

@app.route("/blog")
def blog():
    return "Bem vindo ao blog"
