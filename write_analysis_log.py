import pandas as pd
from datetime import datetime
from sqlalchemy import text

from database_connection import get_db_engine


def load_hero_winrate():
    """从 hero_winrate.xlsx 读取结果到 DataFrame。"""
    return pd.read_excel("hero_winrate.xlsx")


def enrich_with_meta(df: pd.DataFrame) -> pd.DataFrame:
    """在 DataFrame 前新增 analyst/run_time 字段，并重命名字段以匹配数据库表。"""
    df2 = df.copy()
    df2.insert(0, "analyst", "郭海量")
    df2.insert(1, "run_time", datetime.now())
    # 重命名字段以匹配 analysis_log 表
    df2 = df2.rename(columns={
        "total_matches": "total_games",
        "win_count": "win_games",
        "win_rate_pct": "win_rate"
    })
    # 将 win_rate 从字符串 "59.0%" 转换为 float 0.59
    df2["win_rate"] = df2["win_rate"].str.rstrip('%').astype(float) / 100
    # 删除表中不存在的列
    df2 = df2.drop(columns=["role", "attack_type"])
    return df2


def write_to_analysis_log(df: pd.DataFrame):
    """将 DataFrame 追加写入 analysis_log 表。

    注意：由于用户权限限制，无法删除现有记录。
    如果已有 analyst='郭海量' 的记录，将追加新数据（可能导致重复）。
    """
    engine = get_db_engine()
    # 由于权限问题，无法删除，先检查是否有现有记录
    existing_count = pd.read_sql("SELECT COUNT(*) as cnt FROM analysis_log WHERE analyst = '郭海量'", engine).iloc[0, 0]
    if existing_count > 0:
        print(f"警告：已有 {existing_count} 条 analyst='郭海量' 的记录。由于权限限制，无法删除。将追加新数据。")
    # 追加新数据
    try:
        df.to_sql("analysis_log", engine, if_exists="append", index=False)
        print(f"已追加 {len(df)} 条新记录到 analysis_log 表。")
    except Exception as e:
        print(f"写入失败: {e}")


def print_all_analysis_log():
    """查询 analysis_log 表并打印所有记录。"""
    engine = get_db_engine()
    all_log = pd.read_sql("SELECT * FROM analysis_log", engine)
    print(all_log)


def main():
    df = load_hero_winrate()
    enriched = enrich_with_meta(df)
    print(f"准备写入 {len(enriched)} 行 analyst='郭海量' 的数据")
    write_to_analysis_log(enriched)
    print_all_analysis_log()


if __name__ == "__main__":
    main()
