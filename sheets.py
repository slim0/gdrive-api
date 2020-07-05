#!/usr/bin/env python
# coding: utf8

from __future__ import print_function
from apiclient import errors


def spreadsheet_update_cells(service, spreadsheetId, range_, valuesList):
    """
    Permet d'écrire une valeur dans une cellule d'un spreadsheet.

    - La propriété "range_" s'écrit s'écrit sous la forme : NomDeLaFeuille!cell (ex: Feuille_1!A10)
    - La propriété "valuesList" doit être une liste (si plusieurs valeurs,
    elles seront écrite dans les cellules suivante)
    - La propriété "value_input_option" determine comment la data est interprétée.
    Deux valeurs sont possible : 'RAW' ou 'USER_ENTERED'
    La deuxième agit comme si c'était un utilisateur qui avait écrit dans la cellule.
    "=3+2" agira donc comme une formule par exempl !
    """

    value_input_option = 'RAW'

    value_range_body = {"values": [valuesList]}

    try:
        response = service.spreadsheets().values().update(spreadsheetId=spreadsheetId,
                                                          range=range_,
                                                          valueInputOption=value_input_option,
                                                          body=value_range_body).execute()
        return response
    except errors.HttpError as error:
        raise error


def protect_spreadsheet_element(service,
                                sheet_id,
                                spreadsheet_id,
                                warningOnly,
                                requestingUserCanEdit,
                                UsersList=[],
                                **kwargs):
    """
    Function use to protect element into a spreadhseet. It could be a cell, a range of cells or an entire sheet.
    Parameters :
    - sheet_id : Could be find with 'get_spreadsheet_info' function
    - warningOnly : True if you want that the cell can be edit but print a warning to the user
    requestingUserCanEdit : True if the user who requested this protected range can edit
    the protected area. This field is read-only.
    - UsersList : List of users email. Is empty by default if not giving
    - **kwargs : You can give the 'position' parameter. It must be a tuple with 4 int value.
    position = (startRowIndex, endRowIndex, startColumnIndex, endColumnIndex)
    If you don't use this parameter, the entire sheet will be protect.
    """

    protect_range = {"sheetId": sheet_id}

    for key, value in kwargs.items():
        if key == "position":
            protect_range["startRowIndex"] = value[0]
            protect_range["endRowIndex"] = value[1]
            protect_range["startColumnIndex"] = value[2]
            protect_range["endColumnIndex"] = value[3]

    body = {
        "requests": [
            {
                "addProtectedRange": {
                    "protectedRange": {
                        "range": protect_range,
                        "description": "Protected with Project Manager",
                        "warningOnly": warningOnly,
                        "requestingUserCanEdit": requestingUserCanEdit,
                        "editors": {"users": UsersList}}
                }
            }
            ]
        }

    try:
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body).execute()
        return response
    except errors.HttpError as error:
        raise error


def hide_spreadsheet_column(service, spreadsheet_id, sheet_id, column_index, hiddenByUser):
    """
    Permet de masquer ou afficher une colonne d'un spreadhseet.
    Attention, la première colonne (colonne A) à pour index 0 et non pas 1
    HiddenByUser : True ou False
    """
    requests = {
        'updateDimensionProperties': {
            "range": {
                "sheetId": sheet_id,
                "dimension": 'COLUMNS',
                "startIndex": column_index,
                "endIndex": column_index + 1,
                },
            "properties": {
                "hiddenByUser": hiddenByUser,
            },
            "fields": 'hiddenByUser',
            }
        }

    body = {'requests': requests}

    try:
        response = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                                      body=body).execute()
        return response
    except errors.HttpError as error:
        raise error


def get_spreadsheet_info(service, spreadsheet_id, ranges):
    # "ranges" s'écrit sous la forme ["my sheet!D9:D10", "my sheet!E12:E18"]

    # True if grid data should be returned.
    # This parameter is ignored if a field mask was set in the request.
    include_grid_data = True  # True if grid data should be returned

    request = service.spreadsheets().get(spreadsheetId=spreadsheet_id,
                                         ranges=ranges,
                                         includeGridData=include_grid_data)

    try:
        response = request.execute()

        # return full response but can be parsed. response is a 'dict'
        return response
    except errors.HttpError as error:
        raise error


def add_spreadsheet_sheet(service, spreadsheet_id, sheet_name, column_nb, row_nb):
    # "ranges" s'écrit sous la forme ["my sheet!D9:D10", "my sheet!E12:E18"]

    # True if grid data should be returned.
    # This parameter is ignored if a field mask was set in the request.
    body = {
        "requests": [
            {
                "addSheet": {
                    "properties": {
                        "title": sheet_name,
                        "gridProperties": {
                            "rowCount": row_nb,
                            "columnCount": column_nb
                            }
                        }
                    }
                }
            ]
        }

    try:
        response = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                                      body=body).execute()
        return response
    except errors.HttpError as error:
        raise error
