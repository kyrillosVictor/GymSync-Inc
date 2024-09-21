from django import template
from main.models import Subscription, SubPlan
from django.contrib.auth.models import User
from datetime import date

register = template.Library()

# Check if package is purchased
@register.simple_tag
def check_user_package(user_id, plan_id):

    user = User.objects.get(id=user_id)
    plan = SubPlan.objects.get(id=plan_id)
    check_package = Subscription.objects.filter(user=user, plan=plan).count()

    if check_package > 0:
        return True
    else:
        return False


# Check if package validity and the remaining days in the subscription
@register.simple_tag
def check_pckg_validity(user_id, plan_id):

    expired = False
    pending_days = None
    pckg_validity = None

    user = User.objects.get(id=user_id)
    plan = SubPlan.objects.get(id=plan_id)
    check_package = Subscription.objects.filter(user=user, plan=plan).count()

    if check_package > 0:
        pckg_data = Subscription.objects.filter(user=user, plan=plan).order_by('-id').first()
        today =  date.date.today()
        purchase_date = pckg_data.reg_date
        pending_days = (today-purchase_date).days
        pckg_validity = pckg_data.plan.valid_days

        if  pending_days > pckg_validity:
            expired = True

    else:
        expired = False

    return expired