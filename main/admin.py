from django.contrib import admin
from . import models


# Show a thumbnail image next to the alt text in Admin panel of BANNERS
class BannerAdmin(admin.ModelAdmin):
    list_display = ("alt_text", "image_tag")

admin.site.register(models.Banners, BannerAdmin)


# Show a thumbnail image next to the alt text in Admin panel of SERVICES
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "image_tag")

admin.site.register(models.Service, ServiceAdmin)


# Show alt text in Admin panel of PAGES
class PageAdmin(admin.ModelAdmin):
    list_display = ("title",)

admin.site.register(models.Page, PageAdmin)


# FAQ
class faqAdmin(admin.ModelAdmin):
    list_display = ("question", "answer",)

admin.site.register(models.faq, faqAdmin)


# Enquiry
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "detail", "send_time")

admin.site.register(models.Enquiry, EnquiryAdmin)


# Gallery (make a separate gallery for different occassion e.g. Competitions, Workout, Cardio outside etc...)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("title", "image_tag",)   

admin.site.register(models.Gallery, GalleryAdmin)


# Gallery Images (Add images to deifferent galleries)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("alt_text", "image_tag",)

admin.site.register(models.GalleryImage, GalleryImageAdmin)


# Subscription plan
class SubPlanAdmin(admin.ModelAdmin):
    # edit highlt status and max number of memberships in the list without opening the subscription plan
    list_editable = ("highlight", "max_member", "valid_days")
    list_display = ("title", "price","max_member", "valid_days", "highlight")

admin.site.register(models.SubPlan, SubPlanAdmin)


# Subscription plan features that will be displayed in the admin panel
class SubPlanFeatureAdmin(admin.ModelAdmin):
    list_display = ("feature", "subplans")
    # A function to show the plan in front of the feature that's contained in this plan
    def subplans(self, object):
        return " | " .join([sub.feature for sub in object.subplan.all()])

admin.site.register(models.SubPlanFeature, SubPlanFeatureAdmin)


# Plan discounts
class PlanDiscountAdmin(admin.ModelAdmin):
    list_display = ("subplan", "total_months", "total_discount")

admin.site.register(models.PlanDiscount, PlanDiscountAdmin)


# Subscriber
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("user", "mobile", "image_tag")

admin.site.register(models.Subscriber, SubscriberAdmin)


# Subscription
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "price", "reg_date")

admin.site.register(models.Subscription, SubscriptionAdmin)


# Trainer
class TrainerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "mobile", "is_active", "salary", "img", "details")
    list_editable = ("is_active",)

admin.site.register(models.Trainer, TrainerAdmin)


# Notifications
class NotifyAdmin(admin.ModelAdmin):
    list_display = ("notify_detail", "read_by_user", "read_by_trainer")

admin.site.register(models.Notify, NotifyAdmin)


# Notifications
class NotifUserStatusAdmin(admin.ModelAdmin):
    list_display = ("notif", "user", "status")

admin.site.register(models.NotifUserStatus, NotifUserStatusAdmin)


# Assign subscriber to a trainer
class AssignSubscriberAdmin(admin.ModelAdmin):
    list_display = ("user", "trainer")

admin.site.register(models.AssignSubscriber, AssignSubscriberAdmin)


# Trainer's Acheivments
class TrainerAcheivementAdmin(admin.ModelAdmin):
    list_display = ("trainer", "title", "date", "image_tag", "details")

admin.site.register(models.TrainerAcheivement, TrainerAcheivementAdmin)


# Trainer's Salary
class TrainerSalaryAdmin(admin.ModelAdmin):
    list_display = ("trainer", "amount", "amount_date", "remarks")

admin.site.register(models.TrainerSalary, TrainerSalaryAdmin)


# Trainer Notifications
class TrainerNotificationAdmin(admin.ModelAdmin):
    list_display = ('notif_msg',)

admin.site.register(models.TrainerNotification, TrainerNotificationAdmin)


# Trainer Notifications
class TrainerNotificationStatusAdmin(admin.ModelAdmin):
    list_display = ('notif_msg',)

admin.site.register(models.TrainerNotification, TrainerNotificationAdmin)


# Subscribers and Admin Messages to Trainer
class TrainerMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "trainer", "message")

admin.site.register(models.TrainerMessage, TrainerMessageAdmin)

