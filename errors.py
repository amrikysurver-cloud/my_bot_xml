import logging
from aiogram import Router
from aiogram.types import ErrorEvent

error_router = Router()
logger = logging.getLogger(__name__)

@error_router.errors()
async def global_error_handler(event: ErrorEvent):
    logger.critical(f'Critical exception caught globally: {event.exception}', exc_info=True)
    try:
        if event.update.message:
            await event.update.message.answer('⚠️ عذراً، حدث خطأ داخلي غير متوقع في النظام. تم إبلاغ المطورين لحله فوراً.')
        elif event.update.callback_query:
            await event.update.callback_query.answer('⚠️ حدث خطأ داخلي في معالجة الطلب.', show_alert=True)
    except Exception as e:
        logger.error(f'Failed to handle error feedback to user: {e}')
