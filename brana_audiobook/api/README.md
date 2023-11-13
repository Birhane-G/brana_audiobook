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
### Registeration
This Api used to register user 
Endpoint: ```brana_audiobook.api.auth_api.signup```
###### Request
    HTTP Method: POST
    Parameters: firstname, lastname, email, phonenumber and Password
###### Response
    HTTP Status Code: 200 OK
    Content-Type: application/json
###### Response Body
    The response body will contain the details of the user Data in JSON format.
    Example:
```
    "message": {
        "message": "registered successfully Check Your Email",
        "user_data": {
            "firstname": "gemechis",
            "lastname": "kedir",
            "email": "testuser@gmail.com",
            "username": "gk"
        }
    },
    "home_page": "/me",
    "full_name": "gemechis kedir",
```
### User Profile
This Api used to retrieve User Profile based on user session
Endpoint: ```brana_audiobook.api.user_profile_api.retrieve_profile```
###### Request
    HTTP Method: POST
    Parameters: None
###### Response
    HTTP Status Code: 200 OK
    Content-Type: application/json
###### Response Body
    The response body will contain the details of the user in JSON format.
    Example:
```
{
    "message": {
        "email": "testuser@gmail.com",
        "first_name": "gemechis",
        "last_name": "kedir",
        "username": "gk",
        "profile_url": "https://app.berana.appNone"
    }
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
Endpoint: ```brana_audiobook.api.audiobook_api.retrieve_audiobook```
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
        "title": "ባርቾ",
        "description": "ሁሌም የገጠር ‹‹ዘመዶቻችን›› ሲመጡ እኔም፣ ታላቅ እህቴም፣ ታላቅ ወንድሜም እንከፋለን፡፡ ይሄንን ደግሞ ደብቀነው አናውቅም፡፡ ያውቃል፡፡ ጠንቅቆ ያውቃል፡፡ እኔ ግን ዛሬ ምን እንዲህ እንዳደረገው አላወቅኩም፡፡\nየገጠር ዘመዶቹን የማልወድበት ምክንያት ብዙ ነው፡፡\nአንደኛ፤ እንዲህ አይነት- ጫማው የሚሸት፣ ፀገሩ የማይበጠር፣ ልብሱ የማይታጠብ፣ በበረባሶ የሚሄድ- ዘመድ አለኝ ብዬ ማመን ዝቅ የሚያደርገኝ ስለሚመስለኝ፤ ((እህቴ ‹‹እነሱ ሁለት ሳምንት ቆይተው ሲሄዱ የጫማ ቸው ሽታ ግን ሁለት ወር ይቆያል›› እያለች ታስቀን ነበር)\nሁለተኛ፤ ዘመዶቻችን እኛ ቤት መጥተው ሲከርሙ ከአልጋዬም ከዘወትር ኑሮዬም ስለሚያፈናቅሉኝ (ለምሳሌ- እነሱ እንግሊዝኛ ስለማይገባቸው የቴሌቪዥን ፊልም እንዳይ አይፈቀድም፡፡ የሚከፈተው የአማርኛ ፕሮግራም ብቻ ነው፡፡)",
        "author": "ህይወት እምሻው",
        "narrator": "Natnael Tilaye",
        "thumbnail": "https://app.berana.app/files/book1.jpg",
        "Sample Audiobook Title": "ዘመዶቼ",
        "duration": "7m 24s",
        "total chapter": 3,
        "total chapter duration": "14m 45s",
        "chapters": [
            {
                "title": "ሰዎችን እንድታስቢ",
                "duration": "54s"
            },
            {
                "title": "ከዲሞክራሲያዊ መሪ",
                "duration": "6m 26s"
            },
            {
                "title": "ጆሮዬን እየጎተተና",
                "duration": "7m 24s"
            }
        ]
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
            "title": "ሌባሻይ",
            "description": "የዑንታ ወንዝ  ከላይ ከገሪማ  ተራራ  ሰው ይዞ  መጥቶ መንጅቦ ና  ቡሳሴ  ላይ አዝመራውን  የሚያጠፋው ጂኒዎች ሲጋቡ ነው  በተለይ ይህንን ክረምት  ጅኒዎች ሰርጋቸው በዝቷል  ሲጨፍሩ ነው የሚያድሩት እኔ ቋንቋ ቸውን  ስለማውቅ  የሚነጋገሩትን እሰማለሁ  ኩሪሚሪሚሪ..... ማለት በጅኒ ቋንቋ ሰውን  እንፍጅ \" ማለት ነው ፡፡ ያን  ሰአት  ድፋን ክፍ እንቅልፉን ሲለጥጥ እኔ  ከጅኒ ጋር ስዋጋ ነው የምድረው  የኮርማ  ደራሯ እመቤት  ከመፅሀፍ  የተወሰደ፡፡ ገፅ 400 ",
            "author": "ድርቡ አደራ",
            "narrator": "Abebe Balcha",
            "thumbnail": "https://app.berana.app/files/book2cbd491.jpeg",
            "sample audiobook title": null,
            "duration": "7m 24s",
            "total chapter": 0,
            "total chapter duration": "",
            "chapters": []
}
```
#### Editors Picks Audiobooks
This api endpoint allows you to retrieve editors picks audiobook from Brana Audiobook collection.
Endpoint: ```brana_audiobook.api.audiobook_api.retrieve_editors_picks```
###### Request
    HTTP Method: GET
    Parameters: None
