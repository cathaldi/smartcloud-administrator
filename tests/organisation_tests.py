from smartcloudadmin.models.organization import Organization
from smartcloudadmin.models.subscription import Subscription
from smartcloudadmin.models.subscriber import Subscriber
from smartcloudadmin.utils.generators import given_name,family_name,email_address
from smartcloudadmin.exceptions import BssResourceNotFound, BSSBadData
import unittest
from smartcloudadmin.enums import State
from time import sleep
from random import randint
import os
from smartcloudadmin.config import BssConfig

##### This block ensures tests run in order.
def cmp(a, b):
    return (a > b) - (a < b)
unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: cmp(x, y)


class TestOrganisation(unittest.TestCase):

    my_sub = None
    test_org = None
    test_subscriber = None
    config = BssConfig()
    config.log_level = "dgdsgsdgsd"
    config.add_datacenter("TEST", os.environ.get("url"), (os.environ.get("username"), os.environ.get("password")))

    @classmethod
    def setUpClass(cls):
        number = "%05d" % randint(0, 99999)
        first_name = given_name()
        familiy_name = family_name()
        admin_email = email_address(given_name=first_name, family_name=familiy_name, org_name=f"bss-api-bvt-{number}")
        created_org = Organization.create(environment="TEST", organisation_name=f"bss-api-bvt-{number}", given_name=first_name,
                                          family_name=familiy_name, admin_email=admin_email, address_line_1=" ",
                                          city="Cork", address_type="billing", country="Ireland")
        cls.test_organisation_id = created_org.id
        cls.test_org = created_org
        cls.my_sub = created_org.add_subscription(part_number="D0NPULL", duration_length=8, duration_units="MONTHS", part_quantity=20 )
        print("my_test_user" + number + ".isc4sb.com")
        cls.test_subscriber = cls.test_org.add_subscriber(given_name="tod", family_name="todd", email_address="my_test_user" + number + "@isc4sb.com")

    def test_01_get_organisation(self):
        tested_org = Organization.get("TEST", self.test_org.id)    #502212451   # self.test_organisation_id
        assert(tested_org.id == self.test_org.id)

    def test_02_suspend_organisation(self):
        self.test_org.suspend()
        assert(self.test_org.state == State.SUSPENDED.value)

        # activate admin

    def test_03_unsuspend_organisation(self):
        self.test_org.unsuspend()
        assert(self.test_org.state == State.ACTIVE.value)

    def test_04_add_subscription_via_organisation(self):
        test_org_subscription = self.test_org.add_subscription(part_number="D0NPULL", part_quantity=16,
                                                               duration_length=10, duration_units="MONTHS")  # todo: Maybe use this in the next tests
        assert(test_org_subscription.state == State.ACTIVE.value)  # subscription is activated
        assert(self.test_org.subscriptions.get(test_org_subscription.id) == test_org_subscription)  # sub added to dict

    def test_05_cancel_subscription_via_organisation(self):
        test_org_subscription = self.test_org.add_subscription(part_number="D0NPULL", part_quantity=16,
                                                               duration_length=10, duration_units="MONTHS")
        self.test_org.remove_subscription(test_org_subscription)

        # test_org_subscription.delete()  todo: make this a new test.
        # assert(test_org_subscription.state == State.UNSET.value)
        assert(self.test_org.subscriptions.get(test_org_subscription.id, "") == "")  # sub should not be in the sub list

    def test_06_transfer_seat(self):
        number = "%05d" % randint(0, 99999)
        print("-")
        new_subscription = self.test_org.add_subscription(part_number="D0NRILL", part_quantity=16,
                                                          duration_length=10, duration_units="MONTHS")
        new_subscriber = self.test_org.add_subscriber(given_name="James", family_name="Johnson",
                                                      email_address="my_test_user" + number + "@isc4sb.com")
        new_subscriber.entitle(new_subscription.id)
        new_subscription._get_details()
        print("-")
        source_pre_transfer_available_seats = new_subscription.available_numbers_of_seats
        sleep(3)  # seems to be a delay with update sometimes.
        seat = new_subscriber.seat_set[new_subscription.id]
        new_subscription.transfer_seat(seat.id, self.my_sub.id)
        new_subscription._get_details()
        source_post_transfer_available_seats = new_subscription.available_numbers_of_seats
        print(f"{source_pre_transfer_available_seats} < {source_post_transfer_available_seats}")
        assert(source_pre_transfer_available_seats < source_post_transfer_available_seats)
    #
    # todo: add a range of roles

    # def test_07_assign_role_to_new_user_via_organisation(self):  #
    #     subscriber = self.test_org.add_subscriber()
    #     subscriber.activate()
    #     subscriber.assign_role("CustomerAdministrator")
    #     print(subscriber.get_role_list())
    #     assert("CustomerAdministrator" in subscriber.get_role_list())

    def test_07_assign_role_to_new_user_via_organisation(self):
        number = "%05d" % randint(0, 99999)
        new_sub_id = self.test_org.add_subscriber(given_name="James", family_name="Johnson",
                                                  email_address="my_test_user" + number + "@isc4sb.com").id
        self.test_org.subscribers.get(new_sub_id).activate()
        self.test_org.subscribers.get(new_sub_id).assign_role("CustomerAdministrator")
        assert("CustomerAdministrator" in self.test_org.subscribers.get(new_sub_id).get_role_list())

    def test_08_assign_already_assigned_role_via_organisation(self):  # todo: should there be a warning for this?
        number = "%05d" % randint(0, 99999)
        new_sub_id = self.test_org.add_subscriber(given_name="James", family_name="Johnson",
                                                  email_address="my_test_user" + number + "@isc4sb.com").id
        self.test_org.subscribers.get(new_sub_id).activate()
        self.test_org.subscribers.get(new_sub_id).assign_role("CustomerAdministrator")
        self.test_org.subscribers.get(new_sub_id).assign_role("CustomerAdministrator")
        assert("CustomerAdministrator" in self.test_org.subscribers.get(new_sub_id).get_role_list())

    def test_09_unassign_role_via_organisation(self):
        number = "%05d" % randint(0, 99999)
        subscriber = self.test_org.add_subscriber(given_name="James", family_name="Johnson",
                                                  email_address="my_test_user" + number + "@isc4sb.com")
        subscriber.activate()
        subscriber.unassign_role("User")
        assert("User" not in subscriber.get_role_list())

    def test_10_unassign_already_unassigned_role(self):
        number = "%05d" % randint(0, 99999)
        subscriber = self.test_org.add_subscriber(given_name="James", family_name="Johnson",
                                                  email_address="my_test_user" + number + "@isc4sb.com")
        subscriber.activate()
        subscriber.unassign_role("User")
        assert("User" not in subscriber.get_role_list())

    def test_11_suspend_subscription(self):
        self.my_sub.suspend()
        assert(self.my_sub.state == State.SUSPENDED.value)

    def test_12_unsuspend_subscription(self):
        self.my_sub.unsuspend()
        assert(self.my_sub.state == State.ACTIVE.value)

    def test_13_add_subscriber(self):
        number = "%05d" % randint(0, 99999)
        self.test_subscriber = self.test_org.add_subscriber(given_name="James", family_name="Johnson",
                                                            email_address="my_test_user" + number + "@isc4sb.com")
        assert(self.test_subscriber.state == State.PENDING.value)
        assert(self.test_org.subscribers.get(self.test_subscriber.id, None))

    def test_14_activate_org_user(self):
        number = "%05d" % randint(0, 99999)
        subscriber = self.test_org.add_subscriber(given_name="James", family_name="Johnson",
                                                  email_address="my_test_user" + number + "@isc4sb.com")
        subscriber.activate()
        assert(subscriber.state == State.ACTIVE.value)

    def test_15_password_set_one_time_and_check_24_wait(self):  # todo: check for exceptions.
        number = "%05d" % randint(0, 99999)
        subscriber = self.test_org.add_subscriber(given_name="James", family_name="Johnson",
                                                  email_address="my_test_user" + number + "@isc4sb.com")
        subscriber.activate()
        subscriber.set_one_time_password("basic4Password")
        subscriber.change_password("basic4Password", "MyBetterSaferPassword1!")
        assert(subscriber.state == State.ACTIVE.value)
        # Trying again within 24 hour wait period
        with self.assertRaises(BSSBadData):
            subscriber.change_password("MyBetterSaferPassword1!", "ReallyReallySecureWith0dd_ch4r4ct3rs_")

    def test_16_entitle_user(self):  # todo: check for exceptions.
        number = "%05d" % randint(0, 99999)
        subscriber = self.test_org.add_subscriber(given_name="James", family_name="Johnson",
                                                  email_address="my_test_user" + number + "@isc4sb.com")
        subscriber.entitle(self.my_sub.id)
        assert(self.my_sub.id in subscriber.entitlements)  # todo: better assertion needed

    def test_17_suspend_user(self):  # todo: check for exceptions.
        number = "%05d" % randint(0, 99999)
        subscriber = self.test_org.add_subscriber(given_name="James", family_name="Johnson",
                                                  email_address="my_test_user" + number + "@isc4sb.com")
        subscriber.activate()
        subscriber.suspend()
        assert(subscriber.state in State.SUSPENDED.value)

    def test_18_unsuspend_user(self):  # todo: check for exceptions.
        number = "%05d" % randint(0, 99999)
        subscriber = self.test_org.add_subscriber(given_name="James", family_name="Johnson",
                                                  email_address="my_test_user" + number + "@isc4sb.com")
        subscriber.activate()
        subscriber.suspend()
        subscriber.unsuspend()
        assert(subscriber.state in State.PENDING.value)

    def test_19_revoke_subscriber(self):  # todo: check for exceptions.
        number = "%05d" % randint(0, 99999)
        subscriber = self.test_org.add_subscriber(given_name="James", family_name="Johnson",
                                                  email_address="my_test_user" + number + "@isc4sb.com")
        subscriber_id = subscriber.id
        subscriber.entitle(self.my_sub.id)
        subscriber.revoke(self.my_sub.id)
        sleep(5)
        try:
            new_subscriber = Subscriber.get("TEST", subscriber_id=subscriber_id)
            print(new_subscriber.state)
        except BssResourceNotFound:
            print("excepto")
            state = ""

        assert(self.my_sub.id not in subscriber.entitlements)    # todo: better assertion needed

    def test_20_soft_delete_subscriber(self):  # todo: check for exceptions.
        number = "%05d" % randint(0, 99999)
        subscriber = self.test_org.add_subscriber(given_name="James", family_name="Johnson",
                                                  email_address="my_test_user" + number + "@isc4sb.com")
        subscriber.entitle(self.my_sub.id)
        subscriber.delete()
        assert(subscriber.state == State.SOFT_DELETED.value or subscriber.state == State.REMOVE_PENDING.value)

    def test_21_restore_soft_deleted_subscriber(self):  # todo: check for exceptions.
        number = "%05d" % randint(0, 99999)
        subscriber = self.test_org.add_subscriber(given_name="James", family_name="Johnson",
                                                  email_address="my_test_user" + number + "@isc4sb.com")
        subscriber.entitle(self.my_sub.id)
        subscriber.delete()
        if subscriber.state == State.SOFT_DELETED.value:  # we can't do much about it.
            subscriber.restore()
            assert(subscriber.state == State.ACTIVE.value)
        # In deregister pending - ignore. It's a BSSCore issue.

    # move it to another test. should be org, remove use
    def test_22_hard_delete_subscriber(self):  # todo: check for exceptions.
        number = "%05d" % randint(0, 99999)
        subscriber = self.test_org.add_subscriber(given_name="James", family_name="Johnson",
                                                  email_address="my_test_user" + number + "@isc4sb.com")
        subscriber.entitle(self.my_sub.id)
        subscriber.delete(soft_delete="false")

        assert(subscriber.state == State.UNSET.value)    # todo: remove pending or an exception is thrown.
        assert(self.test_org.subscribers.get(self.test_subscriber.id, None))

    def test_23_delete_subscription(self):
        temp_subscription = self.test_org.add_subscription(part_number="D0NPULL", duration_length=8, duration_units="MONTHS", part_quantity=20 )

        temp_subscription.delete()
        assert(temp_subscription.state == State.UNSET.value)


    # At this stage we should have 3 pending users
        # 1 pending admin and 2 pending users with no subscription.
            # entitle users and then activate admin using list


    # def test_24_compare_org_initiization_from_id_and_from_name(self):
    #     org_from_id = Organization.get("TEST", self.test_org.id)
    #     org_from_json = my_client.get_orgs("TEST", self.test_org.name)[0]
    #
    #     assert(org_from_id == org_from_json)

        # verify objects are equal regardless of how populated.
    def test_25_compare_org_initiization_from_new_org_and_org_id(self):
        number="%05d" % randint(0, 99999)
        first_name = given_name()
        familiy_name = family_name()
        admin_email = email_address(given_name=first_name, family_name=familiy_name, org_name=f"bss-api-bvt-{number}")
        created_org = Organization.create(environment="TEST", organisation_name=f"bss-api-bvt-{number}", given_name=first_name,
                                          family_name=familiy_name, admin_email=admin_email, address_line_1=" ",
                                          city="Cork", address_type="billing", country="Ireland")

        org_from_id = Organization.get("TEST", created_org.id)
        assert(org_from_id == created_org)

    def test_26_compare_subscriptions_initialisation_methods(self):  # case to be made to make split into 2 tests. check sub adds to list after add.
        new_sub = self.test_org.add_subscription(part_number="D0NPULL", duration_length=8, duration_units="MONTHS", part_quantity=20 )

        sub_from_list = self.test_org.subscriptions.get(new_sub.id)
        sub_from_id = Subscription.get("TEST", new_sub.id)

        assert(new_sub == sub_from_id == sub_from_list)

    def test_27_compare_subscribers_initialisation_methods(self):  # case to be made to make split into 2 tests. check sub adds to list after add.
        number="%05d" % randint(0, 99999)
        new_subscriber = self.test_org.add_subscriber(given_name="James", family_name="Johnson",
                                                      email_address="my_test_user" + number + "@isc4sb.com")

        subscriber_from_id = Subscriber.get("TEST", subscriber_id=new_subscriber.id)

        # Creates Org and gets details.
        org_from_id = Organization.get("TEST", new_subscriber.customer_id)
        subscriber_from_customer_list = org_from_id.subscribers.get(new_subscriber.id)

        assert(new_subscriber == subscriber_from_id == subscriber_from_customer_list)

    def test_28_update_org(self):
        tested_org = Organization.get("TEST", self.test_organisation_id)
        tested_org.check_for_updates()
        tested_org.add_subscription(part_number="D0NPULL", duration_length=8, duration_units="MONTHS", part_quantity=20 )

        assert(tested_org.id == self.test_org.id)


    def test_29_org_deletion(self):
        self.test_org.delete()
        assert(self.test_org.state is State.UNSET.value)


    # Exception handling tests
    def test_50_check_exception_organisation_not_found(self):
        with self.assertRaises(BssResourceNotFound):
            Organization.get("TEST", "045454")

    def test_51_check_exception_subscription_not_found(self):
        with self.assertRaises(BssResourceNotFound):
            Subscription.get("TEST", "045454")

    def test_52_check_exception_subscriber_not_found(self):
        with self.assertRaises(BssResourceNotFound):
            Subscriber.get("TEST", subscriber_id="045454")

    def test_53_check_exception_org_bad_data(self):
        with self.assertRaises(BSSBadData):
            Subscription.get("TEST", "safasfswa")

    def test_54_check_exception_subscription_bad_data(self):
        with self.assertRaises(BSSBadData):
            Subscriber.get("TEST", subscriber_id="safasfswa")

    def test_55_check_exception_subscriber_bad_data(self):
        with self.assertRaises(BSSBadData):
            Organization.get("TEST", "safasfswa")

    # Subscriber updates - NEEDS TO BE CHECKED.
    #
    #
    # test orgs that are deregister pending
    # test on orgs not found
    #
    #
    # update transactions need help
    #
    # #get admin
    #
    # activate admin.