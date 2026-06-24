from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        user_notifications = Notification.objects.filter(user=request.user)
        unread_count = user_notifications.filter(is_read=False).count()
        unread_announcements = user_notifications.filter(is_read=False, link__icontains='announcements').count()
        unread_leave_requests = user_notifications.filter(is_read=False, link__icontains='leave-requests').count()
        
        return {
            'unread_notifications_count': unread_count,
            'unread_announcements_count': unread_announcements,
            'unread_leave_requests_count': unread_leave_requests,
        }
    return {}
