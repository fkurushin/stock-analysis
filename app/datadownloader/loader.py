from urllib.parse import urlencode
from urllib.request import urlopen
from datetime import datetime
from .tickers import tickers
from loguru import logger
import pandas as pd

FINAM_URL = "http://export.finam.ru/"
market = 0  # можно не задавать. Это рынок, на котором торгуется бумага. Для акций работает с любой цифрой. Другие рынки не проверял.
# filename = "quotes.txt"


def download_data(ticker, period, start: str, end: str):
    logger.info(
        f"ticker={ticker}; period={period}; start={start}; end={end}"
    )

    start_date = datetime.strptime(start, "%d.%m.%Y").date()
    start_date_rev = datetime.strptime(start, "%d.%m.%Y").strftime("%Y%m%d")
    end_date = datetime.strptime(end, "%d.%m.%Y").date()
    end_date_rev = datetime.strptime(end, "%d.%m.%Y").strftime("%Y%m%d")
    params = urlencode(
        [
            ("market", market),  # на каком рынке торгуется бумага
            (
                "em",
                tickers[ticker],
            ),  # вытягиваем цифровой символ, который соответствует бумаге.
            ("code", ticker),  # тикер нашей акции
            ("apply", 0),  # не нашёл что это значит.
            ("df", start_date.day),  # Начальная дата, номер дня (1-31)
            ("mf", start_date.month - 1),  # Начальная дата, номер месяца (0-11)
            ("yf", start_date.year),  # Начальная дата, год
            ("from", start_date),  # Начальная дата полностью
            ("dt", end_date.day),  # Конечная дата, номер дня
            ("mt", end_date.month - 1),  # Конечная дата, номер месяца
            ("yt", end_date.year),  # Конечная дата, год
            ("to", end_date),  # Конечная дата
            ("p", period),  # Таймфрейм
            (
                "f",
                ticker + "_" + start_date_rev + "_" + end_date_rev,
            ),  # Имя сформированного файла
            ("e", ".csv"),  # Расширение сформированного файла
            ("cn", ticker),  # ещё раз тикер акции
            (
                "dtf",
                1,
            ),
            ("tmf", 1),  # В каком формате брать время. Выбор из 4 возможных.
            ("MSOR", 0),  # Время свечи (0 - open; 1 - close)
            ("mstime", "on"),  # Московское время
            ("mstimever", 1),  # Коррекция часового пояса
            (
                "sep",
                1,
            ),  # Разделитель полей	(1 - запятая, 2 - точка, 3 - точка с запятой, 4 - табуляция, 5 - пробел)
            ("sep2", 1),  # Разделитель разрядов
            ("datf", 1),  # Формат записи в файл. Выбор из 6 возможных.
            # 1 - '<TICKER>,<PER>,<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>
            ("at", 1),
        ]
    )
    url = (
        FINAM_URL + ticker + "_" + start_date_rev + "_" + end_date_rev + ".csv?" + params
    )
    logger.info("Стучимся на Финам по ссылке: " + url)
    # txt = urlopen(
    #     url
    # ).readlines()

    try:
        response = urlopen(url)
        if response.status == 200:
            txt = response.readlines()
            # Process the downloaded data as needed
            return pd.DataFrame(
                [t.strip().decode("utf-8").split(",") for t in txt[1:]],
                columns=txt[0].strip().decode("utf-8").split(","))
        else:
            logger.error("Ошибка при загрузке данных: " + str(response.status))
            return None
    except Exception as e:
        logger.error("Ошибка при загрузке данных: " + str(e))
        return None


if __name__ == "__main__":
    # пользовательские переменные
    ticker = "SBER"  # задаём тикер
    period = 7  # задаём период. Выбор из: 'tick': 1, 'min': 2, '5min': 3, '10min': 4, '15min': 5, '30min': 6, 'hour': 7, 'daily': 8, 'week': 9, 'month': 10
    start = "01.01.2017"  # с какой даты начинать тянуть котировки
    end = "31.12.2017"  # финальная дата, по которую тянуть котировки
    print(download_data(ticker, period, start, end).head())
