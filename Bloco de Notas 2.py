import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText


class BlocoDeNotas:
    def __init__(self, root):
        self.root = root
        self.root.title("Bloco de Notas")
        self.root.geometry("800x600")
        
        # Variáveis para o zoom
        self.fonte_atual = 12
        
        # Adicionando o menu
        self.menu = tk.Menu(root)
        self.root.config(menu=self.menu)
        
        # Menus de Arquivo
        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Arquivo", menu=self.file_menu)
        self.file_menu.add_command(label="Novo", command=self.novo_arquivo)
        self.file_menu.add_command(label="Abrir...", command=self.abrir_arquivo)
        self.file_menu.add_command(label="Salvar", command=self.salvar_arquivo)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Sair", command=root.quit)
        
        # Menu Editar
        self.edit_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Editar", menu=self.edit_menu)
        self.edit_menu.add_command(label="Localizar...", command=self.localizar_palavra)

        # Menu Exibir
        self.view_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Exibir", menu=self.view_menu)
        self.view_menu.add_command(label="Zoom In", command=self.zoom_in)
        self.view_menu.add_command(label="Zoom Out", command=self.zoom_out)

        # Menu Sobre
        self.about_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Sobre", menu=self.about_menu)
        self.about_menu.add_command(label="Sobre o Bloco de Notas", command=self.mostrar_sobre)

        # Área de texto com barra de rolagem
        self.text_area = ScrolledText(root, wrap=tk.WORD, font=("Segoe UI", self.fonte_atual))
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.text_area.bind("<KeyRelease>", self.atualizar_status)
        self.text_area.bind("<ButtonRelease>", self.atualizar_status)
        
        # Vincular o Ctrl+Scroll para o zoom
        self.text_area.bind("<Control-MouseWheel>", self.zoom_scroll)
        
        # Barra de status
        self.status_bar = tk.Label(root, text="Linhas: 1 | Colunas: 1 | 0 caracteres", anchor="w")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Caminho do arquivo
        self.caminho_arquivo = None

    def atualizar_status(self, event=None):
        # Contagem de caracteres
        texto = self.text_area.get(1.0, tk.END)
        num_caracteres = len(texto) - 1  # Remove o último caractere '\n'

        # Linha e coluna do cursor
        posicao_cursor = self.text_area.index(tk.INSERT)  # Posição do cursor no formato "linha.coluna"
        linha, coluna = posicao_cursor.split(".")
        linha = int(linha)
        coluna = int(coluna) + 1  # Ajustar para 1-based

        # Atualiza a barra de status
        self.status_bar.config(text=f"Linhas: {linha} | Colunas: {coluna} | {num_caracteres} caracteres")

    def novo_arquivo(self):
        self.text_area.delete(1.0, tk.END)
        self.caminho_arquivo = None
        self.root.title("Bloco de Notas")
        self.atualizar_status()

    def abrir_arquivo(self):
        caminho = filedialog.askopenfilename(filetypes=[("Todos os arquivos", "*.*"), ("Arquivos de texto", "*.txt")])
        if caminho:
            try:
                with open(caminho, "r", encoding="utf-8") as arquivo:
                    conteudo = arquivo.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, conteudo)
                self.caminho_arquivo = caminho
                self.root.title(f"Bloco de Notas - {caminho}")
                self.atualizar_status()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir o arquivo:\n{e}")

    def salvar_arquivo(self):
        if self.caminho_arquivo:
            try:
                with open(self.caminho_arquivo, "w", encoding="utf-8") as arquivo:
                    conteudo = self.text_area.get(1.0, tk.END).strip()
                    arquivo.write(conteudo)
                messagebox.showinfo("Salvar", "Arquivo salvo com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível salvar o arquivo:\n{e}")
        else:
            self.salvar_como()

    def salvar_como(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")])
        if caminho:
            try:
                with open(caminho, "w", encoding="utf-8") as arquivo:
                    conteudo = self.text_area.get(1.0, tk.END).strip()
                    arquivo.write(conteudo)
                self.caminho_arquivo = caminho
                self.root.title(f"Bloco de Notas - {caminho}")
                messagebox.showinfo("Salvar", "Arquivo salvo com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível salvar o arquivo:\n{e}")

    def localizar_palavra(self):
        palavra = simpledialog.askstring("Localizar", "Digite a palavra:")
        if palavra:
            self.text_area.tag_remove("highlight", 1.0, tk.END)
            texto = self.text_area.get(1.0, tk.END)
            inicio = 1.0
            while True:
                inicio = self.text_area.search(palavra, inicio, stopindex=tk.END, nocase=True)
                if not inicio:
                    break
                fim = f"{inicio}+{len(palavra)}c"
                self.text_area.tag_add("highlight", inicio, fim)
                inicio = fim
            self.text_area.tag_config("highlight", background="blue", foreground="white")

    def zoom_in(self):
        self.fonte_atual += 2
        self.text_area.config(font=("Segoe UI", self.fonte_atual))

    def zoom_out(self):
        if self.fonte_atual > 8:
            self.fonte_atual -= 2
            self.text_area.config(font=("Segoe UI", self.fonte_atual))

    def zoom_scroll(self, event):
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def mostrar_sobre(self):
        mensagem = (
            "Esse bloco de notas foi desenvolvido totalmente em Python no dia 7 de janeiro de 2025 "
            "por Luan da Silva Ramalho, um jovem super nerd, formado em ciência da computação, pela Unicarioca, "
            "Centro Universitário mais conceituado da cidade do Rio de Janeiro, que gosta muito de programação "
            "e desenvolvimento de softwares."
        )
        messagebox.showinfo("Sobre", mensagem)


# Executa o programa
if __name__ == "__main__":
    root = tk.Tk()
    app = BlocoDeNotas(root)
    root.mainloop()
