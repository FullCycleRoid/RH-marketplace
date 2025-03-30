from typing import List, Optional, Dict
from sqlalchemy import text
from sqlalchemy.orm import Session

get_by_inn_stmt = """
WITH company_data AS (
    SELECT
        c.id,
        c.country_code,
        -- Переводы названия компании
        (
            SELECT json_agg(json_build_object('lang', ct.language_code, 'name', ct.name))
            FROM company_translations ct
            WHERE ct.company_id = c.id AND ct.language_code = :lang
        ) AS translations,
        -- Данные менеджеров
        (
            SELECT json_agg(json_build_object(
                'inn', m.inn,
                'position', m.position,
                'name', COALESCE(
                    (SELECT mt.full_name 
                     FROM manager_translations mt 
                     WHERE mt.manager_id = m.id AND mt.language_code = :lang),
                    'No name'
                )
            ))
            FROM managers m
            WHERE m.company_id = c.id
        ) AS managers,
        -- Коды ОКВЭД
        (
            SELECT json_agg(json_build_object('code', o.code, 'name', o.name))
            FROM company_m2m_okved co
            JOIN okved_nodes o ON co.okved_id = o.id
            WHERE co.company_id = c.id
        ) AS okveds,
        -- Дата регистрации
        (
            SELECT f.datetime_data
            FROM company_fields f
            JOIN company_field_type cft ON f.company_field_type_id = cft.id
            JOIN field_type_translations ftt 
                ON cft.id = ftt.field_type_id 
                AND ftt.language_code = :lang
                AND ftt.name ILIKE 'дата_регистрации'
            WHERE f.company_id = c.id
            LIMIT 1
        ) AS registration_date
    FROM companies c
    JOIN company_fields cf ON c.id = cf.company_id
    JOIN company_field_type cft ON cf.company_field_type_id = cft.id
    JOIN field_type_translations ftt 
        ON cft.id = ftt.field_type_id 
        AND ftt.language_code = :lang
        AND (ftt.name ILIKE 'инн' OR ftt.name ILIKE 'inn')
    WHERE
        cf.code = :inn_value
)
SELECT 
    id,
    country_code,
    json_build_object(
        'name', COALESCE((translations->0->>'name'), 'No name'),
        'inn', :inn_value,
        'okveds', COALESCE(okveds, '[]'::json),
        'registration_date', registration_date,
        'managers', COALESCE(managers, '[]'::json)
    ) AS data
FROM company_data;
"""

