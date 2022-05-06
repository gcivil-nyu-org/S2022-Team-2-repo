from django.contrib import admin
from django.core.mail import EmailMessage
from django.db.models import Count
from django.template.loader import render_to_string

from .models import Profile, FriendRequest, Report, Blacklist

admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(Blacklist)

admin.site.site_header = "NYUnite Admin Portal"


def report_email(user):
    to_email = user.username + "@nyu.edu"
    mail_subject = "From NYUnite Admin Team: Your account has been removed"
    message = render_to_string(
        "users/report_email.html",
        {"user": user},
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


def report_wrapper(user):
    blacklist_record = Blacklist(blacklisted=user)
    blacklist_record.save()
    user.is_active = False
    user.save()
    reports = Report.objects.all().filter(reported=user)
    reports.update(status="approved")
    report_email(user)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("reported", "reporter", "reason", "status")
    list_filter = ("status",)
    actions = ['make_received', 'make_ignored', 'make_approved']

    def get_queryset(self, request):
        qs = super(ReportAdmin, self).get_queryset(request).annotate(count=Count('reported'))
        return qs.order_by('count').order_by("-status")

    @admin.action(description="Mark selected reports as received")
    def make_received(self, request, queryset):
        queryset.update(status="received")

    @admin.action(description="Mark selected reports as ignored")
    def make_ignored(self, request, queryset):
        queryset.update(status="ignored")

    @admin.action(description="Mark selected reports as approved")
    def make_approved(self, request, queryset):
        queryset.update(status="approved")
        reported = set()
        for report in queryset:
            reported.add(report.reported)
        for user in reported:
            report_wrapper(user)
