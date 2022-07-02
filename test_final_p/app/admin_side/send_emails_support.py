# Import all necessary moduls:
# 1) from Django package.
from django.core.mail import send_mail

# 2) Local import.
from user_side.models import CustomUser


# Sending notification on admin email, when script cannot
# find scores of this match.
def send_match_error_message_to_admin(input_data):
    # Email for recived notification.
    admin_email = CustomUser.objects.filter(username="admin")[0].email
    send_mail(
        f"Виникли проблеми з матчем '{input_data['teams_together']}',",
        f"знайдений статус матча '{input_data['match_status']}'",
        "karbivnychyi.volodymyr@gmail.com",
        [admin_email],
        fail_silently=False
    )


# Sending notification via email, for User who didn`t make forecast.
def send_reminder_to_user(input_data):
    # Email of User who will get notification.
    user_email = CustomUser.objects.filter(
        username=input_data["user_name"])[0].email
    send_mail(
        subject="Нагадування про прогноз.",
        message=(
            f"Шановний '{input_data['user_name']}', матч "
            f"'{input_data['match']}' розпочнеться менше ніж за годину, "
            "будь-ласка не забудьте зробити прогноз. "
            "Перейдіть за почиланням - http://127.0.0.1:8000/"
        ),
        from_email="karbivnychyi.volodymyr@gmail.com",
        recipient_list=[user_email, ],
        fail_silently=False,
    )


# Sending notification on admin email, when match/matches in round are not ok.
def send_round_error_message_to_admin(input_data):
    admin_email = CustomUser.objects.filter(username="admin")[0].email
    send_mail(
        subject=f"Проблеми з туром #'{input_data['round_number']}'.",
        message=(
            "Вам як адмінісратору потрібно перевірити проблемні матчі в турі"
            ", і потім запустити скрипт для обрахунку балів вручну."
        ),
        from_email="karbivnychyi.volodymyr@gmail.com",
        recipient_list=[admin_email, ],
        fail_silently=False,
    )
