import tkinter as tk

def acao_botao():
    print("Botão clicado!")

janela = tk.Tk()
janela.title("Interface Simples")

rotulo = tk.Label(janela, text="Bem-vindo ao Tkinter!", font=("Arial", 16))
rotulo.pack()

botao = tk.Button(janela, text="Clique aqui", command=acao_botao)
botao.pack()

entrada = tk.Entry(janela)
entrada.pack()

menu = tk.Menu(janela)
janela.config(menu=menu)

submenu = tk.Menu(menu)
menu.add_cascade(label="Arquivo", menu=submenu)
submenu.add_command(label="Sair", command=janela.quit)

janela.mainloop()