class RawCompanyQueryManager:
    """Класс для выполнения сырых SQL-запросов"""

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, company_id: str, lang: str = 'RU') -> Optional[Dict]:
        """Получение компании по ID с использованием SQL (исправленная версия)"""
        query = text("""
        SELECT 
            c.id,
            c.country_code,
            c.legal_status,
            c.system_status,
            c.created_at,
            c.updated_at,
            json_build_object(
                'translations', COALESCE(ct.translations, '[]'),
                'fields', COALESCE(cf.fields, '[]'),
                'managers', COALESCE(m.managers, '[]'),
                'okveds', COALESCE(ok.okveds, '[]'),
                'financial_reports', COALESCE(fr.reports, '[]'),
                'tax_reports', COALESCE(tr.reports, '[]'),
                'contacts', COALESCE(con.contacts, '[]')
            ) as data
        FROM companies c
        LEFT JOIN (
            SELECT company_id, json_agg(json_build_object(
                'lang', language_code,
                'name', name
            )) as translations
            FROM company_translations
            GROUP BY company_id
        ) ct ON c.id = ct.company_id
        LEFT JOIN (
            SELECT 
                cf.company_id,
                json_agg(json_build_object(
                    'code', cf.code,
                    'value', COALESCE(ft.data, cf.code),
                    'name', ftt.name,
                    'data_type', cft.data_type
                )) as fields
            FROM company_fields cf
            LEFT JOIN field_translations ft 
                ON cf.id = ft.field_id AND ft.language_code = :lang
            LEFT JOIN company_field_type cft 
                ON cf.company_field_type_id = cft.id
            LEFT JOIN field_type_translations ftt
                ON cft.id = ftt.field_type_id AND ftt.language_code = :lang
            GROUP BY cf.company_id
        ) cf ON c.id = cf.company_id
        LEFT JOIN (
            SELECT 
                m.company_id,
                json_agg(json_build_object(
                    'inn', m.inn,
                    'position', m.position,
                    'since_on_position', m.since_on_position,
                    'name', COALESCE(mt.full_name, 'No name')
                )) as managers
            FROM managers m
            LEFT JOIN manager_translations mt 
                ON m.id = mt.manager_id AND mt.language_code = :lang
            GROUP BY m.company_id
        ) m ON c.id = m.company_id
        LEFT JOIN (
            SELECT 
                co.company_id,
                json_agg(json_build_object(
                    'code', o.code,
                    'name', o.name
                )) as okveds
            FROM company_m2m_okved co
            JOIN okved_nodes o ON co.okved_id = o.id
            GROUP BY co.company_id
        ) ok ON c.id = ok.company_id
        LEFT JOIN (
            SELECT 
                company_id,
                json_agg(json_build_object(
                    'year', year,
                    'annual_income', annual_income,
                    'net_profit', net_profit,
                    'currency', currency
                )) as reports
            FROM financial_reports
            GROUP BY company_id
        ) fr ON c.id = fr.company_id
        LEFT JOIN (
            SELECT 
                company_id,
                json_agg(json_build_object(
                    'year', year,
                    'taxes_paid', taxes_paid,
                    'paid_insurance', paid_insurance
                )) as reports
            FROM tax_reports
            GROUP BY company_id
        ) tr ON c.id = tr.company_id
        LEFT JOIN (
            SELECT 
                company_id,
                json_agg(json_build_object(
                    'type', type,
                    'data', data,
                    'is_verified', is_verified
                )) as contacts
            FROM contacts
            GROUP BY company_id
        ) con ON c.id = con.company_id
        WHERE c.id = :company_id
        """)

        result = self.session.execute(query, {
            'company_id': company_id,
            'lang': lang
        }).fetchone()

        return self._format_result(result) if result else None

    def get_by_inn(self, inn_value: str, lang: str = 'RU') -> List[Dict]:
        """Оптимизированный поиск по ИНН через сырой SQL"""
        clean_inn = ''.join(filter(str.isdigit, inn_value))

        result = self.session.execute(
                text(get_by_inn_stmt), {
                'inn_value': clean_inn,
                'lang': lang
            }).first()

        return result


    def _format_result(self, row) -> Dict:
        """Форматирование результата запроса по ID"""
        return {
            "id": str(row.id),
            "country_code": row.country_code,
            "legal_status": row.legal_status,
            "system_status": row.system_status,
            "created_at": row.created_at.isoformat(),
            "updated_at": row.updated_at.isoformat(),
            **row.data
        }

    def _format_inn_result(self, rows) -> List[Dict]:
        """Преобразование результатов запроса в список словарей"""
        return [
            {
                "id": str(row['id']),
                "country_code": row['country_code'],
                "name": row['data'].get('name', 'No name'),
                "inn": row['data'].get('inn', ''),
                "okveds": row['data'].get('okveds', []),
                "managers": row['data'].get('managers', [])
            }
            for row in rows
        ]


# # Пример использования
# # with MarketplaceDBSession() as session:
# manager = RawCompanyQueryManager()
#
# start = time()
# # Получение компании по ID
# # company = manager.get_by_id('00022e80-ccf9-4b47-9b29-a4fa45aaf987')
# # pprint(company)
#
# companies = manager.get_by_inn('7804576823')
# pprint(companies)
#
#
# elapsed = time() - start
# print('Time', elapsed)
