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
    from smartcloudadmin.bss_config import BssConfig

    # Provide North American data center details and supply user credentials
    config = BssConfig()
    config.add_datacenter("NA", "https://apps.na.collabserv.com", (email_address, password))

    # Create an Organization object for organization id 11111111 on NA
    my_org = Organization.get("NA", "11111111")
