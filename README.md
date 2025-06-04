

# Filtrador de documentos

Este script em Python permite **filtrar páginas de múltiplos arquivos PDF** a partir de palavras-chave fornecidas pelo usuário. As páginas que contêm qualquer das palavras-chave são extraídas (em blocos de até 5 páginas consecutivas) e salvas em novos arquivos PDF. É útil para triagem automática de documentos jurídicos, administrativos ou acadêmicos.

## Funcionalidades

* Seleção interativa de pasta de entrada e saída (usando interface gráfica).
* Busca por uma ou mais palavras-chave (insira separadas por vírgula).
* Processamento de múltiplos PDFs de uma vez.
* Criação de novos PDFs filtrados apenas com páginas relevantes.
* Geração de um arquivo `log.csv` detalhando possíveis erros por arquivo/página.

## Requisitos

* Python 3.8+
* Bibliotecas Python:

  * `PyMuPDF` (fitz)
  * `tkinter`
  * `tqdm`
  * `csv`
  * `re`
  * `os`

Para instalar as dependências, execute:

```bash
pip install pymupdf tqdm
```

> `tkinter`, `csv`, `re` e `os` já fazem parte da biblioteca padrão do Python.

## Como usar

1. **Salve o script** em um arquivo, por exemplo, `pdf_filter.py`.

2. **Execute** no terminal:

   ```bash
   python pdf_filter.py
   ```

3. O programa abrirá janelas para:

   * Selecionar a pasta onde estão os PDFs de entrada.
   * Selecionar a pasta para salvar os PDFs filtrados.
   * Digitar as palavras-chave ou expressões (separadas por vírgula).

4. O processamento mostrará uma barra de progresso.

5. Ao final, os arquivos filtrados estarão na pasta de saída, e um `log.csv` será gerado com eventuais erros.

## Detalhes do Filtro

* A busca por palavras-chave **não diferencia maiúsculas de minúsculas**.
* Cada ocorrência de palavra-chave gera um bloco de até 5 páginas consecutivas, começando pela página encontrada.
* Caso queira extrair um documento maior do que 5 páginas altere end = min(idx + 4#Coloque o número que deseja extrair, doc.page_count - 1)
* Blocos próximos são fundidos para evitar duplicidade.
* Os arquivos filtrados terão o sufixo `_FILTRADO.pdf`.

## Estrutura do Log

O arquivo `log.csv` conterá:

| Arquivo     | Página | Erro        | Detalhes               |
| ----------- | ------ | ----------- | ---------------------- |
| arquivo.pdf | 3      | READ\_ERROR | Detalhe do erro        |
| arquivo.pdf |        | OPEN\_ERROR | Não foi possível abrir |
| ...         | ...    | ...         | ...                    |

## Exemplo de Uso

1. Suponha que você queira buscar por "contrato,cláusula" em todos os PDFs de uma pasta.
2. O script irá extrair páginas onde qualquer dessas palavras aparecer, gerar arquivos filtrados e um log de erros.

## Observações

* O script NÃO altera os arquivos originais.
* Em caso de erro ao abrir, ler ou salvar algum PDF/página, o erro será detalhado no log.
* Ideal para volumes médios de PDFs (pode ser limitado por memória para PDFs muito grandes já testei com PDF's de 40k páginas e funcionou perfeitamente) 


