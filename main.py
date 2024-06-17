import tkinter as tk
from tkinter import filedialog, font, messagebox
import re
from br import traduzir_codigo, palavras_chave


def escolher_arquivo():
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivo Tupi", "*.tupi"), ("Todos os Arquivos", "*.*")])
    if caminho_arquivo:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            codigo_tupi = arquivo.read()
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, codigo_tupi)
        aplicar_coloracao()

def aplicar_coloracao(event=None):
    texto = text_area.get(1.0, tk.END)
    text_area.tag_remove("palavra_chave", "1.0", tk.END)
    text_area.tag_remove("string", "1.0", tk.END)
    text_area.tag_remove("numero", "1.0", tk.END)
    text_area.tag_remove("comentario", "1.0", tk.END)

    for palavra_pt, palavra_en in palavras_chave.items():
        padrao = r'\b' + re.escape(palavra_pt) + r'\b'
        for match in re.finditer(padrao, texto):
            inicio = match.start()
            fim = match.end()
            text_area.tag_add("palavra_chave", f"1.0 + {inicio}c", f"1.0 + {fim}c")

    padrao_string = r'"(.*?)"'
    for match in re.finditer(padrao_string, texto):
        inicio = match.start()
        fim = match.end()
        text_area.tag_add("string", f"1.0 + {inicio}c", f"1.0 + {fim}c")

    padrao_numero = r'\b\d+\b'
    for match in re.finditer(padrao_numero, texto):
        inicio = match.start()
        fim = match.end()
        text_area.tag_add("numero", f"1.0 + {inicio}c", f"1.0 + {fim}c")

    padrao_comentario = r'#.*'
    for match in re.finditer(padrao_comentario, texto):
        inicio = match.start()
        fim = match.end()
        text_area.tag_add("comentario", f"1.0 + {inicio}c", f"1.0 + {fim}c")

    text_area.tag_configure("palavra_chave", foreground="#FFD700", font=("Courier New", 12, "bold"))
    text_area.tag_configure("string", foreground="#98C379")
    text_area.tag_configure("numero", foreground="#D19A66")
    text_area.tag_configure("comentario", foreground="#5C6370")

def configurar_tags():
    aplicar_coloracao()

def executar_codigo(event=None):
    codigo_tupi = text_area.get(1.0, tk.END)
    codigo_python = traduzir_codigo(codigo_tupi)
    saida_texto.config(state=tk.NORMAL)
    saida_texto.delete(1.0, tk.END)
    try:
        exec(codigo_python, {'print': print_saida})
    except Exception as e:
        print_saida(f"Erro: {e}")
    saida_texto.config(state=tk.DISABLED)

def print_saida(*args, **kwargs):
    saida_texto.config(state=tk.NORMAL)
    saida_texto.insert(tk.END, ' '.join(map(str, args)) + '\n')
    saida_texto.config(state=tk.DISABLED)
    saida_texto.see(tk.END)

def salvar_arquivo():
    codigo_tupi = text_area.get(1.0, tk.END)
    caminho_arquivo = filedialog.asksaveasfilename(defaultextension=".tupi", filetypes=[("Arquivo Tupi", "*.tupi")])
    if caminho_arquivo:
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(codigo_tupi)
        messagebox.showinfo("Sucesso", "Código salvo com sucesso!")

def criar_interface():
    global text_area, saida_texto

    janela = tk.Tk()
    janela.title("Tupi")
    janela.configure(bg='#282828')  # Cinza escuro para um tema dark suave

    frame_botoes = tk.Frame(janela, bg='#282828', padx=10, pady=5)  # Adicionando margens internas
    frame_botoes.pack(side=tk.TOP, fill=tk.X)

    btn_documentacao = tk.Button(frame_botoes, text="Documentação", bg='#282828', fg='white', font=('Helvetica', 10, 'bold'), bd=0)  # bd=0 para remover a borda
    btn_documentacao.pack(side=tk.LEFT, padx=5)

    btn_escolher_codigo = tk.Button(frame_botoes, text="Escolher Código", command=escolher_arquivo, bg='#282828', fg='white', font=('Helvetica', 10, 'bold'), bd=0)
    btn_escolher_codigo.pack(side=tk.LEFT, padx=5)

    btn_executar_codigo = tk.Button(frame_botoes, text="Executar Código", command=executar_codigo, bg='#282828', fg='white', font=('Helvetica', 10, 'bold'), bd=0)
    btn_executar_codigo.pack(side=tk.LEFT, padx=5)

    btn_salvar_codigo = tk.Button(frame_botoes, text="Salvar Código", command=salvar_arquivo, bg='#282828', fg='white', font=('Helvetica', 10, 'bold'), bd=0)
    btn_salvar_codigo.pack(side=tk.LEFT, padx=5)

    frame_texto = tk.Frame(janela, bg='#282828')
    frame_texto.pack(expand=tk.YES, fill=tk.BOTH)

    # Widget para números de linha
    linha_numero = tk.Text(frame_texto, width=4, padx=3, bg='#1E1E1E', fg='#6B6B6B', font=('Courier New', 12), wrap=tk.NONE)
    linha_numero.pack(side=tk.LEFT, fill=tk.Y)

    text_area = tk.Text(frame_texto, wrap=tk.WORD, bg='#282828', fg='white', insertbackground='white', font=('Courier New', 12))
    text_area.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
    text_area.bind("<KeyRelease>", aplicar_coloracao)

    scrollbar = tk.Scrollbar(frame_texto, command=text_area.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_area.config(yscrollcommand=lambda *args: sync_scrollbar(args, linha_numero))
    linha_numero.config(yscrollcommand=lambda *args: sync_scrollbar(args, text_area))

    frame_saida = tk.Frame(janela, bg='#282828')
    frame_saida.pack(expand=tk.YES, fill=tk.BOTH)

    saida_texto = tk.Text(frame_saida, wrap=tk.WORD, bg='#282828', fg='white', insertbackground='white', font=('Courier New', 12), state=tk.DISABLED)
    saida_texto.pack(expand=tk.YES, fill=tk.BOTH)

    configurar_tags()

    # Sincronizar a rolagem entre text_area e linha_numero
    text_area.config(yscrollcommand=lambda *args: sync_scrollbar(args, linha_numero))
    linha_numero.config(yscrollcommand=lambda *args: sync_scrollbar(args, text_area))

    janela.mainloop()

def sync_scrollbar(command, widget):
    if command[0] == 'moveto':
        widget.yview_moveto(command[1])
    elif command[0] == 'scroll':
        widget.yview_scroll(command[1], command[2])


if __name__ == "__main__":
    criar_interface()
