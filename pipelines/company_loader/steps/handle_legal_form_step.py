from pipelines.generic_pipeline import Context, NextStep


ru_to_en = {
    "ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ": {"full": "LIMITED LIABILITY COMPANY", "abbr": ["LLC", "LTD"]},
    "АКЦИОНЕРНОЕ ОБЩЕСТВО": {"full": "JOINT STOCK COMPANY", "abbr": ["JSC", "PLC"]},
    "ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО": {"full": "PUBLIC JOINT STOCK COMPANY", "abbr": ["PJSC"]},
    "ЗАКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО": {"full": "CLOSED JOINT STOCK COMPANY", "abbr": ["CJSC"]},
    "ОТКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО": {"full": "OPEN JOINT STOCK COMPANY", "abbr": ["OJSC"]},
    "КОММАНДИТНОЕ ТОВАРИЩЕСТВО": {"full": "LIMITED PARTNERSHIP", "abbr": ["LP"]},
    "ПОЛНОЕ ТОВАРИЩЕСТВО": {"full": "GENERAL PARTNERSHIP", "abbr": ["GP"]},
    "ТОВАРИЩЕСТВО НА ВЕРЕ": {"full": "PARTNERSHIP WITH LIMITED LIABILITY", "abbr": ["LLP"]},
    "ГОСУДАРСТВЕННОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ": {"full": "STATE UNITARY ENTERPRISE", "abbr": ["SUE"]},
    "МУНИЦИПАЛЬНОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ": {"full": "MUNICIPAL UNITARY ENTERPRISE", "abbr": ["MUE"]},
    "ХОЗЯЙСТВЕННОЕ ТОВАРИЩЕСТВО": {"full": "BUSINESS PARTNERSHIP", "abbr": []},
    "КООПЕРАТИВ": {"full": "COOPERATIVE", "abbr": ["CO-OP"]},
    "ЖИЛИЩНО-СТРОИТЕЛЬНЫЙ КООПЕРАТИВ": {"full": "HOUSING CONSTRUCTION COOPERATIVE", "abbr": ["HCC"]},
    "ГАРАЖНЫЙ СПЕЦИАЛИЗИРОВАННЫЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ": {"full": "GARAGE SPECIALIZED CONSUMER COOPERATIVE", "abbr": ["GSCC"]},
    "ГАРАЖНЫЙ КООПЕРАТИВ": {"full": "GARAGE COOPERATIVE", "abbr": ["GC"]},
    "ТОВАРИЩЕСТВО СОБСТВЕННИКОВ ЖИЛЬЯ": {"full": "HOMEOWNERS ASSOCIATION", "abbr": ["HOA"]},
    "МЕЖДУНАРОДНЫЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ": {"full": "INTERNATIONAL CONSUMER COOPERATIVE", "abbr": ["ICC"]},
    "МЕЖДУНАРОДНОЕ ПОТРЕБИТЕЛЬСКОЕ ОБЩЕСТВО": {"full": "INTERNATIONAL CONSUMER SOCIETY", "abbr": ["ICS"]},
    "НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО": {"full": "NON-COMMERCIAL PARTNERSHIP", "abbr": ["NCP"]},
    "МЕСТНАЯ РЕЛИГИОЗНАЯ ОРГАНИЗАЦИЯ": {"full": "LOCAL RELIGIOUS ORGANIZATION", "abbr": ["LRO"]},
    "СПЕЦИАЛИЗИРОВАННЫЙ ЗАСТРОЙЩИК": {"full": "SPECIALIZED DEVELOPER", "abbr": ["SD"]},
    "ГОСУДАРСТВЕННОЕ АВТОНОМНОЕ ПРОФЕССИОНАЛЬНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ": {"full": "STATE AUTONOMOUS PROFESSIONAL EDUCATIONAL INSTITUTION", "abbr": ["SAPEI"]},
    "АВТОНОМНАЯ НЕКОММЕРЧЕСКАЯ ОРГАНИЗАЦИЯ": {"full": "AUTONOMOUS NON-COMMERCIAL ORGANIZATION", "abbr": ["ANO"]},
    "МУНИЦИПАЛЬНОЕ БЮДЖЕТНОЕ ДОШКОЛЬНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ": {"full": "MUNICIPAL BUDGET PRESCHOOL EDUCATIONAL INSTITUTION", "abbr": ["MBPEI"]},
    "МУНИЦИПАЛЬНОЕ ОБЩЕОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ": {"full": "MUNICIPAL GENERAL EDUCATIONAL INSTITUTION", "abbr": ["MGEI"]},
    "ГЛАВА КРЕСТЬЯНСКОГО (ФЕРМЕРСКОГО) ХОЗЯЙСТВА": {"full": "HEAD OF PEASANT (FARMER) HOUSEHOLD", "abbr": ["HPFH"]},
    "ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ": {"full": "FEDERAL STATE BUDGETARY INSTITUTION", "abbr": ["FSBI"]},
    "САДОВОДЧЕСКОЕ ТОВАРИЩЕСТВО": {"full": "GARDENING PARTNERSHIP", "abbr": ["GP"]},
    "ЧАСТНОЕ ОБЩЕОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ": {"full": "PRIVATE EDUCATIONAL INSTITUTION", "abbr": ["PEI"]},
    "МЕЖРЕГИОНАЛЬНАЯ ОБЩЕСТВЕННАЯ ОРГАНИЗАЦИЯ": {"full": "INTERREGIONAL PUBLIC ORGANIZATION", "abbr": ["IPO"]},
    "КРЕДИТНЫЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ": {"full": "CREDIT CONSUMER COOPERATIVE", "abbr": ["CCC"]},
    "САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО": {"full": "NON-COMMERCIAL GARDENING PARTNERSHIP", "abbr": ["NCGP"]},
    "МУНИЦИПАЛЬНОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ": {"full": "MUNICIPAL STATE INSTITUTION", "abbr": ["MSI"]},
    "БЛАГОТВОРИТЕЛЬНЫЙ ФОНД": {"full": "CHARITABLE FOUNDATION", "abbr": ["CF"]},
    "МЕСТНАЯ МУСУЛЬМАНСКАЯ РЕЛИГИОЗНАЯ ОРГАНИЗАЦИЯ": {"full": "LOCAL MUSLIM RELIGIOUS ORGANIZATION", "abbr": ["LMRO"]},
    "ПОТРЕБИТЕЛЬСКИЙ АВТОГАРАЖНЫЙ КООПЕРАТИВ": {"full": "CONSUMER GARAGE COOPERATIVE", "abbr": ["CGC"]},
    "СЕЛЬСКОХОЗЯЙСТВЕННЫЙ ПОТРЕБИТЕЛЬСКИЙ СНАБЖЕНЧЕСКО-СБЫТОВОЙ КООПЕРАТИВ": {"full": "AGRICULTURAL CONSUMER SUPPLY AND MARKETING COOPERATIVE", "abbr": ["ACSMC"]},
    "КОММУНАЛЬНОЕ ДОШКОЛЬНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ": {"full": "COMMUNAL PRESCHOOL EDUCATIONAL INSTITUTION", "abbr": ["CPEI"]},
    "КООПЕРАТИВ ЛИЧНЫХ ГАРАЖЕЙ-СТОЯНОК": {"full": "COOPERATIVE OF PERSONAL GARAGE PARKING", "abbr": ["CGPC"]},
    "ФОНД": {"full": "FOUNDATION", "abbr": []},
    "АССОЦИАЦИЯ": {"full": "ASSOCIATION", "abbr": []},
    "СОЮЗ": {"full": "UNION", "abbr": []},
    "ИНДИВИДУАЛЬНЫЙ ПРЕДПРИНИМАТЕЛЬ": {"full": "INDIVIDUAL ENTREPRENEUR", "abbr": ["IE", "SOLE PROPRIETOR"]}
}


