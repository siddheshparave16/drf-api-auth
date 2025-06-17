import os
from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models  import User
from celery.utils.log import get_task_logger
from django.core.exceptions import ObjectDoesNotExist


logger = get_task_logger(__name__)

@shared_task(bind=True, max_retries=3, time_limit=120, soft_time_limit=90)
def send_email(self, user_pk):
    """
    Send welcome email to newly registered user
    Args:
        user_pk (int): Primary key of the newly registered user
    Returns:
        bool: True if email sent successfully, False otherwise
    """

    try:
        user = User.objects.get(pk=user_pk)
        
        send_mail(subject="User Registered Successfully.",
                message= f"""Hello {user.username},\n\n
                        Thank you for registering. Your account is now active.\n\n
                        Best regards,\n
                        The Team""",
                from_email= os.getenv("EMAIL_HOST_USER", "default@example.com"),
                recipient_list=[user.email],
                fail_silently=False
        )

        logger.info(f"Successfully sent welcome email to {user.email}")
    
    except ObjectDoesNotExist as e:
        logger.error(f"User with pk {user_pk} does not exist: {e}")
        return False
    
    except Exception as e:
        logger.error(f"Email sending failed for user {user_pk}: {str(e)}")
        self.retry(exc=e, countdown=60, max_retries=3)
        return False
    
    return True