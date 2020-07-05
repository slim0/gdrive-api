#!/usr/bin/env python
# coding: utf8

from __future__ import print_function
from apiclient import errors


def print_about(service, fields="*"):
    """
    Print all information about the active user (storage limit, quota...)
    It is possible to specify a specific field with field argument.
    for exemple : 
        print_about(service, fields="user")
    """

    try:    
        response = service.about().get(fields=fields).execute()
        return response
    except errors.HttpError as error:
        raise error


def get_files(service, location="root", nb=100):
    """
    Affiche les 'n' premiers fichiers auquels l'utilisateur à accès, 
    y compris les fichiers qui lui sont partagé.
    Par défaut, get_files affichera les 100 premiers fichiers à la racine du user.
    Mais il est possible de modifier le comportement grâce aux attributs location et nb : 
    - la valeur de nb indiquera le nombre de fichiers à scanner
    - Pour location, 3 valeur possibles : 
        - "all" affiche tous les fichiers (y compris les shared)
        - "shared" affiche seulement les éléments partagés avec le user
        - "root" affiche les éléments à la racine du user (ceux dont il est propriétaire)
    """
    
    if location == "all":
        location = "name contains ''"
    elif location == "shared":
        location = "sharedWithMe"
    elif location == "root":
        location = "'root' in parents"
    else:
        location = "name contains ''"

    try:
        response = service.files().list(q=location,
                                        orderBy='folder, createdTime',
                                        pageSize=nb).execute()

        items = response.get('files', [])

        return items
    except errors.HttpError as error:
        raise error


def search_file(service, name, nb=100):
    """
    Permet de rechercher un fichier par son nom (parramètre 'name') dans un drive.
    Retourne une liste (max 100) des fichiers qui correspondent à la requête.
    voir l'utilisation des queries gdrive ici : https://developers.google.com/drive/api/v3/search-files
    """
    query = "name contains '{}'".format(name)

    try:
        response = service.files().list(q=query, orderBy='folder, createdTime',pageSize=nb).execute()
        items = response.get('files', [])
        return items
    except errors.HttpError as error:
        raise error


def full_search_file(service, fulltext, nb=100):
    """
    Identique à la fonction search_file, sauf que cette fonction recherche le parramètre 'fulltext' dans tous le fichier
    (nom et contenu).
    voir l'utilisation des queries gdrive ici : https://developers.google.com/drive/api/v3/search-files
    """
    query = "fullText contains '{}'".format(fulltext)

    try:
        response = service.files().list(q=query, pageSize=nb).execute()
        items = response.get('files', [])
        return items
    except errors.HttpError as error:
        raise error


def trash_file(service, file_id):
    """
    Move file into trash on GDRIVE where 'file_id' is the id of the file
    """
    
    body = {
        'trashed': True,
    }

    try:
        return service.files().update(body=body, 
                                      fileId=file_id).execute()
    except errors.HttpError as error:
        raise error


def delete_file(service, file_id):
    """
    Delete file on GDRIVE where 'file_id' is the id of the file.
    Cette fonction supprime complétement le fichier correspondant. 
    Préférez la fonction trash_file pour mettre un élément à la poubelle.
    """
    try:
        return service.files().delete(fileId=file_id).execute()
    except errors.HttpError as error:
        raise error


def create_folder(service, parent_id, foldername):
    """Create Folder on GDRIVE
    Parameters : 
    parent_id : ID of the parent folder when we want to create our folder. If root: parent_id='root'
    foldername : Name of the folder we want to create
    """

    file_metadata = {
        'name': foldername,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id],
    }

    try:    
        response = service.files().create(body=file_metadata).execute()
        return response
    except errors.HttpError as error:
        raise error


def copy_file(service, origin_file, parents_list):
    """Copy an existing file.

    Args:
    service: Drive API service instance.
    origin_file: ID of the origin file to copy.
    copy_title: Title of the copy.

    Returns:
    The copied file if successful, None otherwise.
    """
    body = {
        "parents": parents_list,
        "name": origin_file['name']
    }

    try:
        return service.files().copy(
            fileId=origin_file['id'], body=body).execute()
    except errors.HttpError as error:
        raise error
    return None


def rename_file(service, file_id, new_name):    
    body = {
        'name': new_name,
    }

    try:
        return service.files().update(body=body,
                                      fileId=file_id).execute()
    except errors.HttpError as error:
        raise error


def mkdir_gdrive(service, Tree, parent_id):
    """
    Create 'Tree' directory into 'parent_id' folder on GDRIVE.
    Tree should be a dictionnary that represent folder-tree
    """
    
    i = 0
    for key, val in Tree.items():
        file_metadata = {
            'name': key,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id],
        }

        try:
            results = service.files().create(body=file_metadata,
                                             fields='id').execute()
        except errors.HttpError as error:
            raise error

        new_parent_folder_id = str(results.get('id'))

        if i == 0:
            project_folder_id = new_parent_folder_id
        i = i + 1
        if isinstance(val, dict):
            mkdir_gdrive(service=service,
                         Tree=val,
                         parent_id=new_parent_folder_id)

    return project_folder_id


