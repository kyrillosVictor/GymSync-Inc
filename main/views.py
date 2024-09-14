from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.core import serializers
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Count
from . import models
from . import forms
import stripe

from datetime import timedelta

# To send an email to subscriber after purchasing
from django.conf import settings
from django.core.mail import send_mail, EmailMessage


# Home Page
def home(request):
    # banners sections
    banners = models.Banners.objects.all()
    # services
    services = models.Service.objects.all()[:3]
    # gallery pictures in reverse order, fetch only 9 pics
    gimgs = models.GalleryImage.objects.all().order_by("-id")[:9]
    return render(request, 'home.html', {'banners' : banners, 'services' : services, 'gimgs' : gimgs})


# Page details
def page_detail(request, id):
    page = models.Page.objects.get(id = id)
    return render(request, 'page.html', {'page' : page,})


# FAQ Page
def faq_list(request):
    FAQ = models.faq.objects.all()
    return render(request, 'faq.html', {'faqs' : FAQ,})


# Enquiry Page
def enquiry(request):
    
    msg = ''
    # Save the posted enquiry and show a message after posting an enquiry
    if request.method == "POST":
        form = forms.EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            msg = 'Your enquiry has been sent successfully'
    
    form = forms.EnquiryForm
    return render(request, 'enquiry.html', {'form' : form, 'msg' : msg})


# Show galleryies
def gallery(request):
    gallery = models.Gallery.objects.all().order_by('id')
    return render(request, 'gallery.html', {'gallerys' : gallery,})

# Show gallery pictures
def gallery_detail(request, id):
    gallery = models.Gallery.objects.get(id=id)
    gallery_images = models.GalleryImage.objects.filter(gallery=gallery).order_by('-id')
    return render(request, 'gallery_images.html', {'gallery_images' : gallery_images, "gallery" : gallery})


# Subscription Plans
def pricing(request):
    pricing = models.SubPlan.objects.annotate(total_members=Count("subscription__id")).all().order_by('price')
    features = models.SubPlanFeature.objects.all()
    return render(request, 'pricing.html', {'plans' : pricing, 'features' : features})


# Sign Up
def signup(request):
    if request.user.is_authenticated:
        return redirect('pricing')  # or redirect to any other page for authenticated users

    msg = None
    if request.method == 'POST':
        form = forms.SignUp(request.POST)
        if form.is_valid():
            form.save()
            msg = "Thank you for signing up, We're plaesed to have you in GymSync"
    form = forms.SignUp
    return render(request, 'registration/signup.html', {'form' : form, 'msg' : msg})


# Checkout
def checkout(request, plan_id):    
    planDetail = models.SubPlan.objects.get(pk=plan_id)

    return render(request, 'checkout.html', {'plan':planDetail,})


# Stripe API for payments
stripe.api_key = 'sk_test_51PrHmZAD6ucpsYs8tBW5zihoJm6PTBTkJ0XzqhPIdugxjjLosLLBP0uiW9ZW2cSG7mZPxeDBceJ6YfegxF6TDtJ100HrEFvEXK'
def checkout_session(request, plan_id):
    plan = models.SubPlan.objects.get(pk=plan_id)
    session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items=[{
            'price_data': {
                'currency': 'egp',
                'product_data': {
                'name': plan.title,
                },
                'unit_amount': float(plan.price),
            },
            'quantity': 1,
        }],
        mode = 'payment',
        #success_url = reverse('pay_success') + f'?session_id={session.id}'
        #cancel_url = reverse('pay_cancel')
        success_url = 'http://127.0.0.1:8000/pay_success?session_id={CECKOUT_SESSION_id}',
        cancel_url = 'http://127.0.0.1:8000/pay_cancel',
        client_reference_id = plan_id,
    )
    return redirect(session.url, code=303)

# Pay Success
def pay_success(request):
    session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
    plan_id = session.client_reference_id
    plan = models.SubPlan.objects.get(pk=plan_id)
    user = request.user
    models.Subscription.objects.create(
        plan = plan,
        user = user,
        price = plan.price,
    )
    subject = "Order Email"
    html_content = get_template('orderemail.html').render({'title' : plan.title})
    from_email = 'purchase@gymsync.com'

    msg = EmailMessage(subject, html_content, from_email, ['subscriber@email.com'])
    msg.content_subtype = "html"
    msg.send()
    
    return render(request, 'success.html')

# Pay Cancel
def pay_cancel(request):
    return render(request, 'cancel.html')


# User Dashboard
def user_dashboard(request):
    current_plan = models.Subscription.objects.get(user=request.user)
    my_trainer = models.AssignSubscriber.objects.get(user=request.user)
    end_date = current_plan.reg_date + timedelta(days=current_plan.plan.valid_days)

    # To show the number of unread notifications next to Notifications in left-side bar
    # Code didn't work properly so it was cancelled

    return render(request, 'user/dashboard.html', {
        'current_plan':current_plan,
        'my_trainer': my_trainer,
        'end_date': end_date,
        })


