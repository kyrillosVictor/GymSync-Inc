from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User

# Send a notification after creating or saving an instance of any model to the custom function we make
# lie new user creation will send user info to the subscriber model
from django.db.models.signals import post_save
from django.dispatch import receiver

import json
import asyncio
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer


# Website home page banner
class Banners(models.Model):
    img = models.ImageField(upload_to="banners/")
    alt_text = models.CharField(max_length=150)

    # Edit model name in Admin panel (by removing the extra s)
    class Meta:
        verbose_name_plural = "Banners"

    # Show the name of images in Banners section that will be named through the panel section (admin panel)
    def __str__(self):
        return self.alt_text
    
    def image_tag(self):
        # Returns an HTML <img> tag to display the product's image in the admin interface
        # The image is displayed as a thumbnail with a width of 80 pixels.
        return mark_safe("<img src='%s' width='80'/>" %(self.img.url))


# The offered services
class Service(models.Model):
    title = models.CharField(max_length=150)
    detail = models.TextField()
    img = models.ImageField(upload_to="services/", null=True)
    
    # Show alt text of images in Service section (admin panel)
    def __str__(self):
        return self.title
    
    def image_tag(self):
        return mark_safe("<img src='%s' width='80'/>" %(self.img.url))


# Pages
class Page(models.Model):
    title = models.CharField(max_length=150)
    detail = models.TextField()

    def __str__(self):
        return self.title
    

# FAQ
class faq(models.Model):
    question = models.TextField()
    answer = models.TextField()

    class Meta:
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


# Enquiry
class Enquiry(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    detail = models.TextField()
    send_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Enquiries"
    
    def __str__(self):
        return self.question


# Gallery (make a separate gallery for different occassion e.g. Competitions, Workout, Cardio outside etc...)

class Gallery(models.Model):
    title = models.CharField(max_length=150)
    detail = models.TextField()
    img = models.ImageField(upload_to="gallery/", null=True)

    class Meta:
        verbose_name_plural = "Galleries"
    
    # Show alt text of images in Service section (admin panel)
    def __str__(self):
        return self.title
    
    def image_tag(self):
        return mark_safe("<img src='%s' width='80'/>" %(self.img.url))
    

# Gallery Images (Add images to deifferent galleries)
class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, null=True)
    alt_text = models.CharField(max_length=150)
    img = models.ImageField(upload_to="gallery_images/", null=True)
    
    # Show alt text of images in Service section (admin panel)
    def __str__(self):
        return self.alt_text
    
    def image_tag(self):
        return mark_safe("<img src='%s' width='80'/>" %(self.img.url))


# Subscription plans (pricing)
class SubPlan(models.Model):
    title = models.CharField(max_length=150)
    price = models.IntegerField()

    # Set a maximum number for memebrs to sign up for the plan and disable the "get started" button when the plan reaches the max number
    max_member = models.IntegerField(null=True)
    highlight = models.BooleanField(default=False, null=True)

    #Set validation days for the subscription plan
    valid_days = models.IntegerField(null=True)

    # Plan title (basic, Advanced etc...)
    def __str__(self):
        return self.title
    

# Subscription plan features
class SubPlanFeature(models.Model):
    # Many to many, so each feature can be added to the applicable plan instead of adding manually inside the plan
    # We add the feature once in the admin panel and select the plan that could contain this feature
    subplan = models.ManyToManyField(SubPlan)
    feature = models.CharField(max_length=150)

    # Show plan title in the comparison table
    def __str__(self):
        return self.feature
    

# Plans discounts
class PlanDiscount(models.Model):
    subplan = models.ForeignKey(SubPlan, on_delete=models.CASCADE, null=True)
    total_months = models.IntegerField()
    total_discount = models.IntegerField()

    def __str__(self):
        return str(self.total_months)


# Subscriber
class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    img = models.ImageField(upload_to="subs/")

    def __str__(self):
        return str(self.user)

    def image_tag(self):
        if self.img:
            return mark_safe("<img src='%s' width='80'/>" %(self.img.url))
        else:
            return 'no-image'


