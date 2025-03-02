import re
from datetime import datetime

from pipelines.generic_pipeline import Context, NextStep
from src.company.dto import FinancialReport


def convert_to_numeric(value):
    try:
        # Извлекаем числовую часть и единицы измерения
        match = re.search(r"(-?\d[\d\.,]*)\s*(тыс|млн|млрд|трлн)?\.?\s*руб", value)
        if not match:
            return 0

        number = float(match.group(1).replace(",", ".").replace(" ", ""))
        unit = match.group(2)

        multipliers = {
            "тыс": 1_000,
            "млн": 1_000_000,
            "млрд": 1_000_000_000,
            "трлн": 1_000_000_000_000
        }

        return int(number * multipliers.get(unit, 1))
    except:
        return 0


def extract_financial_data(text):
    # Ищем все блоки с годами и показателями
    year_blocks = re.findall(
        r"Финансовые показатели за .*?(?=Финансовые показатели за|Финансовые коэффициенты|$)",
        text,
        re.DOTALL
    )

    financial_data = {}

    for block in year_blocks:
        # Извлекаем годы из заголовка
        years = re.findall(r"\b\d{4}\b(?=\s*год)", block)
        if not years:
            continue

        # Основной год отчета
        main_year = years[0]

        # Извлекаем показатели
        revenue = re.search(r"Выручка\s*([^Ч]+)", block)
        profit = re.search(r"Чистая прибыль\s*([^К]+)", block)
        capital = re.search(r"Капитал\s*([^\n]+)", block)

        # Собираем данные
        financial_data[main_year] = {
            "Выручка": convert_to_numeric(revenue.group(1)) if revenue else 0,
            "Чистая прибыль": convert_to_numeric(profit.group(1)) if profit else 0,
            "Капитал": convert_to_numeric(capital.group(1)) if capital else 0
        }

    return financial_data


class HandleFinancialReportStep:
    def __call__(self, context: Context, next_step: NextStep) -> None:
        annual_income = convert_to_numeric(context.raw_company.annual_income)
        net_profit = convert_to_numeric(context.raw_company.net_profit)
        context.company_dto.financial_reports.append(
            FinancialReport(
                year='2023',
                annual_income=annual_income,
                net_profit=net_profit,
                currency='RUB'
            )
        )

        next_step(context)
