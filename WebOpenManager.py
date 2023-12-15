from webbrowser import open as webopen

def OpenImageByUrl(event,url):
    print(event)
    webopen(url,new=0)