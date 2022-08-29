import os
import shutil

from docxtpl import DocxTemplate


class SMGSDOCX:

    @classmethod
    def create_docx(cls, smgs_data: dict, train_name: str, store_path: str):
        if not os.path.isdir(store_path + train_name):
            path = os.path.join(store_path, train_name)
            os.mkdir(path)
            draft_path = os.path.join(path, 'draft')
            original_path = os.path.join(path, 'original')
            os.mkdir(draft_path)
            os.mkdir(original_path)
        smgs_draft_template = DocxTemplate('static/smgs_draft.docx')
        smgs_original_template = DocxTemplate('static/smgs_original.docx')
        draft_path = store_path + f"{train_name}/draft/" + train_name + "_" + smgs_data['container'] + ".docx"
        original_path = store_path + f"{train_name}/original/" + train_name + "_" + smgs_data['container'] + ".docx"
        smgs_draft_template.render(smgs_data)
        smgs_original_template.render(smgs_data)
        smgs_draft_template.save(draft_path)
        smgs_original_template.save(original_path)
        return str(draft_path).replace('app/', ''), str(original_path).replace('app/', '')