###### Response
    HTTP Status Code: 200 OK
    Content-Type: application/json
###### Response Body
    The response body will contain editor picks Audiobook and It's Chapters in JSON format.
    Example:
```
{
            "title": "ባርቾ",
            "description": "ሁሌም የገጠር ‹‹ዘመዶቻችን›› ሲመጡ እኔም፣ ታላቅ እህቴም፣ ታላቅ ወንድሜም እንከፋለን፡፡ ይሄንን ደግሞ ደብቀነው አናውቅም፡፡ ያውቃል፡፡ ጠንቅቆ ያውቃል፡፡ እኔ ግን ዛሬ ምን እንዲህ እንዳደረገው አላወቅኩም፡፡\nየገጠር ዘመዶቹን የማልወድበት ምክንያት ብዙ ነው፡፡\nአንደኛ፤ እንዲህ አይነት- ጫማው የሚሸት፣ ፀገሩ የማይበጠር፣ ልብሱ የማይታጠብ፣ በበረባሶ የሚሄድ- ዘመድ አለኝ ብዬ ማመን ዝቅ የሚያደርገኝ ስለሚመስለኝ፤ ((እህቴ ‹‹እነሱ ሁለት ሳምንት ቆይተው ሲሄዱ የጫማ ቸው ሽታ ግን ሁለት ወር ይቆያል›› እያለች ታስቀን ነበር)\nሁለተኛ፤ ዘመዶቻችን እኛ ቤት መጥተው ሲከርሙ ከአልጋዬም ከዘወትር ኑሮዬም ስለሚያፈናቅሉኝ (ለምሳሌ- እነሱ እንግሊዝኛ ስለማይገባቸው የቴሌቪዥን ፊልም እንዳይ አይፈቀድም፡፡ የሚከፈተው የአማርኛ ፕሮግራም ብቻ ነው፡፡)",
            "Author": "ህይወት እምሻው",
            "narrator": "Natnael Tilaye",
            "thumbnail": "https://app.berana.app/files/book1.jpg",
            "sample audiobook title": "ዘመዶቼ",
            "duration": "7m 24s",
            "Total chapter": 3,
            "Total chapter Duration": "14m 45s",
            "chapters": [
                {
                    "title": "ሰዎችን እንድታስቢ",
                    "duration": "54s"
                },
                {
                    "title": "ከዲሞክራሲያዊ መሪ",
                    "duration": "6m 26s"
                },
                {
                    "title": "ጆሮዬን እየጎተተና",
                    "duration": "7m 24s"
                }
            ]
}
```
#### Genres
This api endpoint allows you to retrieve all genres, It's associated audiobooks, 5 thubnails and total number of audiobook from Brana Audiobook collection.
Endpoint: ```brana_audiobook.api.audiobook_api.retreive_audiobook_genres```
###### Request
    HTTP Method: GET
    Parameters: None
###### Response
    HTTP Status Code: 200 OK
    Content-Type: application/json
