from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LeaveRequest, Announcement, StudentWarning, Notification, Student
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=LeaveRequest)
def leave_request_notification(sender, instance, created, **kwargs):
    if created:
        # Notify admins when a leave request is created
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            Notification.objects.create(
                user=admin,
                message=f"New Leave Request from {instance.user.get_full_name() or instance.user.username}",
                link="/dashboard/admin/leave-requests/"
            )
    else:
        # Notify teacher when leave request status changes
        if instance.status != 'Pending':
            Notification.objects.create(
                user=instance.user,
                message=f"Your Leave Request for {instance.start_date} was {instance.status}",
                link="/dashboard/teacher/leave-requests/"
            )

@receiver(post_save, sender=Announcement)
def announcement_notification(sender, instance, created, **kwargs):
    if created:
        # Notify all students
        students = Student.objects.all()
        for student in students:
            Notification.objects.create(
                user=student.user,
                message=f"New Announcement: {instance.title}",
                link="/dashboard/student/announcements/"
            )

@receiver(post_save, sender=StudentWarning)
def warning_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.student.user,
            message=f"You received a warning: {instance.message[:30]}...",
            link="/dashboard/student/"
        )