# When creating a new user it will be added to the subscribers database
@receiver(post_save, sender=User)
def create_subscriber(sender, instance, created, **kwargs):
    if created:
        Subscriber.objects.create(user=instance)


# Subscription
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    plan = models.ForeignKey(SubPlan, on_delete=models.CASCADE, null=True)
    price = models.CharField(max_length=15)
    reg_date = models.DateField(auto_now_add=True, null=True)

    # Other data will be displayed from the admin panel 


# Trainers
class Trainer(models.Model):
    full_name = models.CharField(max_length=150)
    username = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=False)
    details = models.TextField()
    img = models.ImageField(upload_to="trainers/")
    salary = models.IntegerField(default=1)

    # Social Media links to trainer's profile
    facebook = models.CharField(max_length=500, null=True)
    instagram = models.CharField(max_length=500, null=True)
    twitter = models.CharField(max_length=500, null=True)
    youtube = models.CharField(max_length=500, null=True)
    blog = models.CharField(max_length=500, null=True)

    def __str__(self):
        return str(self.full_name)
    
    def image_tag(self):
        if self.img:
            return mark_safe("<img src='%s' width='80'/>" %(self.img.url))
        else:
            return 'no-image'


# Notifications (Json response via AJAX)
class Notify(models.Model):
    notify_detail = models.TextField()
    read_by_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    read_by_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Notifications"

    def __str__(self):
        return str(self.notify_detail)
    

# Notifications - Mark as read by user
class NotifUserStatus(models.Model):
    notif = models.ForeignKey(Notify, on_delete=models.CASCADE, related_name='notifuserstatus')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Notification Status"


# Assign subscriber to a trainer
class AssignSubscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


# Trainer's Achievements
class TrainerAcheivement(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    date = models.DateField(null=True)
    img = models.ImageField(upload_to="trainers_achievments/")
    details = models.TextField()

    def __str__(self):
        return str(self.title)
    
    def image_tag(self):
        if self.img:
            return mark_safe("<img src='%s' width='80'/>" %(self.img.url))
        else:
            return 'no-image'
        

# Trainer's Salary
class TrainerSalary(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    amount = models.IntegerField()
    amount_date = models.DateField()
    remarks = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Trainers' Salaries"

    def __str__(self):
        return str(self.trainer.full_name)
    

# Training Notifications
class TrainerNotification(models.Model):
    notif_msg = models.TextField()

    def __str__(self):
        return str(self.notif_msg)


    def save(self,  *args, **kwargs):
        super(TrainerNotification, self).save(*args, **kwargs)
        channel_layer = get_channel_layer()
        notif = self.notif_msg
        total = TrainerNotification.objects.all().count()
        async_to_sync(channel_layer.group_send) (
            'noti_group_name', {
                'type' : 'send_notificatio',
                'value' : json.dumps({'notif':notif, 'total': total})}
            )



# Notifications - Mark as read by trainer
class NotifTrainerStatus(models.Model):
    notif = models.ForeignKey(TrainerNotification, on_delete=models.CASCADE, related_name='trainernotification')
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='trainer')
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Trainer Notification Status"


# Subscribers and Admin Messages to Trainer
class TrainerMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True)
    message = models.TextField()

    class Meta:
        verbose_name_plural = "Messages for Trainers"


# Send reports to admin
class TrainerSubscriberReport(models.Model):
    report_from_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, related_name='report_from_trainer')
    report_from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='report_from_user')

    report_for_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, related_name='report_for_trainer')
    report_for_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='report_for_user')

    report_msg = models.TextField()


# Add a website logo through the admin panel
class AppSetting(models.Model):
    logo_img = models.ImageField(upload_to='app_logos/')

    def image_tag(self):
        return mark_safe('<img src="%s" width="80"/>' % (self.logo_img.url))