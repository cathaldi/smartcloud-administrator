Examples
========

Activate any user in a Pending state and set a temporary password
-----------------------------------------------------------------

.. code-block:: python

    my_org = Organization.get(1213232)
    pending_subscribers = my_org.filter_subscribers(attribute="state", attribute_value="PENDING",passed_operator=operator.eq)
    for subscriber in pending_subscribers:
        subscriber.activate()
        subscriber.setOneTimePassword("users_temp_password")


Returns subscribers that were modified within the last 7 days
-------------------------------------------------------------
.. code-block:: python

    my_org.filter_subscribers(attribute="modified", attribute_value=LAST_WEEK,passed_operator=operator.ge)

    for user in my_org.subscribers:
        if user.state != "PENDING":
            print(user.email + " : " + user.state)

    this could also be done with a filter
    my_org.filter_subscribers(attribute="state", attribute_value="PENDING",passed_operator=operator.ge)


Create an organisation, add Connections S2 and ICEC subscriptions
-----------------------------------------------------------------
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


Get print each user in an org in the format username, city
----------------------------------------------------------
.. code-block:: python

    for subscriber_id,subscriber in org.subscribers.items():
        f = open("user_list .txt", "a")
        f.write(f"{subscriber.email},Pa88w0rd\n")
