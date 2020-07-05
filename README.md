# gsuite-api
Bunch of functions that allows you to interact with GSuite API.

## Requirements
Before using the API, you'll need to:
- Create a Google service account. [https://cloud.google.com/compute/docs/access/service-accounts](https://cloud.google.com/compute/docs/access/service-accounts)
- Enable and configure Google API.
- Download the JSON credentials file of your service account, secure it and enter the path in the "SERVICE_ACCOUNT_CREDENTIALS_FILE" variable (services.py file)
- Install required libraries in your environment :
`pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
- Enable domain-wide delegation for the service account so it can access every users datas in your domain.

Please take a look at these links, they will help you with this: 
- [https://developers.google.com/gsuite/aspects/apis](https://developers.google.com/gsuite/aspects/apis)
- [https://developers.google.com/drive/api/v3/quickstart/python](https://developers.google.com/drive/api/v3/quickstart/python)
- [https://developers.google.com/sheets/api/quickstart/python](https://developers.google.com/sheets/api/quickstart/python)

## How to use it
Once everything is correctly has been correctly configured:

In your environment, launch a python console, and, for example:

```python
#!/usr/bin/env python
# coding: utf8
from services import *
from drive import *
from sheets import *

scopes = ["https://www.googleapis.com/auth/drive", ]
api = "drive"

service = get_service(scopes, api, user_email=None)
get_files(service)
# Should return the first the 100 first files of your service account 
```