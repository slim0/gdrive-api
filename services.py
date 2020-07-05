#!/usr/bin/env python
# coding: utf8

import os
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Please take a look at Google API documentation to setup scopes depend on what you want (cf README)
# scopes = ["https://www.googleapis.com/auth/drive", ]

# Path to the downloaded json credentials of your service account (see google documentation and ReadMe)
SERVICE_ACCOUNT_CREDENTIALS_FILE = "/path/to/credentials.json"


def get_service(scopes, api, user_email=None):
    """
    Build Google service depends on scopes and API you need
    @param scopes: list of Google scopes you need for your service
    drive scopes: https://developers.google.com/drive/api/v2/about-auth#OAuth2Authorizing
    sheets scopes: https://developers.google.com/sheets/api/guides/authorizing#OAuth2Authorizing
    @param api: Only compatible with "drive" or "sheet" for now.
    @param user_email: If you want to access a specific user's datas, you can specify his email (it should be in your
    GSuite domain). Else, function will return Google service of your service account.
    @return: Google service for your service account, or for a specific user if user_email parameter was filled in.
    """
    available_api = ('drive', 'sheets')
    if api not in available_api:
        raise ValueError("'{}' not in {}".format(api, available_api))

    credentials_service_account = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_CREDENTIALS_FILE,
        scopes=scopes)
    credentials = credentials_service_account

    if user_email:
        credentials = credentials_service_account.with_subject(user_email)

    if api == "drive":
        service = build('drive', 'v3', credentials=credentials)
    else:  # api == "sheets"
        service = build('sheets', 'v4', credentials=credentials)

    return service
