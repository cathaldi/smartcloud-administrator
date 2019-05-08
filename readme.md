# SmartCloud Administrator

An unofficial python api for helping to administer with IBM Smartcloud
which supports products like Connections, Sametime and Notes.

Package is based on [BSS API documentation](https://www-10.lotus.com/ldd/appdevwiki.nsf/xpAPIViewer.xsp?lookupName=API+Reference)

Package Documentation can be found here on [read the docs](https://smartcloud-administrator.readthedocs.io/en/latest/).

## Setup
    pip install smartcloudadmin


## Getting Started

### Config
Define datacenter credentials 

    from smartcloudadmin import Organization
    from smartcloudadmin.config import BssConfig
    import os
    
    config = BssConfig()
    config.add_datacenter("NA", "https://apps.na.collabserv.com", (os.environ.get("BSS_USER"),
                                                                         os.environ.get("BSS_PASSWORD")))
                                                                         

Retrieve an Organization

    my_organization = Organization.get("NA", 123456)
    
    print(my_organization.state)
    >>> ACTIVE
    
    print(my_organization.security_realm)
    >>> FEDERATED
    
    print(my_organization.is_guest)
    >>> False
    
Add a new user, entitle them and set a one time password
    
    user = my_organization.add_subscriber(email_address="user_1@ibm.com, given_name="John", family_name="Doe")
    user.entitle(987654)  # Entitle user with subscription id 987654
    user.set_one_time_password("Test1Test")
    

Suspend the new user
    
    user.suspend()    