###### Response Body
    The response body will contain genres, thumbnails and total number of Audiobook in JSON format.
    Example:
```
{
    {
        "Genre Name": "Biography",
        "Audiobooks": 1,
        "thumbnail": [
            "https://app.berana.app/files/book6.webp"
            ]
    },
    {
        "Genre Name": "Thriller",
        "Audiobooks": 0,
        "thumbnail": []
    },
    {
        "Genre Name": "Fiction",
        "Audiobooks": 5,
        "thumbnail": [
            "https://app.berana.app/files/book4.jpeg",
            "https://app.berana.app/files/book3.jpg",
            "https://app.berana.app/files/book2cbd491.jpeg",
            "https://app.berana.app/files/book4.jpeg",
            "https://app.berana.app/files/book1.jpg"
        ]
    }
}
```
#### Genre 
This api endpoint allows you to retrieve Audiobook based on genre from Brana Audiobook collection.
Endpoint: ```brana_audiobook.api.audiobook_api.retreive_audiobook_genre?audiobook_genre=Fiction```
###### Request
    HTTP Method: POST
    Parameters: audiobook_genre
###### Response
    HTTP Status Code: 200 OK
    Content-Type: application/json
###### Response Body
    The response body will contain audiobooks in JSON format.
    Example:
```
{
    {
            "title": "ባርቾ",
            "description": "ሁሌም የገጠር ‹‹ዘመዶቻችን›› ሲመጡ እኔም፣ ታላቅ እህቴም፣ ታላቅ ወንድሜም እንከፋለን፡፡ ይሄንን ደግሞ ደብቀነው አናውቅም፡፡ ያውቃል፡፡ ጠንቅቆ ያውቃል፡፡ እኔ ግን ዛሬ ምን እንዲህ እንዳደረገው አላወቅኩም፡፡\nየገጠር ዘመዶቹን የማልወድበት ምክንያት ብዙ ነው፡፡\nአንደኛ፤ እንዲህ አይነት- ጫማው የሚሸት፣ ፀገሩ የማይበጠር፣ ልብሱ የማይታጠብ፣ በበረባሶ የሚሄድ- ዘመድ አለኝ ብዬ ማመን ዝቅ የሚያደርገኝ ስለሚመስለኝ፤ ((እህቴ ‹‹እነሱ ሁለት ሳምንት ቆይተው ሲሄዱ የጫማ ቸው ሽታ ግን ሁለት ወር ይቆያል›› እያለች ታስቀን ነበር)\nሁለተኛ፤ ዘመዶቻችን እኛ ቤት መጥተው ሲከርሙ ከአልጋዬም ከዘወትር ኑሮዬም ስለሚያፈናቅሉኝ (ለምሳሌ- እነሱ እንግሊዝኛ ስለማይገባቸው የቴሌቪዥን ፊልም እንዳይ አይፈቀድም፡፡ የሚከፈተው የአማርኛ ፕሮግራም ብቻ ነው፡፡)",
            "author": "ህይወት እምሻው",
            "narrator": "Natnael Tilaye",
            "thumbnail": "https://app.berana.app/files/book1.jpg",
            "sample audiobook title": "ዘመዶቼ",
            "duration": "7m 24s",
            "Total chapter": 3,
            "Total chapter Duration": "14m 45s",
            "chapters": [
                {
                    "title": "ሰዎችን እንድታስቢ",
                    "duration": "54s"
                },
                {
                    "title": "ከዲሞክራሲያዊ መሪ",
                    "duration": "6m 26s"
                },
                {
                    "title": "ጆሮዬን እየጎተተና",
                    "duration": "7m 24s"
                }
            ]
        },
        {
            "title": "ሌባሻይ",
            "description": "የዑንታ ወንዝ  ከላይ ከገሪማ  ተራራ  ሰው ይዞ  መጥቶ መንጅቦ ና  ቡሳሴ  ላይ አዝመራውን  የሚያጠፋው ጂኒዎች ሲጋቡ ነው  በተለይ ይህንን ክረምት  ጅኒዎች ሰርጋቸው በዝቷል  ሲጨፍሩ ነው የሚያድሩት እኔ ቋንቋ ቸውን  ስለማውቅ  የሚነጋገሩትን እሰማለሁ  ኩሪሚሪሚሪ..... ማለት በጅኒ ቋንቋ ሰውን  እንፍጅ \" ማለት ነው ፡፡ ያን  ሰአት  ድፋን ክፍ እንቅልፉን ሲለጥጥ እኔ  ከጅኒ ጋር ስዋጋ ነው የምድረው  የኮርማ  ደራሯ እመቤት  ከመፅሀፍ  የተወሰደ፡፡ ገፅ 400 ",
            "author": "ድርቡ አደራ",
            "narrator": "Abebe Balcha",
            "thumbnail": "https://app.berana.app/files/book2cbd491.jpeg",
            "sample audiobook title": null,
            "duration": "7m 24s",
            "Total chapter": 0,
            "Total chapter Duration": "",
            "chapters": []
        }
}
```
#### Latest Audiobook
This api endpoint allows you to retrieve latest Audiobook based on the last 5 day from Brana Audiobook collection.
Endpoint: ```brana_audiobook.api.audiobook_api.retreive_latest_audiobook```
###### Request
    HTTP Method: GET
    Parameters: None
