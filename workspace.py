from saucenao_api import SauceNao

# key: 15d4ceca34b800a9280e5b55118734761d19d1ea
my_api_key = "15d4ceca34b800a9280e5b55118734761d19d1ea"
sauce = SauceNao(api_key=my_api_key)

# photo file
photo_file_path = ".\Photos\Pio_tirami.png"
# photo_file_path = "https://i.imgur.com/oZjCxGo.jpg"

result = sauce.from_file(open(photo_file_path,"rb"))

# output url from pixiv
# 前五筆
for i in range(0,5):
    print(result[i].thumbnail)
    print(result[i].urls)