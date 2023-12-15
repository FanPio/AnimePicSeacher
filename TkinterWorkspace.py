import tkinter as tk
from tkinter import filedialog
from tkinter.constants import CENTER
import tkinter.font as tkFont
from PIL import Image,ImageTk

from io import BytesIO

import SpilderWorkspace
import WebOpenManager

from saucenao_api import SauceNao

# sauceNao所需的資料
# my_api_key = "15d4ceca34b800a9280e5b55118734761d19d1ea"
# my_api_key = "ed8cc8d032c275df185175e8577f2e2b2289e6dd"
my_api_key = "41a0ebf48ef95bbcfde6f4c42ac81c0aff5998d1"
sauce = SauceNao(api_key=my_api_key)

# 函式: 上傳圖片後變更按鈕的位置
def ButtonPosChange():
    Upload_button.place(x=275,y=160,anchor=CENTER)
    Search_button.place(x=275,y=200,anchor=CENTER)
    PreviewPicShow()

# 函式: 上傳圖片後顯示圖片
def PreviewPicShow():
    global UserInputPicPreviewLabel
    global PreviewImage

    # 開啟圖片
    PreviewImage = Image.open(UserInputPic)
    # 變更解析度
    PreviewImage_raw_x = PreviewImage.size[0]
    PreviewImage_raw_y = PreviewImage.size[1]

    # 等比例縮小
    # 125 * 125
    Max_pixel = 15625
    PreviewImage_adjusted_x = (Max_pixel / (PreviewImage_raw_y/PreviewImage_raw_x)) ** 0.5
    PreviewImage_adjusted_y = PreviewImage_adjusted_x  * (PreviewImage_raw_y/PreviewImage_raw_x)

    PreviewImage_adjusted_x = int(PreviewImage_adjusted_x)
    PreviewImage_adjusted_y = int(PreviewImage_adjusted_y)

    # 確認修改後的大小
    # print("X:",PreviewImage_adjusted_x)
    # print("Y:",PreviewImage_adjusted_y)

    PreviewImage = PreviewImage.resize((PreviewImage_adjusted_x,PreviewImage_adjusted_y))


    # 轉成適用於tkinter
    PreviewImage = ImageTk.PhotoImage(PreviewImage)
    
    UserInputPicPreviewLabel = tk.Label(master=window,image=PreviewImage,
                                        width=PreviewImage.width(),
                                        height=PreviewImage.height())
    UserInputPicPreviewLabel.place(x=475,y=200,anchor=CENTER)

# 函式: 讀取圖片
def LoadPicFile():
    global UserInputPic

    local_file_path = filedialog.askopenfilename(filetypes=(("png files","*.png"),
                                                            ("all files","*.*")))
    UserInputPic = local_file_path

    # 確認圖片路徑
    # print(UserInputPic)
    
    # 改變位置
    ButtonPosChange()

# 函式: 使用sauceNao開始搜尋
def PicSearch():
    result = sauce.from_file(open(UserInputPic,"rb"))

    print(result[0].urls)

    PicDetailShow(result[0])

    # 使用爬蟲擷取作者頭貼
    # 失敗
    # SpilderWorkspace.GetPixivAuthorThumbnail(result)
    