###### Response
    HTTP Status Code: 200 OK
    Content-Type: application/json
###### Response Body
    The response body will contain latest audiobooks in JSON format.
    Example:
```
{
            "title": "እያደር ሲገለጥ",
            "description": "ድርሰቱ  በአጠቃላይ በሀገራችን በገጠሩ ህብረተሰብ  ውስጥ ያሉትን ማህበራዊ  ክስተቶች  የሚዳስ ስ  መፅሀፍ ነው ሌሎችንም  የህገራችንን  የገጠሩን ባህል ከዕለት ዕለት እንቅስቃሴ ውስጥ ያሉትን  ሂደቶች ይተርካል፡፡ ገፅ 76",
            "author": "ጎበዜ ጣፈጠ",
            "narrator": "Daniel Muluneh",
            "thumbnail": "https://app.berana.app/files/book3.jpg",
            "Sample Audiobook": "ዘመዶቼ",
            "duration": "7m 7s",
            "Total chapter": 0,
            "Total chapter Duration": "",
            "chapters": []
}
```
### Podcasts
This api endpoint allows you to retrieve all Podcasts available in the Brana Audiobook collection.
Endpoint: ```brana_audiobook.api.podcast_api.retrieve_podcasts```
###### Request
    HTTP Method: GET
    Parameters: None
###### Response
    HTTP Status Code: 200 OK
    Content-Type: application/json
###### Response Body
    The response body will contain list podcasts and episodes in JSON format.
    Example:
```
{
    "message": [
        {
            "title": "በትምህርት ሚኒስቴር ለረጅም ጊዜ አገልግለዋል",
            "description": "በትምህርት ሚኒስቴር ለረጅም ጊዜ አገልግለዋል",
            "Host": "ህይወት እምሻው",
            "cover image": "https://app.berana.app/files/049A6919.JPG",
            "episodes": [
                {
                    "title": "ሚኒስቴር ለረጅም",
                    "duration": "6m 26s",
                    "podcast Number": "1"
                }
            ]
        },
        {
            "title": "ባህል፣ አስተሳሰብ እንዲሁም የአኗኗር ዘይቤ",
            "description": "የኢጣልያ ወረራ ሲከሰት ከልዑል ራስ ዕምሩ ኃይለ ሥላሴ ጦር ጋር በምዕራብ ኢትዮጵያ በአርበኝነት ሲዋጉ ቆይተው በመያዛቸው ጣሊያን ከልዑል ራስ ዕምሩ ጋር በግዞት ለሰባት ዓመታት በፖንዞ ደሴትና በሊፓሪ ደሴት ታስረው ቆይተዋል።\nከዚያም የተባባሪ ኃያላት ወታደሮች በ1935 ዓ.ም. ሲያስመልጧቸው በተመለሱበት ጊዜ በትምህርታቸው እንደገና በኦክስፎርድ ከገፉ በኋላ በተለያዩ የመንግስት ተቋማት በተለይም በትምህርት ሚኒስቴር ለረጅም ጊዜ አገልግለዋል።\n",
            "Host": "Birhane Gabriel",
            "cover image": "https://app.berana.app/files/049A6919.JPG",
            "episodes": [
                {
                    "title": "ጊዜ አገልግለዋል",
                    "duration": "6m 26s",
                    "podcast Number": "1"
                }
            ]
        }
    ]
}
```
#### Podcast
This api endpoint allows you to retrieve podcast from Brana Audiobook collection.
Endpoint: ```brana_audiobook.api.podcast_api.retrieve_podcast```
###### Request
    HTTP Method: GET
    Parameters: podcast_id
