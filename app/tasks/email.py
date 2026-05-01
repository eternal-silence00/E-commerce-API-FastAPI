from app.celery_app import celery_app
import time

@celery_app.task(bind=True, max_retries=3,default_retry_delay=30)
def send_order_confirmation(self, user_email: str, order_id: int):
    time.sleep(2)  # имитация задержки отправки
    print(f"Email отправлен на {user_email} для заказа {order_id}")
    return {"status": "sent", "to": user_email}