def share_file(service, file_id, email, sendNotificationEmail, role, type_):
    """Share Folder on GDRIVE
    Parameters : 
    - file_id : ID of the file when we want to share
    - email : email of the person we want to share the file with
    - sendNotificationEmail : True or False either if we want to send notification email
    - role : what permission will have the new user on the file (owner, organizer, 
    fileOrganizer, writer, reader)
    """

    body = {
        "role": role,
        "type": type_,
        "emailAddress": email
    }

    try:
        response = service.permissions().create(body=body,
                                                fileId=file_id,
                                                sendNotificationEmail=sendNotificationEmail).execute()
        return response
    except errors.HttpError as error:
        raise error


def get_shared_users(service, fileId):
    """
    Get the list of shared users on a specific file
    """

    try:
        shared_users = service.permissions().list(fileId=fileId, 
                                                  fields="nextPageToken, " \
                                                         "permissions(id,emailAddress,role)").execute()
        permissions = shared_users.get('permissions', [])
        return permissions
    except errors.HttpError as error:
        raise error


def delete_permission(service, fileId, permissionId):
    """
    Remove permission on file. 
    fileId : The ID of the file
    permissionId : the permissionId of the user on this file
    """
    
    try:
        service.permissions().delete(fileId=fileId, permissionId=permissionId).execute()
    except errors.HttpError as error:
        raise error


def duplicate_tree(service, list_of_folder_objects, parent_id, lst):
    """
    Fonction qui duplique une/des arborescences et retourne une 
    liste de tous les objets créé (avec mimeType, id, name...).
    Explication des paramètres : 
    - list_of_folder_objects : Il s'agit d'une liste contenant un dictionnaire par dossier à copier. 
    Chaque dictionnaire contient l'ID, le nom et le mimeType du dossier ou fichier à dupliquer.
    
    Voici la fonction permettant de récupérer ces informations pour 1 dossier :

    folder_to_copy = [service.files().get(fileId = my_folder_id, 
                                          fields = "id, name, mimeType").execute()] 

    """

    for item in list_of_folder_objects:
        if item['mimeType'] == "application/vnd.google-apps.folder":

            try:
                new_folder = create_folder(service=service,
                                           parent_id=parent_id,
                                           foldername=item['name'])
            except errors.HttpError as error:
                raise error

            new_folder["source_id"] = item["id"]
            lst.append(new_folder)

            query = "parents in '" + item["id"] + "'"

            response = service.files().list(q=query,
                                            fields="nextPageToken,"
                                                   " files(id, name, mimeType)").execute()

            children_items = response['files']

            if children_items:
                for element in children_items:
                    if element['mimeType'] != "application/vnd.google-apps.folder":
                        new_file = copy_file(service=service,
                                             origin_file=element,
                                             parents_list=[new_folder['id']])
                        new_file["source_id"] = element["id"]
                        lst.append(new_file)

            duplicate_tree(service=service,
                           list_of_folder_objects=children_items,
                           parent_id=new_folder['id'],
                           lst=lst)
    return lst


def add_parent(service, file_id, parent_id):
    """
    Permet de créer l'équivalent d'un raccourcis (en stockage objet) d'un fichier ou dossier dans un autre dossier.
    voir : https://developers.google.com/drive/api/v3/reference/files/update
    :param service: service google ayant les droits sur les scopes necessaires.
    :param file_id: id du fichier ou dossier à qui on souhaite ajouter un parent (équivalent d'un raccourcis)
    :param parent_id: id du ou des dossiers parents, séparés par une virgule, à ajouter
    :return: http response
    """

    try:
        response = service.files().update(fileId=file_id,
                                          addParents=parent_id).execute()
        return response
    except errors.HttpError as error:
        raise error


def get_file_infos(service, file_id):
    """
    Permet de récupérer toutes les informations sur un fichier via son ID Gdrive
    :param service: service: service google ayant les droits sur les scopes necessaires.
    :param file_id: id du fichier
    :return: http response
    """
    try:
        response = service.files().get(fileId=file_id,
                                       fields="*").execute()
        return response
    except errors.HttpError as error:
        raise error


def change_owner(service, file_id, email):
    """
    Permet de changer le propriétaire sur un dossier fichier GDrive
    :param service: service Gdrive
    :param file_id: UUID du fichier
    :param email: email de la personne qui sera le nouveau propriétaire
    :return: Dictionnaire
    """

    body = {
        "role": "owner",
        "type": "user",
        "emailAddress": email
    }

    try:
        response = service.permissions().create(body=body,
                                                fileId=file_id,
                                                sendNotificationEmail=True,
                                                transferOwnership=True).execute()
        return response
    except errors.HttpError as error:
        raise error
