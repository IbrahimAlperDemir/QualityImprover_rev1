import streamlit as st
from generator import generate_requirements
from save_to_docx import save_to_docx
from form_tracker import get_form_history

st.set_page_config(page_title="Gereksinim Dokümanı Oluşturucu", layout="centered")

st.title("Gereksinim Dokümanı Oluşturucu")

st.markdown("Aşağıdaki alanları doldurarak profesyonel bir ürün gereksinim dokümanı oluşturabilirsiniz:")

with st.expander("📚 Oluşturulmuş Form Geçmişi"):
    history = get_form_history()
    if history:
        for item in history[::-1]:  # En son kayıt en üstte
            st.markdown(f"🧾 **{item['form_code']}** ({item['type']}) — {item['date']} — `{item['filename']}`")
    else:
        st.info("Henüz oluşturulmuş form kaydı bulunmuyor.")

with st.form("feature_form"):
    doc_type = st.selectbox("Form Türü", ["PRD", "TEST", "QMS"], index=0)
    revision = st.text_input("Revizyon", value="A")

    name = st.text_input("1. Özellik Adı")
    purpose = st.text_area("2. Bu özellik ne işe yarar? (Amaç)")
    how_it_works = st.text_area("3. Nasıl çalışır?")
    user_facing = st.text_area("4. Kullanıcıya ne gösterilir?")
    not_expected = st.text_area("5. Ne olmamalı?")
    constraints = st.text_area("6. Donanım / Yazılım kısıtları")
    acceptance = st.text_area("7. Kabul kriteri / test senaryosu")

    submitted = st.form_submit_button("📄 Dokümanı Oluştur")

if submitted:
    with st.spinner("Gereksinim dokümanı oluşturuluyor..."):
        data = {
            "name": name,
            "purpose": purpose,
            "how_it_works": how_it_works,
            "user_facing": user_facing,
            "not_expected": not_expected,
            "constraints": constraints,
            "acceptance": acceptance,
            "doc_type": doc_type,
            "revision": revision
        }
        doc_text = generate_requirements(data)
        filename = "Gereksinim_Dokumani.docx"
        save_to_docx(doc_text, filename, doc_type=doc_type, revision=revision)
        with open(filename, "rb") as file:
            st.success("📄 Doküman hazır!")
            st.download_button(
                label="📥 DOCX olarak indir",
                data=file,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