###### Response
    HTTP Status Code: 200 OK
    Content-Type: application/json
###### Response Body
    The response body will contain podcast and It's episodes in JSON format.
    Example:
```
{
    "message": {
        "title": "ባህል፣ አስተሳሰብ እንዲሁም የአኗኗር ዘይቤ",
        "description": "የኢጣልያ ወረራ ሲከሰት ከልዑል ራስ ዕምሩ ኃይለ ሥላሴ ጦር ጋር በምዕራብ ኢትዮጵያ በአርበኝነት ሲዋጉ ቆይተው በመያዛቸው ጣሊያን ከልዑል ራስ ዕምሩ ጋር በግዞት ለሰባት ዓመታት በፖንዞ ደሴትና በሊፓሪ ደሴት ታስረው ቆይተዋል።\nከዚያም የተባባሪ ኃያላት ወታደሮች በ1935 ዓ.ም. ሲያስመልጧቸው በተመለሱበት ጊዜ በትምህርታቸው እንደገና በኦክስፎርድ ከገፉ በኋላ በተለያዩ የመንግስት ተቋማት በተለይም በትምህርት ሚኒስቴር ለረጅም ጊዜ አገልግለዋል።\n",
        "Host": "Birhane Gabriel",
        "cover image": "https://app.berana.app/files/049A6919.JPG",
        "episodes": [
            {
                "title": "ጊዜ አገልግለዋል",
                "duration": "6m 26s",
                "podcast Number": "1"
            }
        ],
        "total episodes": 1
    }
}
```
#### Recommended Podcast 
This api endpoint allows you to retrieve recommended podcasts from Brana Audiobook collection.
Endpoint: ```brana_audiobook.api.podcast_api.retrieve_recommended_podcasts```
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
    "message": [
        {
            "title": "ባህል፣ አስተሳሰብ እንዲሁም የአኗኗር ዘይቤ",
            "description": "የኢጣልያ ወረራ ሲከሰት ከልዑል ራስ ዕምሩ ኃይለ ሥላሴ ጦር ጋር በምዕራብ ኢትዮጵያ በአርበኝነት ሲዋጉ ቆይተው በመያዛቸው ጣሊያን ከልዑል ራስ ዕምሩ ጋር በግዞት ለሰባት ዓመታት በፖንዞ ደሴትና በሊፓሪ ደሴት ታስረው ቆይተዋል።\nከዚያም የተባባሪ ኃያላት ወታደሮች በ1935 ዓ.ም. ሲያስመልጧቸው በተመለሱበት ጊዜ በትምህርታቸው እንደገና በኦክስፎርድ ከገፉ በኋላ በተለያዩ የመንግስት ተቋማት በተለይም በትምህርት ሚኒስቴር ለረጅም ጊዜ አገልግለዋል።\n",
            "Host": "Birhane Gabriel",
            "cover image": "https://app.berana.app/files/049A6919.JPG",
            "episodes": [
                {
                    "title": "ጊዜ አገልግለዋል",
                    "duration": "6m 26s",
                    "podcast Number": "1"
                }
            ],
            "total episodes": 1
        }
    ]
}
```
#### Editors Picks Podcasts
This api endpoint allows you to retrieve editors picks audiobook from Brana Audiobook collection.
Endpoint: ```brana_audiobook.api.podcast_api.retrieve_editor_podcasts```
###### Request
    HTTP Method: GET
    Parameters: None
###### Response
    HTTP Status Code: 200 OK
    Content-Type: application/json
###### Response Body
    The response body will contain editor picks Audiobook and It's Chapters in JSON format.
    Example:
```

