import tkinter as tk #importa o módulo tkinter, que é o principio para o front(interface)

janela = tk.Tk() #instacia da classe tkinter
janela.title("Exemplo 1") #titulo da janela
janela.geometry("300x300") #tamanho da janela

def clicar():
    label.config(text='Você clicou no botão') #config da variavel label. conde configura o texto

label = tk.Label(janela, text='Olá mundo') #Cria uma label dentro da variavel
label.pack(pady=100) #é o espaço entre o rotulo e o widget(botao)

botao = tk.Button(janela, text='Clique aqui', command=clicar) #Inseri um botão na tela, passando a variavel da tela, o texto do botao, e o comando que o botao realiza
botao.pack() #ajusta a posição do botao na tela

janela.mainloop() #inicia e mantem o loop da tela, onde os cliques da tela ficam ativos, sem isso a janela iria abrir e fechar instantaneamente