import sys
from nltk.corpus import wordnet 
import os
from bs4 import BeautifulSoup
from urllib import urlretrieve
import urllib
from PyQt4.QtCore import *
from PyQt4.QtGui import * 
import cv2
import pygame
import xml.etree.ElementTree as ET
from pygame.locals import *


class data :

    def __init__(self) :
        self.obj=str()
        self.item=str()
        self.size=(0,0)
        self.cmd=str()


    def getImage(self,search,nn) :
        wn=wordnet.synset(str(search)+'.n.01')
        wnid=wn.pos()+str(wn.offset()).zfill(8)
        imgt="http://image-net.org/api/text/imagenet.synset.geturls?wnid="+wnid
        page=urllib.urlopen(imgt)
        soup=BeautifulSoup(page,"lxml")
        link=soup.get_text().split()
        global n
        n=nn
        counter=1
        os.system("mkdir "+str(search))
        for im in link :
            if counter<=nn :
                try:
                    
                    pg=urllib.urlopen(im)
                    urltype=pg.info()
                    if urltype.type=="image/jpeg" :
                        path=os.path.join(str(search),"pic"+str(counter)+".jpg")
                        urllib.urlretrieve(im,path)
                        counter+=1
                    else :
                        continue
                        
                except (IOError,UnicodeError) :
                    continue
            else :
                break
        print "Download Complete"

                                    
    




    def delete(self,obj,item) :
        del_items=item.split()
        for items in del_items :
            path_delItem=os.path.join(str(obj),items+".jpg")
            os.remove(path_delItem)
        

    def disp_crop(self,crop) :
        try :
            cv2.imshow("cropped",crop)  
            cv2.imwrite(path_crop,crop)
        except :
            print "Something went wrong"

    def crop(self,obj,test) :
        
        tree=ET.parse(str(test)+".xml")
        root=tree.getroot()
        os.system("./imglab -c "+str(test)+".xml "+obj)
        os.system("./imglab "+str(test)+".xml")
        for val in root.findall('images') :
            for dim in val :
                file=dim.get("file")
                print file
                for x in dim :
                    top=int(x.get("top"))
                    left=int(x.get("left"))
                    width=int(x.get("width"))
                    height=int(x.get("height"))
                    print top
                    path=os.path.join(file)
                    img=cv2.imread(path)
                    crop=img[top:height,left:width]
                    cv2.imwrite(path,crop)
                #cv2.imshow("cropped",crop)
                #cv2.waitkey(0)
                #cv2.destroyAllWindows() 
            
      

    def resize(self,obj,item,sizex,sizey) :
        resize_item=item.split()
        for items in resize_item :
            path_resize=os.path.join(str(obj),items+".jpg")
            resize=cv2.resize(cv2.imread(path_resize),(sizex,sizey))
            cv2.imwrite(path_resize,resize)

 
if __name__=="__main__" :
    dat=data()
    flag=True 
    print "=================TERMINAL===================="
    while flag :
       
        cmd=raw_input(">>")

        if cmd=="exit" :
            flag=False
        else :
            if cmd=="scrap" :
                try :
                    search=raw_input("")
                    nn=int(raw_input(""))
                    dat.getImage(search,nn)
                except :
                    print "Network Error"

            if cmd =='delete' :
                try :
                    obj_del=raw_input("enter the folder : ")
                    item_del=raw_input("enter the image : ")
                    dat.delete(obj_del,item_del)
                except :
                    print "Invalid input"

            elif cmd == 'resize' :
                try :
                    obj_resize=raw_input("enter the folder: ")
                    item_resize=raw_input("enter the image: ")
                    sizex=int(raw_input("width"))
                    sizey=int(raw_input("height"))
                    
                    dat.resize(obj_resize,item_resize,sizex,sizey)
                except Exception as e:
                    print "Invalid input"
                    print e

            elif cmd == "crop" :
                try :

                    obj_crop=raw_input("enter the folder: ")
                    item=raw_input("enter the xml file name: ")
                    dat.crop(obj_crop,item)
                except Exception as e:
                    print "Invalid input"
                    print e

            elif cmd == "help" :
                print "-------------------COMMANDS---------------------"
                print "         scrap  delete  resize  crop            "        
            
            else :
                print "invalid command"
    


                                                                                                                                                                                                     

