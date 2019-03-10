Getting Started
===============

Install through pip

.. code-block:: python

   pip install smartcloudadmin

Retrieving an Organization

.. code-block:: python

    from smartcloudadmin import Organization
    from smartcloudadmin.bss_config import BssConfig

    # Provide North American data center details and supply user credentials
    config = BssConfig()
    config.add_datacenter("NA", "https://apps.na.collabserv.com", (email_address, password))

    # Create an Organization object for organization id 11111111 on NA
    my_org = Organization.get("NA", "11111111")

Entitle a user with a subscription

.. code-block:: python

    from smartcloudadmin import Subscriber
    # Get user from id
    new_subscriber = Subscriber.get("NA", 222222)
    # Or alternatively through email address
    # new_subscriber = Subscriber.get("NA", email="test_email@ibm.com")

    # Entitle the user with subscription Id 33333333
    new_subscriber.entitle(33333333)


