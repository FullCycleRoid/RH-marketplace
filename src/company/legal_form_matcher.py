RU_TO_EN_LEGAL_FORM = {
    "Общество с ограниченной ответственностью": {"full": "Limited Liability Company", "abbr": ["LLC", "Ltd"]},
    "Акционерное общество": {"full": "Joint Stock Company", "abbr": ["JSC", "PLC"]},
    "Публичное акционерное общество": {"full": "Public Joint Stock Company", "abbr": ["PJSC"]},
    "Коммандитное товарищество": {"full": "Limited Partnership", "abbr": ["LP"]},
    "Полное товарищество": {"full": "General Partnership", "abbr": ["GP"]},
    "Товарищество на вере": {"full": "Partnership with Limited Liability", "abbr": ["LLP"]},
    "Государственное унитарное предприятие": {"full": "State Unitary Enterprise", "abbr": ["SUE"]},
    "Муниципальное унитарное предприятие": {"full": "Municipal Unitary Enterprise", "abbr": ["MUE"]},
    "Хозяйственное товарищество": {"full": "Business Partnership", "abbr": []},
    "Кооператив": {"full": "Cooperative", "abbr": ["Co-op"]},
    "Некоммерческое партнерство": {"full": "Non-Commercial Partnership", "abbr": ["NCP"]},
    "Фонд": {"full": "Foundation", "abbr": []},
    "Ассоциация": {"full": "Association", "abbr": []},
    "Союз": {"full": "Union", "abbr": []},
    "Индивидуальный предприниматель": {"full": "Individual Entrepreneur", "abbr": ["IE", "Sole Proprietor"]}
}

EN_TO_RU_LEGAL_FORM = {
    "Limited Liability Company": {"ru": "Общество с ограниченной ответственностью", "abbr": ["LLC", "Ltd"]},
    "Joint Stock Company": {"ru": "Акционерное общество", "abbr": ["JSC", "PLC"]},
    "Public Joint Stock Company": {"ru": "Публичное акционерное общество", "abbr": ["PJSC"]},
    "Limited Partnership": {"ru": "Коммандитное товарищество", "abbr": ["LP"]},
    "General Partnership": {"ru": "Полное товарищество", "abbr": ["GP"]},
    "Partnership with Limited Liability": {"ru": "Товарищество на вере", "abbr": ["LLP"]},
    "State Unitary Enterprise": {"ru": "Государственное унитарное предприятие", "abbr": ["SUE"]},
    "Municipal Unitary Enterprise": {"ru": "Муниципальное унитарное предприятие", "abbr": ["MUE"]},
    "Business Partnership": {"ru": "Хозяйственное товарищество", "abbr": []},
    "Cooperative": {"ru": "Кооператив", "abbr": ["Co-op"]},
    "Non-Commercial Partnership": {"ru": "Некоммерческое партнерство", "abbr": ["NCP"]},
    "Foundation": {"ru": "Фонд", "abbr": []},
    "Association": {"ru": "Ассоциация", "abbr": []},
    "Union": {"ru": "Союз", "abbr": []},
    "Individual Entrepreneur": {"ru": "Индивидуальный предприниматель", "abbr": ["IE", "Sole Proprietor"]}
}

def find_by_abbr(abbr):
    for key, value in RU_TO_EN_LEGAL_FORM.items():
        if abbr in value['abbr']:
            return key, value['full']
    for key, value in EN_TO_RU_LEGAL_FORM.items():
        if abbr in value['abbr']:
            return value['ru'], key
    return None
