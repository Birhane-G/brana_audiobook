# Brana Audiobook API Documentation
### Introduction
This document provides detailed documentation for the Brana Audiobook API. The API allows users to access and manage user profile, including retrieving audiobooks, , updating information, and more.
##### Base URL
The base URL for accessing the Brana Audiobook API is: 
       ```https://app.berana.app/api/method/```
#### End Points
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
    Example:
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
This api endpoint allows you to retrieve all audiobook available in the Brana Audiobook collection.
Endpoint: ```brana_audiobook.api.audiobook_api.retrieve_audiobooks```
###### Request
    HTTP Method: GET
    Parameters: None
###### Response
    HTTP Status Code: 200 OK
    Content-Type: application/json
###### Response Body
    The response body will contain list Audiobooks and Chapters in JSON format.
    Example:
```{
     {
            "title": "መተዋወቂያ",
            "description": "ደንበኛው በጣም አስፈላጊ ነው, ደንበኛው በደንበኛው ይከተላል. ተጫዋቾቹ እድለኞች እስኪሆኑ ድረስ, ካሲኖው በህይወት የተሞላ ነው, እና አየር መንገዱ ንጹህ ነው. የእኔ ሁለቱ ኩርባዎች ነፍሰ ጡር ናቸው። ሞሪሺያን ነበር፣ ሁልጊዜም በፎቶግራፍ የተማረከ፣ ሁልጊዜም የሕይወት አልጋ። ለዚያ የአልጋ አባላት፣ በወቅቱ የሳቅ አካል፣ የቅርጫት ኳስ ገንዳ። አሁን የምድር መንኮራኩሮች ያጌጡ ናቸው, ነገር ግን ሸለቆው ያማልላል. ለህፃናት ግን ካሲኖው ነፃ ነው, ይህ ንጹህ ታሪክ ነው. ሁል ጊዜ ቀላል መሆን ከሚፈልግ ሰው ጋር ምንም አትጨነቅ። ቅስት ለመከታተል ጊዜው",
            "author": "Kebede Desta",
            "narrator": "Birhane Gabriel",
            "thumbnail": "https://app.berana.app/files/book6.webp",
            "Sample Audiobook": "ደንበኛው በጣም አስፈላጊ ነው",
            "duration": "7m 7s",
            "Total chapter": 2,
            "Total chapter Duration": "1m 26s",
            "chapters": [
                {
                    "title": "ሚፈልግ ሰው",
                    "duration": 31.957
                },
                {
                    "title": "ቅስት ለመከታተል ጊዜው",
                    "duration": 54.909
                }
            ]
        }
    }
```
#### Audiobook
This api endpoint allows you to retrieve audiobook from Brana Audiobook collection.
Endpoint: ```brana_audiobook.api.audiobook_api retrieve_audiobook```
###### Request
    HTTP Method: GET
    Parameters: audiobook_id
###### Response
    HTTP Status Code: 200 OK
    Content-Type: application/json
###### Response Body
    The response body will contain Audiobook and It's Chapters in JSON format.
    Example:
```
{
    "message": {
        "title": "መተዋወቂያ",
        "author": "Kebede Desta",
        "narrator": "Birhane Gabriel",
        "thumbnail": "https://app.berana.app/files/book6.webp",
        "Sample Audiobook": "ደንበኛው በጣም አስፈላጊ ነው",
        "duration": "7m 7s",
        "description": "ደንበኛው በጣም አስፈላጊ ነው, ደንበኛው በደንበኛው ይከተላል. ተጫዋቾቹ እድለኞች እስኪሆኑ ድረስ, ካሲኖው በህይወት የተሞላ ነው, እና አየር መንገዱ ንጹህ ነው. የእኔ ሁለቱ ኩርባዎች ነፍሰ ጡር ናቸው። ሞሪሺያን ነበር፣ ሁልጊዜም በፎቶግራፍ የተማረከ፣ ሁልጊዜም የሕይወት አልጋ። ለዚያ የአልጋ አባላት፣ በወቅቱ የሳቅ አካል፣ የቅርጫት ኳስ ገንዳ። አሁን የምድር መንኮራኩሮች ያጌጡ ናቸው, ነገር ግን ሸለቆው ያማልላል. ለህፃናት ግን ካሲኖው ነፃ ነው, ይህ ንጹህ ታሪክ ነው. ሁል ጊዜ ቀላል መሆን ከሚፈልግ ሰው ጋር ምንም አትጨነቅ። ቅስት ለመከታተል ጊዜው"
    }
}
```
#### Recommended Audiobooks 
This api endpoint allows you to retrieve recommended audiobook from Brana Audiobook collection.
Endpoint: ```brana_audiobook.api.audiobook_api.retrieve_recommended_audiobooks```
###### Request
    HTTP Method: GET
    Parameters: None
###### Response
    HTTP Status Code: 200 OK
    Content-Type: application/json
###### Response Body
    The response body will contain Recommended Audiobook and It's Chapters in JSON format.
    Example:
```
{
    "message": {
        "title": "መተዋወቂያ",
        "author": "Kebede Desta",
        "narrator": "Birhane Gabriel",
        "thumbnail": "https://app.berana.app/files/book6.webp",
        "Sample Audiobook": "ደንበኛው በጣም አስፈላጊ ነው",
        "duration": "7m 7s",
        "description": "ደንበኛው በጣም አስፈላጊ ነው, ደንበኛው በደንበኛው ይከተላል. ተጫዋቾቹ እድለኞች እስኪሆኑ ድረስ, ካሲኖው በህይወት የተሞላ ነው, እና አየር መንገዱ ንጹህ ነው. የእኔ ሁለቱ ኩርባዎች ነፍሰ ጡር ናቸው። ሞሪሺያን ነበር፣ ሁልጊዜም በፎቶግራፍ የተማረከ፣ ሁልጊዜም የሕይወት አልጋ። ለዚያ የአልጋ አባላት፣ በወቅቱ የሳቅ አካል፣ የቅርጫት ኳስ ገንዳ። አሁን የምድር መንኮራኩሮች ያጌጡ ናቸው, ነገር ግን ሸለቆው ያማልላል. ለህፃናት ግን ካሲኖው ነፃ ነው, ይህ ንጹህ ታሪክ ነው. ሁል ጊዜ ቀላል መሆን ከሚፈልግ ሰው ጋር ምንም አትጨነቅ። ቅስት ለመከታተል ጊዜው"
    }
}
```
#### Editors Picks Audiobooks
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


## Conclusion
This document has provided an overview of the Brana Audiobook API, including the available endpoints for