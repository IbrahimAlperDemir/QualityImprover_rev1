from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from datetime import datetime

def save_to_docx(text: str, filename: str = "Gereksinim_Dokumani.docx", doc_type: str = "PRD", revision: str = "A") -> None:
    doc = Document()

    # 🧾 Sabit Üst Bilgiler (Sayfa Başlığı Şeklinde)
    header = doc.sections[0].header
    header_paragraph = header.paragraphs[0]
    header_paragraph.text = f"FRM-{doc_type}-{revision} | Ürün Gereksinim Dokümanı | {datetime.today().strftime('%d.%m.%Y')}"
    header_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    header_paragraph.runs[0].font.size = Pt(9)

    # 📄 Başlık
    title = doc.add_heading("Ürün Özellik Gereksinim Dokümanı", level=1)
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    doc.add_paragraph()  # boşluk

    # 📋 İçerik
    for line in text.splitlines():
        if line.strip() == "":
            doc.add_paragraph()
        elif line.strip().endswith(":") or line.strip().startswith("1.") or line.strip().startswith("###"):
            para = doc.add_paragraph()
            run = para.add_run(line.strip())
            run.bold = True
            run.font.size = Pt(12)
        else:
            doc.add_paragraph(line.strip())

    doc.save(filename)
    print(f"✅ '{filename}' başarıyla kaydedildi.")
