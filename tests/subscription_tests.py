from bssapi.utils.generators import given_name,family_name,email_address
import unittest


##### This block ensures tests run in order.
def cmp(a, b):
    return (a > b) - (a < b)
unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: cmp(x, y)


class TestSubscription(unittest.TestCase):

    my_sub = None
    test_org = None

    @classmethod
    def setUpClass(cls):
        first_name = given_name()
        familiy_name = family_name()
        admin_email = email_address(given_name=first_name,family_name=familiy_name,org_name="bss-api-bvt")
        # created_org = Organization.create(environment="SP1",organisation_name="bss-api-bvt", given_name=first_name,
        #                                                 family_name=familiy_name, admin_email=admin_email)
        # cls.test_organisation_id = created_org.id
        # cls.test_org = created_org
        # cls.my_sub = created_org.add_subscription("D0NPULL", 33)