```
#### Play Audiobooks Sample
This api endpoint allows you to play Audiobook based audiobook title from Brana Audiobook collection.
Endpoint: ```brana_audiobook.api.audiobook_api.audiobook_sample?audiobook_id=መተዋወቂያ```
###### Request
    HTTP Method: GET
    Parameters: None
###### Response
    HTTP Status Code: 200 OK
    Content-Type: ""
###### Response
    Example:
![Audioplay](https://app.berana.app/api/method/brana_audiobook.api.audiobook_api.audiobook_sample?audiobook_id=እያደር ሲገለጥ)
#### Play Audiobook Chapters
This api endpoint allows you to play Audiobook chapters based chapter title from Brana Audiobook collection.
Endpoint: ```brana_audiobook.api.audiobook_api.play_audiobook_chapter?audiobook_chapter=ሚፈልግ ሰው```
###### Request
    HTTP Method: GET
    Parameters: audiobook_chapter
###### Response
    HTTP Status Code: 200 OK
    Content-Type: ""
###### Response
    Example:
![Audioplay](https://app.berana.app/api/method/brana_audiobook.api.audiobook_api.play_audiobook_chapter?audiobook_chapter=ሚፈልግ ሰው)
### Authors
This api endpoint allows you to retrieve authors Brana.
Endpoint: ```brana_audiobook.api.authors_api.retrive_authors```
###### Request
    HTTP Method: GET
    Parameters: None
###### Response
    HTTP Status Code: 200 OK
    Content-Type: application/json
###### Response Body
    The response body will contain authors full name, image and number of books in JSON format.
    Example:
```
{
     {
            "full name": "ድርቡ አደራ",
            "user image": "https://app.berana.app/files/book464a244.jpeg",
            "total Book": 1
        },
        {
            "full name": "አያልቅበት አደም",
            "user image": "https://app.berana.app/files/ዘነበወላ.jpg",
            "total Book": 0
        },
        {
            "full name": "በዓሉ ግርማ",
            "user image": "https://app.berana.app/files/bealu.jpeg",
            "total Book": 2
        },
}
```
#### Author
This api endpoint allows you to retrieve author based on author id/name from Brana.
Endpoint: ```brana_audiobook.api.authors_api.retrieve_author?author_id=በዓሉ ግርማ```
###### Request
    HTTP Method: GET
    Parameters: author_id
###### Response
    HTTP Status Code: 200 OK
    Content-Type: application/json
###### Response Body
    The response body will contain authors full name, image, number of books, list of books in JSON format.
    Example:
```
{
    "message": [
        {
            "name": "በዓሉ ግርማ",
            "author image": "https://app.berana.app/files/bealu.jpeg",
            "number of books": 2,
            "books": [
                {
                    "title": "ከአድማስ ባሻገር",
                    "narrator": "Natnael Tilaye",
                    "thumbnail": "https://app.berana.app/files/book4.jpeg",
                    "sample audiobook title": "በቀድሞዋ የሶቪየት ሶሽያሊስት ሕብረት",
                    "duration": "31s",
                    "total chapter": 0,
                    "total chapter duration": "",
                    "chapters": []
                },
                {
                    "title": "The Fable Of Us",
                    "narrator": "Daniel Muluneh",
                    "thumbnail": "https://app.berana.app/files/book1.jpg",
                    "sample audiobook title": "ዘመዶቼ",
                    "duration": "7m 7s",
                    "total chapter": 0,
                    "total chapter duration": "",
                    "chapters": []
                }
            ]
        }
    ]
}
```
#### Promotions
This api endpoint allows you to retrieve promotions Brana.
Endpoint: ```brana_audiobook.api.promotion_api.promotion```
###### Request
    HTTP Method: GET
    Parameters: None
###### Response
    HTTP Status Code: 200 OK
    Content-Type: application/json
###### Response Body
    The response body will contain image, header, description in JSON format.
    Example:
```
{
    "message": [
        {
            "image": "https://app.berana.app/files/BRANA RE FINAL LOGO-ai.png",
            "header": "Upcoming",
            "description": "Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of \"de Finibus Bonorum"
        }
    ]
}
```

## Conclusion
This document has provided an overview of the Brana Audiobook API, including the available endpoints