# Update the User's profile data
def update_profile(request):
    msg = None
    # save the updated data
    if request.method == "POST":
        form = forms.ProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            msg = "Your profile has been updated successfuly"
    
    # show the profile data
    form = forms.ProfileForm(instance = request.user)
    return render(request, 'user/update_profile.html', {'form' : form, 'msg' : msg})


# Trainer Login using session
def trainerlogin(request):
    
    msg = None
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        trainer = models.Trainer.objects.filter(username=username, password=password).count()

        if trainer > 0:
            trainer = models.Trainer.objects.filter(username=username, password=password).first()
            request.session['trainerlogin'] = True
            request.session['trainerid'] = trainer.id
            return redirect('/trainer_dashboard')
        else:
            msg = "Invalid"
    
    form = forms.TrainerLoginForm
    return render(request, 'trainer/trainerlogin.html', {'form' : form, 'msg' : msg})


# Trainer Logout
def trainerlogout(request):
    
    del request.session['trainerlogin']
    return redirect('/trainerlogin')


# Trainer Dashboard
def trainer_dashboard(request):
    return render(request, 'trainer/dashboard.html')


# Trainer Profile
def trainer_profile(request):
    trainer_id = request.session['trainerid']
    trainer = models.Trainer.objects.get(id=trainer_id)

    msg = None
    if request.method == 'POST':
        form = forms.TrainerProfileForm(request.POST, request.FILES, instance = trainer)
        if form.is_valid():
            form.save()
            msg = "Your profile has been updated successfuly"
    
    form = forms.TrainerProfileForm(instance=trainer)
    return render(request, 'trainer/profile.html', {'form' : form, 'msg' : msg})


# Notifications
def notifs(request):
    data = models.Notify.objects.all().order_by('-id')
    return render(request, 'notifs.html', {'data' : data})


# Get all notifications and update it with the interve of 5 seconds or more (up to the programmer)
def get_notifs(request):
    data = models.Notify.objects.all().order_by('-id')
    
    notifStatus = False
    jsonData = []
    totalUnread = 0

    for d in data:
        try:
            notifStatusData = models.NotifUserStatus.objects.get(user=request.user, notif=d)
            if notifStatusData:
                notifStatus: True
        except models.notifStatusData.DoesNotExist:
            notifStatus = False

        # Count the uread notifs
        if not notifStatus:
            totalUnread = totalUnread + 1

        jsonData.append({
            'pk': d.id,
            'notify_detail': d.notify_detail,
            'notifStatus': notifStatus
        })
    #jsonData = serializers.serialize('json', data)
    return JsonResponse({'data' : jsonData, 'totalUnread': totalUnread})


# Mark read by user
def mark_read_notif(request):
    notifs = request.GET.get['notifs']
    user = request.user
    models.NotifUserStatus.objects.create(notification=notifs, user=user, status=True)
    notifs = models.Notify.objects.get(pk=notifs)
    return JsonResponse({'bool':True})


# Assigned subscribers to the trainer
def trainer_subscribers(request):
    trainer = models.Trainer.objects.get(pk=request.session['trainerid'])
    trainer_subs = models.AssignSubscriber.objects.filter(trainer=trainer).order_by('-id')

    return render(request, 'trainer/trainer_subscribers.html', {'trainer_subs' : trainer_subs})


# Assigned payments list
def trainer_payments(request):
    trainer = models.Trainer.objects.get(pk=request.session['trainerid'])
    trainer_pays = models.TrainerSalary.objects.filter(trainer=trainer).order_by('-id')

    return render(request, 'trainer/trainer_payments.html', {'trainer_pays' : trainer_pays})


# Trainer - Change Password
def trainer_change_password(request):
    msg = None

    if request.method =='POST':
        new_password = request.POST['new_password']
        update_response = models.Trainer.objects.filter(pk=request.session['trainerid']).update(password=new_password)

        if update_response:
            msg = "Password Changed Successfully"
            del request.session['trainerid']
            return redirect('/trainerlogin')
        else:
            msg = "Password Change Failed"

    form = forms.TrainerChangePasswordForm

    return render(request, 'trainer/trainer_change_password.html', {'form' : form, 'msg': msg})


# Trainer Notifications
def trainer_notifs(request):
    data = models.TrainerNotification.objects.all().order_by('-id')
    trainer=models.Trainer.objects.get(id = request.session['trainerid'])

    notifStatus = False
    jsonData = []
    totalUnread = 0

    for d in data:
        try:
            notifStatusData = models.NotifTrainerStatus.objects.get(trainer=trainer, notif=d)
            if notifStatusData:
                notifStatus: True
        except models.NotifTrainerStatus.DoesNotExist:
            notifStatus = False

        # Count the uread notifs
        if not notifStatus:
            totalUnread = totalUnread + 1

        jsonData.append({
            'pk': d.id,
            'notify_detail': d.notify_msg,
            'notifStatus': notifStatus
        })

    return render(request, 'trainer/notifs.html', {'notifs' : data, 'totalUnread': totalUnread})


# Trainer Messages
def trainer_msgs(request):
    data = models.TrainerMessage.objects.all().order_by('-id')

    return render(request, 'trainer/messages.html', {'msgs' : data})