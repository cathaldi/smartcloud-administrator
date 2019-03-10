# SmartCloud-admin-api

An unofficial python api for helping to administer with IBM Smartcloud
which supports products like Connections, Sametime and Notes.

## Setup
    pip install smartcloud-admin-api


## Getting Started

### Config
Define datacenter credentials 

    from bssapi import Organization
    from bssapi.bss_config import BssConfig

    # Provide North American data center details and supply user credentials
    config = BssConfig()
    config.add_datacenter("NA", "https://apps.na.collabserv.com", (email_address, password))

    # Create an Organization object for organization id 11111111 on NA
    my_org = Organization.get("NA", "11111111")

More examples and documentation can be found here.