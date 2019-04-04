Examples
========

Activate any user in a Pending state and set a temporary password
-----------------------------------------------------------------

.. code-block:: python

    # BSS Config
    config = BssConfig()
    config.add_datacenter("NA", "https://apps.na.collabserv.com", (os.environ.get('BSS_USER'), os.environ.get('BSS_PASSWORD')))

Create a datacenter configuration. This is specified when retrieving new objects with the get method.
Additional Example:
.. code-block:: python

    Subscription.get("CE", 1234567)
    Subscriber.get("AP", 7654321)

.. code-block:: python

    my_org = Organization.get("NA", 1234567)
    pending_subscribers = my_org.filter_subscribers(attribute="state", attribute_value="PENDING",passed_operator=operator.eq)
    for subscriber in pending_subscribers:
        subscriber.activate()
        subscriber.setOneTimePassword("users_temp_password")


Returns subscribers that were modified within the last 7 days
-------------------------------------------------------------
.. code-block:: python

    recently_modified = my_org.filter_subscribers(attribute="modified", attribute_value=LAST_WEEK,passed_operator=operator.ge)

Returns subscribers that are currently in a PENDING state and may require attention
-----------------------------------------------------------------------------------
.. code-block:: python

    my_org.filter_subscribers(attribute="state", attribute_value="PENDING",passed_operator=operator.eq)


Create an organisation, add Connections S2 and activate users with a password
-----------------------------------------------------------------------------
.. code-block:: python

    org = Organization.create("A3", "Neat_new_company", "admin_email@ibm.com", "John", "Smith")

    # Create a Connections subscription
    connections_subscription = org.add_subscription("D0NPULL", "100")

    for lp in range(100):
        try:
             subscriber = org.add_subscriber()
             subscriber.entitle(connections_subscription.id)
             subscriber.activate()
             subscriber.set_one_time_password("Test1Test")
             subscriber.change_password("temp_password123", "final_password123")
         except Exception as e:
             logger.warn(e)

    admin = Subscriber.get("A3", email_address="admin_email@ibm.com")
    admin.activate()
    admin.set_one_time_password("temp_password123")
    admin.change_password("temp_password123", "final_password123")


