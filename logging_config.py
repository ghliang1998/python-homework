import logging
import logging.handlers
import os


def setup_logger(name: str = "app", log_file: str = "task.log") -> logging.Logger:
    """
    配置日志系统，同时输出到控制台和文件。
    
    参数：
        name: 日志记录器名称
        log_file: 日志文件路径
    
    返回：
        配置好的Logger对象
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # 移除已有处理器，避免重复
    logger.handlers.clear()
    
    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器（输出到屏幕）
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器（输出到task.log）
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
