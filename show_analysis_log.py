import pandas as pd

from database_connection import get_db_engine
from logging_config import setup_logger

logger = setup_logger("show_log")


def print_all_analysis_log():
    """查询 analysis_log 表并打印所有记录。"""
    engine = get_db_engine()
    all_log = pd.read_sql("SELECT * FROM analysis_log", engine)
    logger.info(f"\n所有分析日志（共 {len(all_log)} 条）:\n{all_log.to_string()}")


if __name__ == "__main__":
    logger.info("开始查询分析日志")
    print_all_analysis_log()
    logger.info("查询完成")
