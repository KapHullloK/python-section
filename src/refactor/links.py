import datetime
import re
from datetime import date

from bs4 import BeautifulSoup

LINK_CLASS = "accordeon-inner__item-title link xls"

REPORTS_PATH_PREFIX = "/upload/reports/oil_xls/oil_xls_"
REPORT_EXTENSION = ".xls"
BASE_URL = "https://spimex.com"
DATE_FILENAME_PATTERN = re.compile(r"oil_xls_(\d{8})\.xls")


def parse_page_links(html: str, start_date: date, end_date: date) -> list[tuple[str, date]]:
    """
    Парсит ссылки на бюллетени с одной страницы

    :param html: HTML-контент страницы для парсинга.
    :param start_date: Начальная дата диапазона фильтрации (включительно).
    :param end_date: Конечная дата диапазона фильтрации (включительно).
    :return: Список кортежей [(url, date), ...], где:
        - url: полный URL отчёта
        - date: дата отчёта, извлечённая из имени файла

    :example:
    <a class="accordeon-inner__item-title link xls" href="/upload/reports/oil_xls/oil_xls_20240101_test.xls">link1</a>
    """
    results = []
    soup = BeautifulSoup(html, "html.parser")
    soup_links = soup.find_all("a", class_=LINK_CLASS)

    for soup_link in soup_links:
        href = soup_link.get("href")
        if not href:
            continue

        prefix_href = href.split("?")[0]
        if REPORTS_PATH_PREFIX not in prefix_href or not prefix_href.endswith(REPORT_EXTENSION):
            continue

        try:
            match = DATE_FILENAME_PATTERN.search(prefix_href)
            report_date = datetime.datetime.strptime(match.group(1), "%Y%m%d").date()

            if start_date <= report_date <= end_date:
                u = href if href.startswith("http") else BASE_URL + href
                results.append((u, report_date,))
            else:
                # TODO:добавить логгер
                print(f"Ссылка {href} вне диапазона дат")
        except Exception as e:
            # TODO:добавить логгер
            print(f"Не удалось извлечь дату из ссылки {href}: {e}")

    return results
