import os
import re
import csv
import fitz
import tkinter as tk
from tkinter import filedialog, simpledialog
from tqdm import tqdm

def escolher_pasta(titulo: str) -> str:
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory(title=titulo)
    root.destroy()
    return path

def pedir_palavras_chave() -> str:
    root = tk.Tk()
    root.withdraw()
    palavras = simpledialog.askstring(
        "Palavras-chave",
        "Digite a(s) palavra(s) ou expressão(ões) para buscar, separadas por vírgula:"
    )
    root.destroy()
    return palavras

def main():
    input_dir = escolher_pasta("Selecione a pasta com os PDFs")
    if not input_dir:
        print("Nenhuma pasta de entrada selecionada. Abortando.")
        return

    output_dir = escolher_pasta("Selecione a pasta de saída para os PDFs filtrados")
    if not output_dir:
        print("Nenhuma pasta de saída selecionada. Abortando.")
        return

    palavras = pedir_palavras_chave()
    if not palavras:
        print("Nenhuma palavra-chave informada. Abortando.")
        return

    # Monta o padrão regex com as palavras informadas
    palavras_lista = [p.strip() for p in palavras.split(",") if p.strip()]
    pattern = re.compile(r"\b(" + "|".join(map(re.escape, palavras_lista)) + r")\b", re.IGNORECASE)

    log_entries = []
    pdf_files = [f for f in sorted(os.listdir(input_dir)) if f.lower().endswith('.pdf') and os.path.isfile(os.path.join(input_dir, f))]

    if not pdf_files:
        print("Nenhum PDF encontrado para processar.")
        return

    for pdf_name in tqdm(pdf_files, desc="Processando PDFs", unit="arquivo"):
        pdf_path = os.path.join(input_dir, pdf_name)
        identifier = os.path.splitext(pdf_name)[0]
        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            log_entries.append([pdf_name, '', 'OPEN_ERROR', str(e)])
            continue

        found_idxs = []
        for page_num in range(doc.page_count):
            try:
                page = doc.load_page(page_num)
                text = page.get_text().replace("\n", " ")
            except Exception as e:
                log_entries.append([pdf_name, page_num + 1, 'READ_ERROR', str(e)])
                continue

            if not text.strip():
                log_entries.append([pdf_name, page_num + 1, 'EMPTY_TEXT', 'Página sem texto extraído'])
                continue

            if pattern.search(text):
                found_idxs.append(page_num)

        if not found_idxs:
            doc.close()
            continue

        blocks = []
        for idx in sorted(found_idxs):
            start = idx
            end = min(idx + 4, doc.page_count - 1)
            blocks.append([start, end])

        merged = []
        for b_start, b_end in sorted(blocks, key=lambda x: x[0]):
            if not merged or b_start > merged[-1][1]:
                merged.append([b_start, b_end])
            else:
                merged[-1][1] = max(merged[-1][1], b_end)

        new_pdf = fitz.open()
        for start, end in merged:
            new_pdf.insert_pdf(doc, from_page=start, to_page=end)

        output_path = os.path.join(output_dir, f"{identifier}_FILTRADO.pdf")
        try:
            new_pdf.save(output_path)
        except Exception as e:
            log_entries.append([pdf_name, '', 'SAVE_ERROR', str(e)])
        finally:
            new_pdf.close()
            doc.close()

    # Log único para todos os PDFs
    log_path = os.path.join(output_dir, 'log.csv')
    with open(log_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Arquivo', 'Página', 'Erro', 'Detalhes'])
        writer.writerows(log_entries)

    print(f"Processamento concluído. PDFs filtrados em: {output_dir}")
    print(f"Log de erros em: {log_path}")

if __name__ == '__main__':
    main()