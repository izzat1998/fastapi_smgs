from docxtpl import DocxTemplate


class SMGSDOCX:

    @classmethod
    def create_docx(cls, smgs_data: dict, train_name: str, store_path: str):
        smgs_draft_template = DocxTemplate('static/smgs_draft.docx')
        smgs_original_template = DocxTemplate('static/smgs_original.docx')
        draft_path = store_path + "draft/" + train_name + "_" + smgs_data['container'] + ".docx"
        original_path = store_path + "original/" + train_name + "_" + smgs_data['container'] + ".docx"
        smgs_draft_template.render(smgs_data)
        smgs_original_template.render(smgs_data)
        smgs_draft_template.save(draft_path)
        smgs_original_template.save(original_path)
        return str(draft_path).replace('app/', ''), str(original_path).replace('app/', '')
