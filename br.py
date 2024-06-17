import re

# Mapeamento das palavras-chave e funções embutidas
palavras_chave = {
    "imprima": "print",
    "se": "if",
    "senao": "else",
    "ouse": "elif",
    "enquanto": "while",
    "para": "for",
    "em": "in",
    "funcao": "def",
    "retorne": "return",
    "classe": "class",
    "importar": "import",
    "de": "from",
    "como": "as",
    "tente": "try",
    "excecao": "except",
    "finalmente": "finally",
    "levante": "raise",
    "com": "with",
    "passar": "pass",
    "continue": "continue",
    "pare": "break",
    "Verdadeiro": "True",
    "Falso": "False",
    "nada": "None",
    "e": "and",
    "ou": "or",
    "nao": "not",
    "lambda": "lambda",
    "global": "global",
    "nao_local": "nonlocal",
    "assertiva": "assert",
    "deletar": "del",
    "yield": "yield",
    "aguardar": "await",
    "async": "async",
    "naoimplementado": "NotImplemented",
    "__futuro__": "__future__",
    "abra": "open",
    "entrada": "input",
    "somar": "sum",
    "tamanho": "len",
    "mapear": "map",
    "filtrar": "filter",
    "inteiro": "int",
    "flutuante": "float",
    "texto": "str",
    "lista": "list",
    "dicionario": "dict",
    "conjunto": "set",
    "tupla": "tuple",
    "intervalo": "range",
    "zipar": "zip",
    "minimo": "min",
    "maximo": "max",
    "absoluto": "abs",
    "arredondar": "round",
    "ordem": "ord",
    "caractere": "chr",
    "diretorio": "dir",
    "tipo": "type",
    "e_instancia": "isinstance",
    "tem_atributo": "hasattr",
    "obter_atributo": "getattr",
    "definir_atributo": "setattr",
    "enumerar": "enumerate",
    "avaliar": "eval",
    "auto": "self",
    "executar": "exec",
    "super": "super",
    "__inic__": "__init__",
    "__text__": "__str__",
    "__repr__": "__repr__",
    "__tam__": "__len__",
    "__indexitem__": "__getitem__",
    "__defitem__": "__setitem__",
    "__delitem__": "__delitem__",
    "__obter__": "__getattr__",
    "__def__": "__setattr__",
    "__del__": "__delattr__",
    "__chamar__": "__call__",
    "__getattribute__": "__getattribute__",
    "__dir__": "__dir__",
    "__doc__": "__doc__",
    "__classe__": "__class__",
    "__dicionario__": "__dict__",
    "__modulo__": "__module__",
    "__qualname__": "__qualname__",

    # Novas palavras-chave para gestão de dados
    "dataframe": "pd.DataFrame",
    "ler_csv": "pd.read_csv",
    "ler_excel": "pd.read_excel",
    "escrever_csv": "df.to_csv",
    "escrever_excel": "df.to_excel",
    "plotar": "plt.plot",
    "histograma": "plt.hist",
    "barras": "plt.bar",
    "dispersao": "plt.scatter",
    "mostrar_grafico": "plt.show",
    "agrupar_por": "df.groupby",
    "media": "df.mean",
    "mediana": "df.median",
    "desvio_padrao": "df.std",
    "treinar_modelo": "model.fit",
    "prever": "model.predict",
}


# Função para traduzir o código Tupi para Python
def traduzir_codigo(codigo):
    for palavra_pt, palavra_en in palavras_chave.items():
        codigo = re.sub(r'\b' + palavra_pt + r'\b', palavra_en, codigo)
    return codigo