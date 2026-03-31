import pandas as pd

from database_connection import get_db_engine
from logging_config import setup_logger

logger = setup_logger("export_csv")


def export_analysis_log_to_csv(filename: str = "analysis_log.csv"):
    """从数据库中读取 analysis_log 表并导出为 CSV 文件。"""
    engine = get_db_engine()
    all_log = pd.read_sql("SELECT * FROM analysis_log", engine)
    all_log.to_csv(filename, index=False, encoding="utf-8-sig")
    logger.info(f"已导出 analysis_log 到 CSV：{filename}，共 {len(all_log)} 条记录")


if __name__ == "__main__":
    logger.info("开始导出分析日志到CSV")
    export_analysis_log_to_csv()
    logger.info("导出完成")
