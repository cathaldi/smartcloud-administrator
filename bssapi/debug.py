from bssapi import Organization
import time
import timeit
import operator
import sys
from bssapi.utils.qol import parse_time
from datetime import datetime, timedelta

from bssapi import Subscription
from bssapi import Subscriber

from bssapi.config import BssConfig

# todo: need to sort throttle management.

from datetime import datetime
startTime = datetime.now()
# todo: allow linking up of a custom templates folder.
#my_org = Organization("SP1", 21633066) #  20247356)

config = BssConfig()
config.add_datacenter("SP1", "https://apps.collabservsvtperf1.com", ("cathaldi@ie.ibm.com", "Constantinople1453"))
config.add_datacenter("I1", "https://apps.collabservintegration.com", ("cathaldi@ie.ibm.com", "Constantinople1453"))

print("test")
first_name = "cathal"
family_name= "Dinneen"
admin_email = "test_suspend_this_org_234343235823@ie.ibm.com"
# created_org = Organization.create(environment="SP1", organisation_name="suspend_org_test", given_name=first_name,
#                                   family_name=family_name, admin_email=admin_email)

created_org = Organization.get("SP1", 1000568562)

# sub_id = created_org.add_subscription("D0NPULL", 220)
# print(created_org.name)
sub_id = Subscription.get("SP1",1000072627)

# for admin_id, admin in created_org.admins.items():
#     admin.activate()

# for x in range(250):
# 
#         id = random.randint(1, 10000000)
#         my_user = created_org.add_subscriber(email_address=f"bss_suspend_test_active_user_{id}@isc4sb.com")
#         my_user.activate()
#         my_user.entitle(sub_id.id)
#         my_user.set_one_time_password("Test1Test")
#         my_user.change_password("Test1Test", "pa88w0rd")
#         print(x)


admin = Subscriber.get("I1", email_address="bssnralerts@ie.ibm.com")
admin.set_one_time_password("Test1Test")
admin.change_password("Test1Test", "CheshireCat1865")
# admin.activate()


# show a sample where failed users are added to a list.

# emtitle a user with all subs in an org
# for sub_id, subscription in my_org.subscriptions.items():
#     my_sub.entitle(subscription.id)

# get users with D0NPULL Subscriptions
# D0NPULL_list = []
# for sub_id, subscription in my_org.subscriptions.items():
#     if subscription.part_number == "D0NPULL":
#         D0NPULL_list.append(sub_id)
#
# print("DON PULL LIST")
# print(D0NPULL_list)
# return_list = []
# for subscriber_id, subscriber in my_org.subscribers.items():
#
#     S1 = set(subscriber.entitlements)
#     print(S1)
#     S2 = set(D0NPULL_list)
#     print(S2)
#     print(S1.intersection(S2))
#


# hanlded by filter list
# Show me all subscribers entitled with subscription 23434
# def get_users_with_sub_id(subscription_id):
#     print("checking users with sub 1000068294")
#     entitled = []
#     for subscriber_id, subscriber in my_org.subscribers.items():
#         entitled.append(subscriber) if subscription_id in subscriber.entitlements else _
#     return entitled
#
#
# print(get_users_with_sub_id(1001392642))




# print("-----")
# this_org_two = Organization.get("SP1", "502212451")
# print(this_org_two.is_ssm)
# print(this_org_two.last_sync_date)
# print(type(this_org_two.last_sync_date))
#
# print("+++++")
# this_org_three = Organization.get("SP1", "21606511")
# print(this_org_three.is_ssm)
# print(this_org_three.last_sync_date)
# print(type(this_org_three.last_sync_date))
# # created_org.suspend()
# print(created_org.state)
# created_org.unsuspend()
# print(created_org.state)
# created_org.delete()

# sub = Subscription.get("SP1", "1000055425")

# user_1 = Subscriber.get("SP1", email_address="bss_svt_user_0042972@isc4sb.com")
#
# user_2 = Subscriber.get("SP1", subscriber_id="1000455202")
#
#
# my_client = Client()



# my_org = Organization("SP1", 21633066)
# my_org.toJSON()

# my_org.check_for_updates()
# my_org.add_subscription("D0NPULL", 15)
# # my_org = Organization("SP1", "1000346857") 22 users
# my_org = Organization("SP1", "20247356") #1k users.
# my_org = Organization("SP1", "20320963") 10k users.
#
#
# print(my_org.subscriptions)
# print("+++++")
# list = my_org.filter_subscriptions(attribute="modified_epoch", attribute_value=parse_time("10/24/2016 12:27:46").timestamp(), passed_operator=operator.ne)
#
# print("----------")
# print(list)
# my_org.filter_subscriptions(attribute="state", attribute_value="ACTIVE", passed_operator=operator.eq)
#




#
# for key, admin in my_org.admins.items():
#     print(admin.email)
#
# LAST_WEEK = datetime.now() - timedelta(days=7)
#
#
# # Returns subscribers that were modified within the last 7 days ( last 168 hours )
# my_org.filter_subscribers(attribute="modified", attribute_value=LAST_WEEK,
#                           passed_operator=operator.ge)

# my_org.filter_subscribers(attribute="entitlements", attribute_value=1000068294,
#                           passed_operator=operator.contains())
#

#my_org.filter_subscribers


# get size of doesn't work.

# start_time = time.time()
# my_org = Organization.get("SP1", 1000346857)
#
# print(my_org.subscribers)

#
# current = time.time() - start_time

# for admin in my_org.admins:
#     print(admin.state + " " + admin.email)

# for user in my_org.subscribers:
#     if user.state != "PENDING":
#         print(user.email + " : " + user.state)

# filter_subscriptions
#
# filter_subscribers
# for user in my_org.subscribers:
#     print(user.is_guest)

# works
# my_org.filter_subscribers(attribute="is_guest", attribute_value=False)

# operator.lt(a, b)
# operator.le(a, b)
# operator.eq(a, b)
# operator.ne(a, b)
# operator.ge(a, b)
# operator.gt(a, b)

# my_org.filter_subscribers(attribute="state", attribute_value="PENDING", passed_operator=operator.ne)
# my_org.filter_subscribers(attribute="state", attribute_value="PENDING", passed_operator=operator.ne)
#
#

environment = {
    "SP1": {
        "url": "https://apps.collabservsvtperf1.com",
        "auth": ('cathaldi@ie.ibm.com', 'Constantinople1453')
    },
    "IR3": {
        "url": "https://apps.scniris.com",
        "auth": ('cathaldi@ie.ibm.com', 'Constantinople1453')
    },
    "I1": {
        "url": "https://apps.collabservintegration.com",
        "auth": ('cathaldi@ie.ibm.com', 'Constantinople1453')
    }
}
environment["A3"] = {}



# "SP1": {
#     "url": "https://apps.collabservsvtperf1.com",
#     "auth": ('cathaldi@ie.ibm.com', 'Constantinople1453')


# my_client = Client("https://apps.collabservsvtperf1.com", "Cathaldi@ie.ibm.com", "Constantinople1453")
#
# my_client.get_org("I1", 126)
#
# my_client = Client()
# my_org = Organization.get("SP1", 126)
# my_org = Organization.get("SP1", 21633066)