import sqlite3
from pathlib import Path

import clavier


class Helpers:
    base_path = Path(__file__).parent
    db_path = (base_path / "src/distarb.db").resolve()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    TICKERS = [row[0] for row in cursor.execute("SELECT ticker_symbol FROM stocks").fetchall()]
    COMPANIES = [row[0] for row in cursor.execute("SELECT company_name FROM stocks").fetchall()]
    CLEAN_COMPANIES = [
        row[0] for row in cursor.execute("SELECT clean_company FROM stocks").fetchall()
    ]

    conn.close()

    def __init__(self, TICKERS, COMPANIES):
        self.TICKERS_LIST = TICKERS
        self.COMPANIES = COMPANIES

    @classmethod
    def _get_connection(cls):
        return sqlite3.connect(cls.db_path)

    @classmethod
    def get_alignments(cls, search_item, is_business):
        keyboard = clavier.load_qwerty(staggering=[0.5, 0.25, 0.5])
        search_item = search_item.lower()
        alignment_list = []

        if not is_business:
            for ticker in cls.TICKERS:
                ticker = ticker.lower()
                distance = keyboard.word_distance(
                    search_item, ticker, deletion_cost=0.001, insertion_cost=0.001
                )
                key_distance = keyboard.typing_distance(ticker)
                if distance <= 1 and key_distance <= 50:
                    alignment_list.append((ticker, distance, key_distance))

            alignment_list.sort(key=lambda x: (x[1], x[2]), reverse=False)
            distances = ""
            tickers = "".join([f"{item[0]}\n" for i, item in enumerate(alignment_list[:10])])[:-1]

        elif is_business:
            for company in cls.CLEAN_COMPANIES:
                company = company.lower()
                distance = keyboard.word_distance(
                    search_item, company, deletion_cost=0.001, insertion_cost=0.001
                )
                distance = float(f"{distance:.7f}")
                key_distance = keyboard.typing_distance(company)
                if distance <= 0.05 and key_distance <= 100:
                    alignment_list.append((company, distance, key_distance))

            alignment_list.sort(key=lambda x: (x[1], x[2]), reverse=False)
            distances = ""
            tickers = []
            for item in alignment_list[:3]:
                tickers.append(f"{item[0]}")

        return (distances, tickers, is_business)

    @classmethod
    def get_TICKERS(cls):
        return cls.TICKERS

    @classmethod
    def get_COMPANIES(cls):
        return cls.COMPANIES

    @classmethod
    def get_CLEAN_COMPANIES(cls):
        return cls.CLEAN_COMPANIES

    @classmethod
    def get_ticker_from_name(cls, company_name) -> str:
        conn = cls._get_connection()
        result = conn.execute(
            "SELECT ticker_symbol FROM stocks WHERE company_name = ?", (company_name,)
        ).fetchone()
        conn.close()
        return result[0] if result else None

    @classmethod
    def get_name_from_ticker(cls, ticker_name) -> str:
        conn = cls._get_connection()
        result = conn.execute(
            "SELECT company_name FROM stocks WHERE ticker_symbol = ?", (ticker_name,)
        ).fetchone()
        conn.close()
        return result[0] if result else None

    @classmethod
    def get_clean_name(cls, company_name) -> str:
        conn = cls._get_connection()
        result = conn.execute(
            "SELECT clean_company FROM stocks WHERE company_name = ?", (company_name,)
        ).fetchone()
        conn.close()
        return result[0] if result else None

    @classmethod
    def get_ticker_from_clean_name(cls, clean_company_name) -> str:
        conn = cls._get_connection()
        result = conn.execute(
            "SELECT ticker_symbol FROM stocks WHERE clean_company = ?", (clean_company_name,)
        ).fetchone()
        conn.close()
        return result[0] if result else None

    @classmethod
    def get_company_from_clean_name(cls, clean_company_name) -> str:
        conn = cls._get_connection()
        result = conn.execute(
            "SELECT company_name FROM stocks WHERE clean_company = ?", (clean_company_name,)
        ).fetchone()
        conn.close()
        return result[0] if result else None


if __name__ == "__main__":
    pass
