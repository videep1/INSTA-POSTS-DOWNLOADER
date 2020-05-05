from tkinter import *
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import os, cv2, json, requests, urllib.request, tkinter as tk

# Defining CreateWidgets() function to create necessary tkinter widgets
def CreateWidgets():
    urlLabel = Label(root, text="INSTAGRAM URL : ", background = "tan4")
    urlLabel.grid(row=0, column=0, padx=5, pady=5)

    root.urlEntry = Entry(root, width=30, textvariable=instaURL)
    root.urlEntry.grid(row=0, column=1,columnspan=2, pady=5)

    dwldBTN = Button(root, text="DOWNLOAD", command=i_Downloader, highlightbackground = "green")
    dwldBTN.grid(row=0, column=3, padx=5, pady=5)

    root.resultsLabel = Label(root, text="RESULTS", background = "tan4")
    root.resultsLabel.grid(row=1, column=0, padx=5, pady=1)

    root.dwldLabel = Label(root, textvariable=dwldtxt, background = "deepskyblue4")
    root.dwldLabel.grid(row=2, column=0, columnspan=2, padx=5, pady=5)


    root.previewLabel = Label(root, text="PREVIEW", background = "tan4")
    root.previewLabel.grid(row=3, column=0, padx=5, pady=5)

def i_Downloader():
    
    download_path = r"C:\Users\videe\Documents\ "
    
    insta_Posts = requests.get(instaURL.get())
    #using web scrapping of insta
    
    soup= BeautifulSoup(insta_Posts.text, 'html.parser')
    script=soup.find('script',text=re.compile('window._sharedData'))
    
    page_json = script.text.split(' = ', 1)[1].rstrip(';')
    
    data = json.loads(page_json)
    base_data = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']
    
    typename = base_data['__typename']


    if typename == "GraphImage":
        
        display_url = base_data['display_url']
        
        file_name = base_data['taken_at_timestamp']
        
        download_p = download_path + str(file_name) + ".jpg"
       
        if not os.path.exists(download_p):
           
            urllib.request.urlretrieve(display_url, download_p)
            
            image = Image.open(download_p)
            
            image = image.resize((300, 300), Image.ANTIALIAS)
            
            image = ImageTk.PhotoImage(image)
            
            imageLabel = Label(root)
            imageLabel.grid(row=4, column=1,columnspan=2, padx=1, pady=1)
            imageLabel.config(image=image)
            imageLabel.photo = image
            
            prev_t = dwldtxt.get()
           
            new_t = prev_t + "\n" + str(file_name) + ".jpg DOWNLOADED"
            
            root.dwldLabel.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
            
            dwldtxt.set(new_t)
        else:
            prev_t = dwldtxt.get()
            new_t = prev_t + "\n" + str(file_name) + ".jpg EXISTS"
            root.dwldLabel.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
            dwldtxt.set(new_t)

    # if post is video
    elif typename == "GraphVideo":
        
        video_url = base_data['video_url']
        
        file_name = base_data['taken_at_timestamp']
        download_p = download_path + str(file_name) + ".mp4"
    
        if not os.path.exists(download_p):
            
            urllib.request.urlretrieve(video_url, download_p)
            vid = cv2.VideoCapture(download_p)
            while 11:
                _,frame=vid.read()
                cv2.imshow("Original",frame)
                k=cv2.waitKey(5) & 0xFF
                if k==27:
                    break
            cv2.destroyAllWindows()
            vid.release()

            
            # Displaying the message
            prev_t = dwldtxt.get()
            new_t = prev_t + "\n" + str(file_name) + ".mp4 DOWNLOADED"
            root.dwldLabel.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
            dwldtxt.set(new_t)
        else:
              
            prev_t = dwldtxt.get()
            new_t = prev_t + "\n" + str(file_name) + ".mp4 EXISTS"
            root.dwldLabel.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
            dwldtxt.set(new_t)
            root.dwldLabel.config(text=str(file_name) + ".mp4 HAS ALREADY BEEN DOWNLOADED")


    #to check wheater post contain many images
    elif typename == "GraphSidecar":
        
        shortcode = base_data['shortcode']
        
        response = requests.get(f"https://www.instagram.com/p/" + shortcode + "/?__a=1").json()
        
        post_n = 1; i = 0
        for edge in response['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']:
            
            file_name = response['graphql']['shortcode_media']['taken_at_timestamp']
            
            download_p = download_path + str(file_name) + "-" + str(post_n)
            
            is_video = edge['node']['is_video']

            
            if not is_video:
                
                display_url = edge['node']['display_url']
                download_p += ".jpg"
                if not os.path.exists(download_p):
                    urllib.request.urlretrieve(display_url, download_p)
                    image = Image.open(download_p)
                    image = image.resize((300, 300), Image.ANTIALIAS)
                    image = ImageTk.PhotoImage(image)
                    
                    imageLabel = Label(root)
                    imageLabel.grid(row=4, column=i, padx=1, pady=1)
                    imageLabel.config(image=image)
                    imageLabel.photo = image
                    
                    prev_t = dwldtxt.get()
                    new_t = prev_t+"\n"+str(file_name) + "-" + str(post_n) + ".jpg DOWNLOADED"
                    root.dwldLabel.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
                    dwldtxt.set(new_t)
                    
                    i+=1
                else:
            
                    prev_t = dwldtxt.get()
                    new_t = prev_t+"\n"+str(file_name) + "-" + str(post_n) + ".jpg EXISTS"
                    root.dwldLabel.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
                    dwldtxt.set(new_t)

            
            else:
                
                video_url = edge['node']['video_url']
                
                download_p += ".mp4"
            
                if not os.path.exists(download_p):
                    
                    
                    urllib.request.urlretrieve(video_url, download_p)
                    vid = cv2.VideoCapture(download_p)
                    ret, frame = vid.read()
                    video_icon = download_path + str(file_name) + ".mp4"
                    cv2.imwrite(video_icon, frame)
                     
                    icon = Image.open(video_icon)
                    icon = icon.resize((90, 90), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(icon)
                    imageLabel = Label(root)
                    imageLabel.grid(row=4, column=i, padx=1, pady=1)
                    imageLabel.config(image=img)
                    imageLabel.photo = img
                    # Displaying the message
                    prev_t = dwldtxt.get()
                    new_t = prev_t+"\n"+str(file_name) + "-" + str(post_n) + ".mp4 DOWNLOADED"
                    root.dwldLabel.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
                    dwldtxt.set(new_t)
                    
                    i+=1
                else:
        
                    prev_t = dwldtxt.get()
                    new_t = prev_t+"\n"+str(file_name) + "-" + str(post_n) + ".mp4 EXISTS"
                    root.dwldLabel.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
                    dwldtxt.set(new_t)
            
            post_n += 1


root = tk.Tk()
root.geometry("530x410")
root.title("i-DOWNLOADER")
root.config(background = "deepskyblue4")


instaURL = StringVar()
dwldtxt = StringVar()
CreateWidgets()

root.mainloop()