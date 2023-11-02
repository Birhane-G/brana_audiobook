# Brana Audiobook API Documentation
### Introduction
This document provides detailed documentation for the Brana Audiobook API. The API allows users to access and manage user profile, including retrieving audiobooks, , updating information, and more.
### Base URL
The base URL for accessing the Brana Audiobook API is: 
       ```https://app.berana.app/api/method/```
### End Points
### Authentication
All API requests require authentication using an API key.
Endpoint: ```brana_audiobook.api.auth_api.login```
###### Request
    HTTP Method: POST
    Parameters: Identifire and Password
###### Response
    HTTP Status Code: 200 OK
    Content-Type: application/json
###### Response Body
    The response body will contain the details of the user Data in JSON format.
```{
    "message": {
        "user": "Administrator",
        "first_name": "Administrator",
        "middle_name": null,
        "last_name": null,
        "email": "admin@example.com",
        "user_profile": null
    },
    "home_page": "/app",
    "full_name": "Administrator"
    }
```
### AudioBooks
#### This Api retreive all Audiobook 
    ```https://app.berana.app/api/method/brana_audiobook.api.audiobook_api.retrieve_audiobooks```
    Endpoint: /audiobooks/latest
Request

    HTTP Method: GET
    Parameters: None

Response

    HTTP Status Code: 200 OK
    Content-Type: application/json

Response Body

The response body will contain the details of the latest audiobook in JSON format.

Example:
#### This Api Retrive single Audiobook based on Audiobook Title 
    ```https://app.berana.app/api/method/brana_audiobook.api.audiobook_api retrieve_audiobookaudiobook_id=መተዋወቂያ```
#### This Api Retrive Recommended Audiobooks 
    ```https://app.berana.app/api/method/brana_audiobook.api.audiobook_api.retrieve_recommended_audiobooks```
#### This Api Retrive Editors Picks Audiobooks 
    ```https://app.berana.app/api/method/brana_audiobook.api.audiobook_api.retrieve_editors_picks```
#### This Api Retrive All Genres And Number of Audiobooks  
    ```https://app.berana.app/api/method/brana_audiobook.api.audiobook_api.retreive_audiobook_genres```
#### This Api Retrive Audiobooks based on Genre 
    ```https://app.berana.app/api/method/brana_audiobook.api.audiobook_api.retreive_audiobook_genre?audiobook_genre=Historical Fiction```
#### This Api play Audiobooks Sample based on Audiobook Name  
    ```https://app.berana.app/api/method/brana_audiobook.api.audiobook_api.audiobook_sample?audiobook_id=መተዋወቂያ```
#### This Api play Audiobook Chapters based on Chapter Title
    ```https://app.berana.app/api/method/brana_audiobook.api.audiobook_api.play_audiobook_chapter?audiobook_chapter=ሚፈልግ ሰው```
### Authors
#### This Api list All Authors
    ```https://app.berana.app/api/method/brana_audiobook.api.authors_api.retrive_authors```
#### This Api retreive Author, No of Books, Image 
    ```https://app.berana.app/api/method/brana_audiobook.api.authors_api.retrieve_author?author_id=ገነነ መኩሪያ```
### Podcasts
    ```https://app.berana.app/api/method/brana_audiobook.api.podcast_api.retrieve_podcasts```