# en_to_ru = {
#     "LIMITED LIABILITY COMPANY": {"ru": "ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ", "abbr": ["LLC", "LTD"]},
#     "JOINT STOCK COMPANY": {"ru": "АКЦИОНЕРНОЕ ОБЩЕСТВО", "abbr": ["JSC", "PLC"]},
#     "PUBLIC JOINT STOCK COMPANY": {"ru": "ПУБЛИЧНОЕ АКЦИОНЕРНОе ОБЩЕСТВО", "abbr": ["PJSC"]},
#     "CLOSED JOINT STOCK COMPANY": {"ru": "ЗАКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО", "abbr": ["CJSC"]},
#     "OPEN JOINT STOCK COMPANY": {"ru": "ОТКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО", "abbr": ["OJSC"]},
#     "LIMITED PARTNERSHIP": {"ru": "КОММАНДИТНОЕ ТОВАРИЩЕСТВО", "abbr": ["LP"]},
#     "GENERAL PARTNERSHIP": {"ru": "ПОЛНОЕ ТОВАРИЩЕСТВО", "abbr": ["GP"]},
#     "PARTNERSHIP WITH LIMITED LIABILITY": {"ru": "ТОВАРИЩЕСТВО НА ВЕРЕ", "abbr": ["LLP"]},
#     "STATE UNITARY ENTERPRISE": {"ru": "ГОСУДАРСТВЕННОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ", "abbr": ["SUE"]},
#     "MUNICIPAL UNITARY ENTERPRISE": {"ru": "МУНИЦИПАЛЬНОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ", "abbr": ["MUE"]},
#     "BUSINESS PARTNERSHIP": {"ru": "ХОЗЯЙСТВЕННОЕ ТОВАРИЩЕСТВО", "abbr": []},
#     "COOPERATIVE": {"ru": "КООПЕРАТИВ", "abbr": ["CO-OP"]},
#     "HOUSING CONSTRUCTION COOPERATIVE": {"ru": "ЖИЛИЩНО-СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", "abbr": ["HCC"]},
#     "GARAGE SPECIALIZED CONSUMER COOPERATIVE": {"ru": "ГАРАЖНЫЙ СПЕЦИАЛИЗИРОВАННЫЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", "abbr": ["GSCC"]},
#     "GARAGE COOPERATIVE": {"ru": "ГАРАЖНЫЙ КООПЕРАТИВ", "abbr": ["GC"]},
#     "HOMEOWNERS ASSOCIATION": {"ru": "ТОВАРИЩЕСТВО СОБСТВЕННИКОВ ЖИЛЬЯ", "abbr": ["HOA"]},
#     "INTERNATIONAL CONSUMER COOPERATIVE": {"ru": "МЕЖДУНАРОДНЫЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", "abbr": ["ICC"]},
#     "INTERNATIONAL CONSUMER SOCIETY": {"ru": "МЕЖДУНАРОДНОЕ ПОТРЕБИТЕЛЬСКОЕ ОБЩЕСТВО", "abbr": ["ICS"]},
#     "NON-COMMERCIAL PARTNERSHIP": {"ru": "НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО", "abbr": ["NCP"]},
#     "LOCAL RELIGIOUS ORGANIZATION": {"ru": "МЕСТНАЯ РЕЛИГИОЗНАЯ ОРГАНИЗАЦИЯ", "abbr": ["LRO"]},
#     "SPECIALIZED DEVELOPER": {"ru": "СПЕЦИАЛИЗИРОВАННЫЙ ЗАСТРОЙЩИК", "abbr": ["SD"]},
#     "STATE AUTONOMOUS PROFESSIONAL EDUCATIONAL INSTITUTION": {"ru": "ГОСУДАРСТВЕННОЕ А



class HandleLegalFormStep:
    def __call__(self, context: Context, next_step: NextStep) -> None:
        raw_legal_form = context.raw_company.legal_entity_state


        next_step(context)