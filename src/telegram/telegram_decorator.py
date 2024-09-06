from functools import wraps

from src.log.logger import logger

def get_default_logger():
    return

def telegram_error_handling(_func=None, bot = None):
    def decorator_err(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                logger.exception(f"Exception raised in {func.__name__}. exception: {str(e)}")
                message = args[0]
                if message:
                    bot.send_message(message.chat.id, "Ops, Exception was raised! Try again! ", parse_mode='HTML')
        return wrapper

    if _func is None:
        return decorator_err
    else:
        return decorator_err(_func)
