import requests

url = "https://portal.sa.dendai.ac.jp/uprx/up/pk/pky001/Pky00101.xhtml"
payload = {
    "loginForm": "loginForm",
    "loginForm:userId": "19fi079",
    "loginForm:password": "RF57j3tsK-008!",
    "loginForm:loginButton": "",
    "javax.faces.ViewState": "stateless"
}
print(requests.post(url, data=payload, verify=False).text)
