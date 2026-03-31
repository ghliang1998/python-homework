import pandas as pd
from sqlalchemy import create_engine

# 配置区：数据库连接信息
HOST = '192.168.40.83'
PORT = 3306
USER = 'student'
PASSWORD = 'mlbb2026'
DATABASE = 'homework_db'

def get_db_engine():
    """创建并返回数据库引擎对象，用于连接MySQL数据库。"""
    connection_string = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    engine = create_engine(connection_string)
    return engine


def execute_sql_query(sql_query):
    """执行SQL查询并返回结果DataFrame。"""
    engine = get_db_engine()
    df = pd.read_sql(sql_query, engine)
    return df


def load_hero_battle_stats():
    """加载并合并 hero 表与 battle_record 表的数据，计算每个英雄的胜率等统计指标。"""
    # 先加载原始表
    hero_df = execute_sql_query("SELECT hero_id, hero_name, role, attack_type FROM hero")
    battle_df = execute_sql_query("SELECT hero_id, is_win FROM battle_record")

    # 关联两张表（inner join），仅保留有对局记录的英雄
    merged = battle_df.merge(hero_df, on="hero_id", how="inner")

    # 计算统计值
    stats = (
        merged
        .groupby(["hero_id", "hero_name", "role", "attack_type"], as_index=False)
        .agg(total_matches=("is_win", "count"), win_count=("is_win", "sum"))
    )
    stats["win_rate_pct"] = (stats["win_count"] / stats["total_matches"] * 100).round(1)
    return stats


def filter_and_sort(stats_df, min_matches=30):
    """筛选出总场次 >= min_matches 的英雄，并按胜率从高到低排序。"""
    filtered = stats_df[stats_df["total_matches"] >= min_matches].copy()
    filtered = filtered.sort_values(by="win_rate_pct", ascending=False)
    return filtered


def export_to_excel(df, filename="hero_winrate.xlsx"):
    """将结果导出为 Excel 文件。

    由于 .xlsx 文件本身为 Unicode 格式，Excel 不会出现编码乱码。
    这里将胜率格式化为带百分号的字符串，保留一位小数。"""
    df_export = df.copy()
    df_export["win_rate_pct"] = df_export["win_rate_pct"].map(lambda v: f"{v:.1f}%")
    df_export.to_excel(filename, index=False, engine="openpyxl")


def print_summary(df):
    """在终端打印统计摘要：英雄总数、平均胜率、最高胜率英雄名称。"""
    total_heroes = len(df)
    avg_winrate = df["win_rate_pct"].mean()
    top_hero = df.iloc[0]["hero_name"] if total_heroes > 0 else ""

    print(f"\n统计摘要：")
    print(f"- 记录中出场过的英雄总数：{total_heroes}")
    print(f"- 每个英雄的平均胜率：{avg_winrate:.1f}%")
    print(f"- 胜率最高的英雄：{top_hero}")


def main():
    """主流程：加载数据、计算胜率、筛选、导出、打印摘要。"""
    stats = load_hero_battle_stats()
    result = filter_and_sort(stats, min_matches=30)
    export_to_excel(result, filename="hero_winrate.xlsx")
    print_summary(result)


if __name__ == "__main__":
    main()
