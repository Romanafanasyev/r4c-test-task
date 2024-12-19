from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Robot
from orders.models import Order
from customers.models import Customer

@receiver(post_save, sender=Robot)
def notify_customer_on_robot_availability(sender, instance, created, **kwargs):
    if not created:
        return

    matching_orders = Order.objects.filter(robot_serial=f"{instance.model}-{instance.version}")

    for order in matching_orders:
        customer = order.customer

        send_mail(
            subject="Ваш робот теперь в наличии!",
            message=(
                f"Добрый день!\n\n"
                f"Недавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}. "
                f"Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами."
            ),
            from_email="support@robotfactory.com",
            recipient_list=[customer.email],
            fail_silently=False,
        )

        order.delete()
