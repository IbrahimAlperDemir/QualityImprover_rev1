from tinydb import TinyDB, Query
from datetime import datetime

db = TinyDB("form_counter_db.json")
counter_table = db.table("form_counters")
history_table = db.table("form_history")

def get_next_form_number(doc_type="PRD", revision="A"):
    Form = Query()
    result = counter_table.get(Form.type == doc_type)

    if result:
        current = result["count"] + 1
        counter_table.update({"count": current}, Form.type == doc_type)
    else:
        current = 1
        counter_table.insert({"type": doc_type, "count": current})

    code = f"FRM-{doc_type}-{current:03d}-{revision}"

    # Geçmişe kayıt et
    history_table.insert({
        "form_code": code,
        "type": doc_type,
        "revision": revision,
        "date": datetime.today().strftime("%Y-%m-%d %H:%M"),
        "filename": f"{code}.docx"
    })

    return code

def get_form_history():
    return history_table.all()