# 函式: 展示搜尋結果
# 標題、網址、作者名稱
def PicDetailShow(SauceNaoResult):
    PicURL = SauceNaoResult.urls[0]
    PicAuthorName = SauceNaoResult.author
    PicTitle = SauceNaoResult.title
    PicThumbnail = SauceNaoResult.thumbnail

    # 縮圖
    print(PicThumbnail)
    

    global PicThumbnail_Image
    # 抓線上圖片
    PicThumbnail_Image = Image.open(BytesIO(SpilderWorkspace.GetWebsitePic(PicThumbnail).content))
    # 長、寬
    PicThumbnail_Image_width = PicThumbnail_Image.size[0]
    PicThumbnail_Image_heigh = PicThumbnail_Image.size[1]
    # 轉換成適用於tk的圖片
    PicThumbnail_Image = ImageTk.PhotoImage(PicThumbnail_Image)
    # 圖片區域
    PicThumbnail_Label = tk.Label(image=PicThumbnail_Image,
                                  width=PicThumbnail_Image_width,
                                  height=PicThumbnail_Image_heigh)
    PicThumbnail_Label.place(x=200,y=320,anchor=CENTER)

    # 文字設定
    Font_Settings = tkFont.Font(family="Arial",size=10)

    # 標題
    PicTitle_Label = tk.Label(text="title:{title}".format(title=PicTitle),
                        justify="left",
                        font=Font_Settings)
    PicTitle_Label.place(x=200+PicThumbnail_Image_width+10,y=320+PicThumbnail_Image_heigh-110,anchor=CENTER)

    # URL
    PicURL_Label = tk.Label(text="URL:",
                        justify="left",
                        font=Font_Settings)
    PicURL_Label.place(x=200+PicThumbnail_Image_width+10,y=320+PicThumbnail_Image_heigh-90,anchor=CENTER)

    # Pic_URL_ForWeb = tk.Text(master=window)
    Pic_URL_ForWeb = tk.Label(master=window,text=PicURL,fg="blue")
    Pic_URL_ForWeb.place(x=200+PicThumbnail_Image_width+250,y=320+PicThumbnail_Image_heigh-90,anchor=CENTER)
    Pic_URL_ForWeb.bind('<Button-1>',lambda event,url = PicURL:WebOpenManager.OpenImageByUrl(event,PicURL))

    # PicTitle = tk.Label(text="title:{title}\nurl:{url}\nauthor:{author}".format(title=PicTitle,
    #                                                   url=PicURL,
    #                                                   author=PicAuthorName),justify="left",
    #                                                font=PicInfo_Font)
    # PicInfo_Label.place(x=200+PicThumbnail_Image_width+175,y=320+PicThumbnail_Image_heigh-75,anchor=CENTER)

    # 作者
    PicAuthorName_Label = tk.Label(text="Name:{title}".format(title=PicAuthorName),
                        justify="left",
                        font=Font_Settings)
    PicAuthorName_Label.place(x=200+PicThumbnail_Image_width+10,y=320+PicThumbnail_Image_heigh-70,anchor=CENTER)

# 開啟視窗
window = tk.Tk()

# 視窗設定
window.title = "SauceNao_AnimePicSearcher"
window.geometry("800x600") # 視窗大小
window.resizable(False,False)

# Title標題圖片
# 使用PIL的Image,ImageTk套件解決原生tk套件PhotoImage僅支援GIF和PGM/PPM
# 開啟jpg圖片並轉換成適用於Tk套件的image
Title_image = ImageTk.PhotoImage(Image.open(".\Photos\Title.jpg"))
Title_label = tk.Label(image=Title_image,width=385,height=100)
Title_label.pack()

# 使用者上傳的圖片
UserInputPic = ""

# 使用者上傳的圖片的預覽區
UserInputPicPreviewLabel = ""   

# 主介面的兩個按鈕
# 上傳
Upload_button = tk.Button(text="Upload Pic",command=LoadPicFile,width=15)
# old
# Upload_button.pack(side="top")

# 使用絕對位置排版: 未上傳圖片
Upload_button.place(x=400,y=160,anchor=CENTER)

# 使用絕對位置排版: 已上傳圖片
# Upload_button.place(x=275,y=160,anchor=CENTER)

# 搜尋
Search_button = tk.Button(text="Search",command=PicSearch,width=15)

# old
# Search_button.pack(side="top")

# 使用絕對位置排版: 未上傳圖片
Search_button.place(x=400,y=200,anchor=CENTER)

# 使用絕對位置排版: 已上傳圖片
# Search_button.place(x=275,y=200,anchor=CENTER)

# 重複更新視窗
window.mainloop()