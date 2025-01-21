# -*- coding: utf-8 -*-
import logging
import os
import traceback
from datetime import datetime
from functools import wraps

# 确保日志目录存在
log_dir = os.path.join('resources', 'logs')
os.makedirs(log_dir, exist_ok=True)

def setup_logger():
    # 生成日志文件名（按日期）
    current_date = datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(log_dir, f'app_{current_date}.log')
    
    # 配置日志记录器
    logger = logging.getLogger('app_logger')
    logger.setLevel(logging.DEBUG)
    
    # 清除现有的处理器
    if logger.handlers:
        logger.handlers.clear()
    
    # 创建文件处理器
    file_handler = logging.FileHandler(
        filename=log_file,
        encoding='utf-8',
        mode='a'
    )
    file_handler.setLevel(logging.INFO)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    # 设置详细的日志格式
    log_format = (
        '\n%(asctime)s %(levelname)s\n'
        'File "%(pathname)s", line %(lineno)d, in %(funcName)s\n'
        'Message: %(message)s\n'
        '%(stack_info)s'
    )
    
    formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # 防止日志重复
    logger.propagate = False
    
    return logger

# 创建logger实例
logger = setup_logger()

def log_error(exc_info=True, stack_info=True):
    """装饰器：用于记录函数执行时的错误"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # 获取完整的错误信息
                error_msg = f"""
                异常类型: {type(e).__name__}
                异常信息: {str(e)}
                函数名称: {func.__name__}
                参数信息: args={args}, kwargs={kwargs}
                """
                logger.error(
                    error_msg,
                    exc_info=exc_info,
                    stack_info=stack_info
                )
                raise  # 重新抛出异常
        return wrapper
    return decorator

# 使用示例
if __name__ == '__main__':
    # 基本日志测试
    logger.debug('调试信息')
    logger.info('普通信息')
    logger.warning('警告信息')
    
    # 测试错误日志装饰器
    @log_error()
    def test_function(x, y):
        return x / y
    
    try:
        test_function(1, 0)  # 将触发除零错误
    except:
        pass  # 错误已被记录
