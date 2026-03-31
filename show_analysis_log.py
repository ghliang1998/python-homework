import pandas as pd

from database_connection import get_db_engine


def print_all_analysis_log():
    """查询 analysis_log 表并打印所有记录。"""
    engine = get_db_engine()
    all_log = pd.read_sql("SELECT * FROM analysis_log", engine)
    print(all_log)


if __name__ == "__main__":
    print_all_analysis_log()
