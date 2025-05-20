import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

class ConversorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Converter arquivos")
        self.root.geometry("500x500")

        # Dicionário de funções de conversão
        self.conversores = {
            ('.csv', '.json'): self.converter_csv_para_json,
            ('.csv', '.xlsx'): self.converter_csv_para_xlsx,
            ('.xlsx', '.json'): self.converter_xlsx_para_json,
            ('.xlsx', '.csv'): self.converter_xlsx_para_csv,
            ('.json', '.csv'): self.converter_json_para_csv,
            ('.json', '.xlsx'): self.converter_json_para_xlsx,
        }

        # Tipos de conversões suportadas para exibição
        self.type_conversores = {
            '.png': ['.pdf', '.jpg'],
            '.jpg': ['.png', '.pdf'],
            '.csv': ['.xlsx', '.json'],
            '.xlsx': ['.csv', '.json'],
            '.json': ['.csv', '.xlsx']
        }

        self.option_selected = tk.StringVar()
        self.caminho = None
        self.opcoes_validas = []

        # Frame de opções
        self.frame_radios = tk.Frame(self.root)
        self.frame_radios.pack(pady=10)

        self.label_formatos = tk.Label(self.frame_radios, text='Selecione uma opção para converter')
        self.label_formatos.pack(anchor='w', padx=10)

        self.label_arquivo = tk.Label(self.root, text="")
        self.label_arquivo.pack(pady=5)

        self.botao_selecionar = tk.Button(self.root, text="Selecione um arquivo", command=self.selecionar_arquivo)
        self.botao_selecionar.pack(pady=20)

        self.botao_confirmar = tk.Button(self.root, text="Converter", command=self.converter_arquivo, state='disabled')
        self.botao_confirmar.pack(pady=10)

        self.option_selected.trace('w', self.atualiza_estado_botao)

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecione um arquivo",
            filetypes=[("Todos os arquivos suportados", "*.docx *.pdf *.png *.jpg *.csv *.xlsx *.json")]
        )

        if not caminho:
            messagebox.showwarning('Aviso', 'Selecione um arquivo válido para continuar a conversão')
            return

        self.caminho = caminho
        extensao = os.path.splitext(caminho)[1].lower()

        for widget in self.frame_radios.winfo_children():
            if isinstance(widget, ttk.Radiobutton):
                widget.destroy()

        self.opcoes_validas = self.type_conversores.get(extensao, [])

        if not self.opcoes_validas:
            messagebox.showwarning('Aviso', f'Conversão não suportada para o tipo {extensao}')
            self.label_arquivo.config(text="")
            self.botao_confirmar.config(state='disabled')
            return

        for opcao in self.opcoes_validas:
            ttk.Radiobutton(self.frame_radios, text=opcao, value=opcao, variable=self.option_selected).pack(anchor='w', padx=10)

        nome_arquivo = os.path.basename(caminho)
        self.label_arquivo.config(text=f"Arquivo selecionado: {nome_arquivo}")
        self.botao_confirmar.config(state='disabled')
        self.option_selected.set('')

    def atualiza_estado_botao(self, *args):
        if self.caminho and self.option_selected.get() in self.opcoes_validas:
            self.botao_confirmar.config(state='normal')
        else:
            self.botao_confirmar.config(state='disabled')

    def converter_arquivo(self):
        escolhido = self.option_selected.get()
        if escolhido not in self.opcoes_validas:
            messagebox.showwarning("Aviso", "Selecione uma opção de conversão válida.")
            return

        try:
            origem = os.path.splitext(self.caminho)[1].lower()
            destino = escolhido

            funcao = self.conversores.get((origem, destino))

            if funcao:
                novo_caminho = funcao()
                messagebox.showinfo("Sucesso", f"Arquivo convertido para {destino} em:\n{novo_caminho}")
            else:
                messagebox.showwarning("Aviso", f"Conversão de {origem} para {destino} não está implementada ainda.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao converter: {str(e)}")

    # ===== Métodos de conversão =====

    def converter_csv_para_json(self):
        df = pd.read_csv(self.caminho)
        novo_caminho = os.path.splitext(self.caminho)[0] + '.json'
        df.to_json(novo_caminho, orient='records', indent=4)
        return novo_caminho

    def converter_csv_para_xlsx(self):
        df = pd.read_csv(self.caminho)
        novo_caminho = os.path.splitext(self.caminho)[0] + '.xlsx'
        df.to_excel(novo_caminho, index=False)
        return novo_caminho

    def converter_xlsx_para_json(self):
        df = pd.read_excel(self.caminho)
        novo_caminho = os.path.splitext(self.caminho)[0] + '.json'
        df.to_json(novo_caminho, orient='records', indent=4)
        return novo_caminho

    def converter_xlsx_para_csv(self):
        df = pd.read_excel(self.caminho)
        novo_caminho = os.path.splitext(self.caminho)[0] + '.csv'
        df.to_csv(novo_caminho, index=False)
        return novo_caminho

    def converter_json_para_csv(self):
        df = pd.read_json(self.caminho)
        novo_caminho = os.path.splitext(self.caminho)[0] + '.csv'
        df.to_csv(novo_caminho, index=False)
        return novo_caminho

    def converter_json_para_xlsx(self):
        df = pd.read_json(self.caminho)
        novo_caminho = os.path.splitext(self.caminho)[0] + '.xlsx'
        df.to_excel(novo_caminho, index=False)
        return novo_caminho

if __name__ == "__main__":
    root = tk.Tk()
    app = ConversorApp(root)
    root.mainloop()
