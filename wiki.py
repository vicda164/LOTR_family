# gets all section from page 
# http://lotr.wikia.com/api.php?action=parse&page=Gandalf&format=jsonfm&prop=sections

# gets specific section
# http://lotr.wikia.com/api.php?action=parse&prop=text&page=Gandalf&format=jsonfm&section=Biography

import requests
import secret

def fecthWikiPage(name, section=1):
    print("wiki: try to fecth",name)
    S = requests.Session()
    #api.php?action=login&lgname=user&lgpassword=password
    URL = "http://lotr.wikia.com/api.php?"

    # Retrieve login token first
    PARAMS_0 = {
        'action':"login",        
        'format':"json",
        'lgname': secret.LOTR_NAME,
        'lgpassword':secret.LOTR_PASSWORD,    
    }

    R = S.post(url=URL, params=PARAMS_0)
    DATA = R.json()
    LOGIN_TOKEN = DATA['login']['token']

    print(LOGIN_TOKEN)

    """
    Parameters:
    lgname              - User Name
    lgpassword          - Password
    lgdomain            - Domain (optional)
    lgtoken             - Login token obtained in first request
    """
    # Send a post request to login. Using the main account for login is not
    # supported. Obtain credentials via Special:BotPasswords
    # (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
    PARAMS_1 = {
        'action':"login",
        'lgname':secret.LOTR_NAME,
        'lgpassword':secret.LOTR_PASSWORD,
        'lgtoken':LOGIN_TOKEN,
        'format':"json"
    }

    R = requests.post(URL, data=PARAMS_1)
    DATA = R.json()

    TITLE = name
    """
        section = 0 : infobox and short-description
        section = 1 : biography
    """

    PARAMS = {
        'action': "parse",
        'page': TITLE,
        'format': "json",    
        'section': section
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    # TODO check for error

    return DATA