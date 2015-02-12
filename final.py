import sys
import pygame
from pygame.locals import*
import math
import numpy as np
import matplotlib.pyplot as plt
import Tkinter as tk
import scipy.io
import locale
import os
locale.setlocale( locale.LC_ALL, "")

path_file=os.getcwd()
path_file=path_file+ '\\Data.mat'
pygame.init()
pie=math.pi
marginx=0
marginy=0
pw=540
ph=480
s=6

sz =90

txt=20

top    =[]
bottom =[]

load_pt     =[]
temp_load_pt=[]


temp_range=[]
udl_line=[]
udl_poly=[]
yl_udl=0
val_udl=0

support=[]
temp_support=[]

fld=[]
coff=[]
pt_arr=[]
arr_rec=[]
#first screen
button_top        = pygame.Rect((10,20),(sz,20))
button_bottom     = pygame.Rect((10,50),(sz,20))
button_load       = pygame.Rect((10,80),(sz,20))
button_sup        = pygame.Rect((10,110),(sz,20))
button_export     = pygame.Rect((10,140),(sz,20))

#bottom_butt
button_back = pygame.Rect((10,440),(sz,20))

#second screen
button_polynomial = pygame.Rect((10,20),(sz,20))
button_linear     = pygame.Rect((10,50),(sz,20))

#menu_load
button_pointl     = pygame.Rect((10,20),(sz,20))
button_pointc     = pygame.Rect((10,50),(sz,20))

#menu_udl
button_udlp     = pygame.Rect((10,20),(sz,20))
button_udll     = pygame.Rect((10,50),(sz,20))

#menu_support
button_hinge = pygame.Rect((10,20),(sz,20)) #2
button_fixed = pygame.Rect((10,50),(sz,20)) #1
button_shre  = pygame.Rect((10,80),(sz,20)) #4
button_inhi  = pygame.Rect((10,110),(sz,20)) #3


window=pygame.display.set_mode((640,480))

canvas1=pygame.Rect(marginx,marginy,pw,ph)
show=window.subsurface(canvas1)

canvas2=pygame.Rect(540,0,100,ph)
side=window.subsurface(canvas2)


k=True

blk=(0,0,0)
w=(255,255,255)
li=(24, 4, 255)
ml=(100,255,60)
red=(62, 49, 117)
RED=(163, 32, 8)
GRN=(45, 134, 51)


green=(0,255,0)
button=(143, 141, 155)
wit=(255,255,255)
load_col=(235,14,14)
udl_col=(0,0,0)
udl_top_col=(238, 0, 135)
pdl_rec=(238, 0, 135)
ldl_col=(255, 111, 0)
col=(0,0,0)
ld_rec=(255, 225, 0)
window.fill(blk)
show.fill((255,255,255))
side.fill(red)

hinge= (0,255,0)
fixed= (0,255,0)
shre=  (0,255,0)
inhi=  (0,255,0)
sup_col=[hinge,fixed,shre,inhi]
cols=[ldl_col,udl_top_col]

x=10.0
y=470.0

def texts(txt,x,y,col=ml):
   font=pygame.font.Font(None,20)
   wrtxt=font.render(str(txt), 1,col)
   show.blit(wrtxt, (x, y))

def texts_butt(txt,x,y):
   font=pygame.font.Font(None,20)
   wrtxt=font.render(str(txt), 1,wit)
   side.blit(wrtxt, (x, y))

def text_load(txt,x,y,col=blk):
   font=pygame.font.Font(None,20)
   wrtxt=font.render(str(txt), 1,blk)
   show.blit(wrtxt, (x-2, int(y-10)))

def wrt_file():
        scipy.io.savemat(path_file, mdict={'Top': top,'Bottom': bottom,'ludl': udl_line,'pudl': udl_poly,'pt_load':load_pt,'support': support})

def back_butt((xq,yq)):
        pygame.draw.rect (side, button, button_back)

def confirm(tempi):
        t=True
        button_conf = pygame.Rect((470,450),(70,20))
        pygame.draw.rect (show, GRN, button_conf)
        text_load('Confirm',480,465)
        button_nconf = pygame.Rect((390,450),(70,20))
        pygame.draw.rect (window, RED, button_nconf)
        text_load('Cancel',400,465)
        pygame.display.flip()
        while t:
                for event in pygame.event.get():
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        
                        ## if mouse is pressed get position of cursor ##
                        pos = pygame.mouse.get_pos()
                        ## check if cursor is on button ##
                        if button_conf.collidepoint(pos):
                                pt_arr[:]=[]                            
                                return (1,tempi)
                        elif button_nconf.collidepoint(pos):
                                pt_arr[:]=[]
                                return (0,0)
        
        
def maxxx(a,b):
        if(a>b):
                return a
        else:
                return b


def graph_draw(arr,p=0,col=li):
        points = np.array(arr)
        # get x and y vectors
        x = points[:,0]
        y = points[:,1]
        length=len(points)
        # calculate polynomial
        z = np.polyfit(x, y, length-1)
        f = np.poly1d(z)

        # calculate new x's and y's
        x_new = np.linspace(x[0], x[-1], 50)
        y_new = f(x_new)
        tempx=x_new[0]
        tempy=y_new[0]
        i=1
        leng=len(x_new)
        while (i<leng):
                
                pygame.draw.line(show,col,(tempx,tempy),(x_new[i],y_new[i]))
                (tempx,tempy)=(x_new[i],y_new[i])
                i=i+1
        if(p):
                r=0
                while(r<length):
                        coff.append(f(0)/math.factorial(r))
                        f=f.deriv()
                        r=r+1
        
def polynomial_base(coord,temp,x,y):
        (xl,yl)=coord
        l=True
        pygame.draw.rect (show, (0,0,0), Rect((xl-s/2,yl-s/2),(s,s)))
        show.blit(temp,(0,0))
        pygame.display.flip()
        temp=show.copy()
        while l:
                for event in pygame.event.get():
                        
                        if event.type==pygame.QUIT:
                                pygame.quit()
                        elif(event.type==pygame.MOUSEMOTION):
                                temp_arr=pt_arr[:]
                                (xr,yr)=pygame.mouse.get_pos()
                                show.blit(temp,(0,0))
                                pygame.draw.line(show,ml,(xr,0),(xr,y))
                                pygame.draw.line(show,ml,(xr,yr),(x,yr))
                                temp_arr.append((xr,yr))
                                graph_draw(temp_arr)
                                pygame.draw.rect (show, (0,0,0), Rect((xr-s/2,yr-s/2),(s,s)))
                                texts(xr-x,(xr+x)/2,yr)
                                texts(y-yr,xr,(y+yr)/2)
                                pygame.display.flip()
                        elif(event.type==pygame.MOUSEBUTTONDOWN):
                                if(pygame.mouse.get_pressed()[2]):
                                        show.blit(temp,(0,0))
                                        pygame.draw.rect (show, (0,0,0), Rect((xl-s/2,yl-s/2),(s,s)))
                                        graph_draw(pt_arr,1)
                                        fld.append((xl,yl))
                                        l=False
                                else:
                                        show.blit(temp,(0,0))
                                        pygame.draw.line(show,ml,(xr,yr),(xr,y))
                                        pygame.draw.line(show,ml,(xr,yr),(x,yr))
                                        texts(xr-x,(xr+x)/2,yr)
                                        texts(y-yr,xr,(y+yr)/2)
                                        temp=show.copy()
                                        pt_arr.append((xr,yr))
                                        (xl,yl)=(xr,yr)
                                        graph_draw(pt_arr)
                                        pygame.draw.line(show,ml,(xr,0),(xr,y))
                                        pygame.draw.line(show,ml,(xr,yr),(x,yr))
                                        pygame.draw.rect (show, (0,0,0), Rect((xr-s/2,yr-s/2),(s,s)))
                                
                                        texts(xr-x,(xr+x)/2,yr)
                                        texts(y-yr,xr,(y+yr)/2)
                                
                                pygame.display.flip()
        temp=show.copy()

def polynomial_start(temp,k,x,y):
        while k:
                for event in pygame.event.get():
                        
                        if event.type==pygame.QUIT:
                                pygame.quit()
                        elif(event.type==pygame.MOUSEMOTION):
                                (xr,yr)=pygame.mouse.get_pos()
                                
                                show.blit(temp,(0,0))
                                pygame.draw.rect (show, (0,0,0), Rect((xr-s/2,yr-s/2),(s,s)))
                                pygame.draw.line(show,ml,(xr,y),(xr,0))
                                pygame.draw.line(show,ml,(x,yr),(pw,yr))
                                texts(xr-x,(xr+x)/2,yr)
                                texts(y-yr,xr,(yr+y)/2)
                                pygame.display.flip()
                        elif(event.type==pygame.MOUSEBUTTONDOWN):
                                
                                a=pygame.mouse.get_pos()
                                pt_arr.append(a)
                                k=False
        fld.append(a)
        polynomial_base(a,show.copy(),x,y)

def linear_draw_base(arr,p=0,col=li):
        points = np.array(arr)
        # get x and y vectors
        x = points[:,0]
        y = points[:,1]
        length=len(points)
        # calculate polynomial
        z = np.polyfit(x, y, length-1)
        f = np.poly1d(z)

        # calculate new x's and y's
        x_new = np.linspace(x[0], x[-1], 50)
        y_new = f(x_new)
        tempx=x_new[0]
        tempy=y_new[0]
        i=1
        leng=len(x_new)
        while (i<leng):
                pygame.draw.line(show,col,(tempx,tempy),(x_new[i],y_new[i]))
                (tempx,tempy)=(x_new[i],y_new[i])
                i=i+1
        r=0
        if(p):
                while(r<length):
                        coff.append(f(0)/math.factorial(r))
                        f=f.deriv()
                        r=r+1
                arr_rec.append([coff[:],pt_arr[:],0])
                coff[:]=[]

def linear_draw(arr,yn,v,p=0,col=ldl_col):
        points = np.array(arr)
        # get x and y vectors
        x = points[:,0]
        y = points[:,1]
        length=len(points)
        # calculate polynomial
        z = np.polyfit(x, y, length-1)
        f = np.poly1d(z)

        # calculate new x's and y's
        x_new = np.linspace(x[0], x[-1], 50)
        y_new = f(x_new)
        tempx=x_new[0]
        tempy=y_new[0]
        i=1
        leng=len(x_new)
        while (i<leng):
                pygame.draw.line(show,col,(tempx,tempy),(x_new[i],y_new[i]))
                (tempx,tempy)=(x_new[i],y_new[i])
                i=i+1
        r=0
        if(p):
                while(r<length):
                        coff.append(f(0)/math.factorial(r))
                        f=f.deriv()
                        r=r+1
                arr_rec.append([coff[:],pt_arr[:],yn,v])
                coff[:]=[]
        
def linear_base(coord,temp,x,y):
        (xl,yl)=coord
        l=True
        pygame.draw.rect (show, blk, Rect((xl-s/2,yl-s/2),(s,s)))
        show.blit(temp,(0,0))
        pygame.display.flip()
        temp=show.copy()
        while l:
                for event in pygame.event.get():
                        
                        if event.type==pygame.QUIT:
                                pygame.quit()
                        elif(event.type==pygame.MOUSEMOTION):
                                temp_arr=pt_arr[:]
                                (xr,yr)=pygame.mouse.get_pos()
                                show.blit(temp,(0,0))
                                pygame.draw.line(show,ml,(xr,0),(xr,y))
                                pygame.draw.line(show,ml,(xr,yr),(x,yr))
                                temp_arr.append((xr,yr))
                                linear_draw_base(temp_arr,0)
                                pygame.draw.rect (show, blk, Rect((xr-s/2,yr-s/2),(s,s)))
                                texts(xr-x,(xr+x)/2,yr)
                                texts(y-yr,xr,(y+yr)/2)
                                pygame.display.flip()
                        elif(event.type==pygame.MOUSEBUTTONDOWN):
                                if(pygame.mouse.get_pressed()[2]):
                                        show.blit(temp,(0,0))
                                        pygame.draw.rect (show, blk, Rect((xl-s/2,yl-s/2),(s,s)))
                                        l=False
                                else:
                                        show.blit(temp,(0,0))
                                        pygame.draw.line(show,ml,(xr,yr),(xr,y))
                                        pygame.draw.line(show,ml,(xr,yr),(x,yr))
                                        texts(xr-x,(xr+x)/2,yr)
                                        texts(y-yr,xr,(y+yr)/2)
                                        
                                        pt_arr.append((xr,yr))
                                        (xl,yl)=(xr,yr)
                                        linear_draw_base(pt_arr,1)
                                        del pt_arr[0]
                                        pygame.draw.rect (show, blk, Rect((xr-s/2,yr-s/2),(s,s)))
                                        temp=show.copy()
                                        texts(xr-x,(xr+x)/2,yr)
                                        texts(y-yr,xr,(y+yr)/2)
                                
                                pygame.display.flip()
        temp=show.copy()

def linear_start(temp,k,x,y):
        while k:
                for event in pygame.event.get():
                        
                        if event.type==pygame.QUIT:
                                pygame.quit()
                        elif(event.type==pygame.MOUSEMOTION):
                                (xr,yr)=pygame.mouse.get_pos()
                                
                                show.blit(temp,(0,0))
                                pygame.draw.rect (show, (0,0,0), Rect((xr-s/2,yr-s/2),(s,s)))
                                pygame.draw.line(show,ml,(xr,y),(xr,0))
                                pygame.draw.line(show,ml,(x,yr),(pw,yr))
                                texts(xr-x,(xr+x)/2,yr)
                                texts(y-yr,xr,(yr+y)/2)
                                pygame.display.flip()
                        elif(event.type==pygame.MOUSEBUTTONDOWN):
                                
                                a=pygame.mouse.get_pos()
                                pt_arr.append(a)
                                k=False
        fld.append(a)
        linear_base(a,show.copy(),x,y)

def calc(arr,x):
        t=0
        l=len(arr)
        f=0
        while(f<l):
                t=arr[f]*math.pow(x,f)+t
                f=f+1
        return t        

def load_pos_fx(x,temp_arr):
        r= len(temp_arr)
        c=0
        while(c<r):
                
                [(xl,yl),(xr,yr)]=temp_arr[c][1]
                if(x>=xl and x<xr):
                        y=calc(temp_arr[c][0],x)
                        return y
                c=c+1
        return -100

value =0


def load_value():
        global value
        def send():
                global value
                value = mainTextBox.get()
                onClick()

        def onClick():
                root.destroy()
        root = tk.Tk()
        mainLabel = tk.Label(root, text='enter load value ')
        mainLabel.pack()
        mainTextBox=tk.Entry(root)
        mainTextBox.pack()
        mySubmitButton = tk.Button(root, text='Submit', command=send)
        mySubmitButton.pack()
        quit = tk.Button(root, text=' Quit ', command=onClick)
        quit.pack()
        root.mainloop()

def load_points(temp):
        l=True
        global value
        show.blit(temp,(0,0))
        pygame.display.flip()
        temp=show.copy()
        while l:
                for event in pygame.event.get():
                        
                        if event.type==pygame.QUIT:
                                pygame.quit()
                        elif(event.type==pygame.MOUSEMOTION):
                                (xr,yr)=pygame.mouse.get_pos()
                                show.blit(temp,(0,0))
                                yr=load_pos_fx(xr,top[:])
                                pygame.draw.line(show,ld_rec,(xr,0),(xr,y))
                                pygame.draw.line(show,ld_rec,(xr,yr),(x,yr))
                                pygame.draw.rect (show, ld_rec, Rect((xr-s/2,yr-s/2),(s,s)))
                                texts(xr-x,(xr+x)/2,yr,ld_rec)
                                texts(y-yr,xr,(y+yr)/2,ld_rec)
                                pygame.display.flip()
                        elif(event.type==pygame.MOUSEBUTTONDOWN):
                                if(pygame.mouse.get_pressed()[2]):
                                        show.blit(temp,(0,0))
                                        l=False
                                else:
                                        show.blit(temp,(0,0))
                                        pygame.draw.line(show,ld_rec,(xr,yr),(xr,y))
                                        pygame.draw.line(show,ld_rec,(xr,yr),(x,yr))
                                        pygame.display.flip()
                                        texts(xr-x,(xr+x)/2,yr,ld_rec)
                                        texts(y-yr,xr,(y+yr)/2,ld_rec)
                                        load_value()
                                        if value!=0:
                                                temp_load_pt.append([xr,locale.atof(value)])
                                                pygame.draw.rect (show, ld_rec, Rect((xr-s/2,yr-s/2),(s,s)))
                                                text_load(value,xr,yr-2)
                                                temp=show.copy()
                                                value=0                 
                                pygame.display.flip()
        temp=show.copy()


def udl_polygo(temp,(xl,yl),yi,v,sc):
        l=True
        show.blit(temp,(0,0))
        pygame.draw.rect (show, udl_top_col, Rect((xl-s/2,yl-s/2),(s,s)))
        global pt_arr,yl_udl,val_udl,fld
        value=0
        fld[:]=[]
        
        pygame.display.flip()
        temp=show.copy()
        temp_arr=[]
        pt_arr.append((xl,yi))
        fld.append((xl,yi))
        (xr,yr)=(0,0)
        yn=yi
        while l:
                for event in pygame.event.get():
                        
                        if event.type==pygame.QUIT:
                                pygame.quit()
                        elif(event.type==pygame.MOUSEMOTION):
                                temp_arr=pt_arr[:]
                                (xm,ym)=pygame.mouse.get_pos()
                                show.blit(temp,(0,0))
                                temp_arr.append((xm,ym))
                                graph_draw(temp_arr,0,udl_top_col)
                                pygame.draw.line(show,udl_top_col,(xm,ym),(xm,y))
                                pygame.draw.line(show,udl_top_col,(xl,yl),(xm,yl))
                                pygame.draw.rect (show, udl_top_col, Rect((xm-s/2,yl-s/2),(s,s)))
                                pygame.draw.line(show,udl_top_col,(xm,ym),(x,ym))
                                texts(xm-x,(xm+x)/2,ym,udl_top_col)
                                text_load(float(v)+float(float((yi-ym))/sc),xm,ym)
                                pygame.display.flip()
                        elif(event.type==pygame.MOUSEBUTTONDOWN):
                                if(pygame.mouse.get_pressed()[2]):
                                        show.blit(temp,(0,0))
                                        pygame.draw.rect (show, udl_top_col, Rect((xr-s/2,yl-s/2),(s,s)))
                                        texts(xr-x,(xr+x)/2,ym,udl_top_col)
                                        yl_udl=yl
                                        val_udl=locale.atof(v)
                                        graph_draw(pt_arr,1,udl_top_col)
                                        fld.append((xr,yr))
                                        l=False
                                else:
                                        show.blit(temp,(0,0))
                                        text_load(float(v)+float(float((yi-ym))/sc),xm,ym)
                                        pygame.draw.line(show,udl_top_col,(xm,ym),(xm,yl))
                                        pygame.draw.line(show,udl_top_col,(xl,yl),(xm,yl))
                                        temp=show.copy()
                                        pt_arr.append((xm,ym))
                                        (xr,yr)=(xm,ym)
                                        graph_draw(pt_arr,0,udl_top_col)
                                        pygame.draw.rect (show, udl_top_col, Rect((xr-s/2,yl-s/2),(s,s)))
                                pygame.display.flip()
        temp=show.copy()

def udl_linear(temp,(xl,yl),yi,v,sc):
        l=True
        global pt_arr,yl_udl,val_udl,udl_top_col
        value=0
        show.blit(temp,(0,0))
        pygame.display.flip()
        temp=show.copy()
        pt_arr[:]=[]
        yn=yi
        while l:
                for event in pygame.event.get():
                        
                        if event.type==pygame.QUIT:
                                pygame.quit()
                        elif(event.type==pygame.MOUSEMOTION):
                                pt_arr[:]=[]
                                pt_arr.append((xl,yn))
                                (xm,ym)=pygame.mouse.get_pos()
                                show.blit(temp,(0,0))
                                pt_arr.append((xm,ym))
                                linear_draw(pt_arr,0,ldl_col)
                                pygame.draw.line(show,ldl_col,(xm,ym),(xm,y))
                                pygame.draw.line(show,ldl_col,(xl,yl),(xm,yl))
                                pygame.draw.line(show,ldl_col,(xm,ym),(x,ym))
                                texts(xm-x,(xm+x)/2,ym,ldl_col)
                                pygame.draw.rect (show, ldl_col, Rect((xm-s/2,yl-s/2),(s,s)))
                                text_load(float(v)+float(float((yi-ym))/sc),xm,ym)
                                pygame.display.flip()
                        elif(event.type==pygame.MOUSEBUTTONDOWN):
                                if(pygame.mouse.get_pressed()[2]):
                                        yl_udl=yl
                                        val_udl=float(v)
                                        show.blit(temp,(0,0))
                                        l=False
                                else:
                                        show.blit(temp,(0,0))
                                        linear_draw(pt_arr,yl,float(v),1,ldl_col)
                                        pygame.draw.line(show,ldl_col,(xm,ym),(xm,yl))
                                        pygame.draw.line(show,ldl_col,(xl,yl),(xm,yl))
                                        texts(xm-x,(xm+x)/2,ym,ldl_col)
                                        pygame.draw.rect (show, ldl_col, Rect((xm-s/2,yl-s/2),(s,s)))
                                        text_load(float(v)+float(float((yi-ym))/sc),xm,ym)
                                        yn=ym
                                        xl=xm
                                        temp=show.copy()                        
                                pygame.display.flip()
        temp=show.copy()


def supp(temp,p):
        l=True
        show.blit(temp,(0,0))
        pygame.display.flip()
        temp=show.copy()
        while l:
                for event in pygame.event.get():
                        
                        if event.type==pygame.QUIT:
                                pygame.quit()
                        elif(event.type==pygame.MOUSEMOTION):
                                (xr,yr)=pygame.mouse.get_pos()
                                show.blit(temp,(0,0))
                                yr=load_pos_fx(xr,bottom[:])
                                pygame.draw.line(show,sup_col[p],(xr,0),(xr,y))
                                pygame.draw.line(show,sup_col[p],(xr,yr),(x,yr))
                                pygame.draw.rect (show, sup_col[p], Rect((xr-s/2,yr-s/2),(s,s)))
                                texts(xr-x,(xr+x)/2,yr,sup_col[p])
                                texts(y-yr,xr,(y+yr)/2,sup_col[p])
                                pygame.display.flip()
                        elif(event.type==pygame.MOUSEBUTTONDOWN):
                                if(pygame.mouse.get_pressed()[2]):
                                        show.blit(temp,(0,0))
                                        l=False
                                else:
                                        show.blit(temp,(0,0))
                                        pygame.draw.line(show,sup_col[p],(xr,yr),(xr,y))
                                        pygame.draw.line(show,sup_col[p],(xr,yr),(x,yr))
                                        pygame.display.flip()
                                        texts(xr-x,(xr+x)/2,yr)
                                        texts(y-yr,xr,(y+yr)/2)
                                        temp_support.append([xr,p])
                                        pygame.draw.rect (show, sup_col[p], Rect((xr-s/2,yr-s/2),(s,s)))
                                        temp=show.copy()
                                pygame.display.flip()
        temp=show.copy()


def support_f(temp,p):
        supp(temp,p)
        (k,tempi)=confirm(show.copy())
        
        if k==1:
                for x in temp_support :
                        support.append(x)
                        
                temp_support[:] = []
                return tempi
        else:
                return temp



def udl(temp,(xl,yl),k):
        l=True
        global value
        value =0
        show.blit(temp,(0,0))
        pygame.display.flip()
        temp=show.copy()
        f=0
        while l:
                for event in pygame.event.get():
                        
                        if event.type==pygame.QUIT:
                                pygame.quit()
                        elif(event.type==pygame.MOUSEMOTION):
                                (xi,yi)=pygame.mouse.get_pos()
                                show.blit(temp,(0,0))
                                pygame.draw.line(show,cols[k],(xl,yi),(xl,yl))
                                pygame.display.flip()
                        elif(event.type==pygame.MOUSEBUTTONDOWN):
                                if(pygame.mouse.get_pressed()[2]):
                                        show.blit(temp,(0,0))
                                        l=False
                                else:
                                        show.blit(temp,(0,0))
                                        pygame.draw.line(show,cols[k],(xl,yi),(xl,yl))
                                        pygame.display.flip()
                                        load_value()
                                        text_load(value,xl,yi)
                                        temp=show.copy()
                                        l=False
                                        f=1
                                pygame.display.flip()
        temp=show.copy()
        if(f):
           func_load_udl[k](temp,(xl,yl),yi,value,10)

def load_udl_first(temp,k):
        l=True
        f=0
        show.blit(temp,(0,0))
        pygame.display.flip()
        temp=show.copy()
        while l:
                for event in pygame.event.get():
                        
                        if event.type==pygame.QUIT:
                                pygame.quit()
                        elif(event.type==pygame.MOUSEMOTION):
                                (xr,yr)=pygame.mouse.get_pos()
                                show.blit(temp,(0,0))
                                yr=load_pos_fx(xr,top[:])
                                pygame.draw.line(show,cols[k],(xr,0),(xr,y))
                                pygame.draw.line(show,cols[k],(xr,yr),(x,yr))
                                pygame.draw.rect (show, cols[k], Rect((xr-s/2,yr-s/2),(s,s)))
                                texts(xr-x,(xr+x)/2,yr,cols[k])
                                texts(y-yr,xr,(y+yr)/2,cols[k])
                                pygame.display.flip()
                        elif(event.type==pygame.MOUSEBUTTONDOWN):
                                if(pygame.mouse.get_pressed()[2]):
                                        show.blit(temp,(0,0))
                                        l=False
                                else:
                                        show.blit(temp,(0,0))
                                        pygame.draw.line(show,cols[k],(xr,yr),(xr,y))
                                        pygame.draw.line(show,cols[k],(xr,yr),(x,yr))
                                        texts(xr-x,(xr+x)/2,yr,cols[k])
                                        texts(y-yr,xr,(y+yr)/2,cols[k])
                                        pygame.draw.rect (show, cols[k], Rect((xr-s/2,yr-s/2),(s,s)))
                                        temp=show.copy()
                                        l=False
                                        f=1
                                pygame.display.flip()
        temp=show.copy()
        if(f):
           udl(temp,(xr,yr),k)


def load_udl_poly(temp,k):
        load_udl_first(temp,k)
        (k,tempi)=confirm(show.copy())
        global yl_udl,val_udl
        if k==1:
                udl_poly.append([coff[:],fld[:],yl_udl,val_udl])
                coff[:]=[]
                yl_udl=0
                fld[:]=[]
                val_udl=0
                return tempi
        else:
                return temp

def load_udl_line(temp,k):
        load_udl_first(temp,k)
        (k,tempi)=confirm(show.copy())
        global yl_udl,val_udl
        if k==1:
                for x in arr_rec :
                        udl_line.append(x)
                arr_rec[:]=[]
                yl_udl=0
                val_udl=0
                return tempi
        else:
                return temp



def load_point(temp):
        load_points(temp)
        (k,tempi)=confirm(show.copy())
        
        if k==1:
                for x in temp_load_pt :
                        load_pt.append(x)
                        
                temp_load_pt[:] = []
                return tempi
        else:
                return temp

def linear_top(temp,x,y):
        temp
        linear_start(temp,True,x,y)
        (k,tempi)=confirm(show.copy())
        
        if k==1:
                for x in arr_rec :
                        top.append(x)
                
                fld[:]     = []
                coff[:]    = []
                arr_rec[:] = []
                
                return tempi
        else:
                return temp
                
def linear_bottom(temp,x,y):
        temp
        linear_start(temp,True,x,y)
        (k,tempi)=confirm(show.copy())
        
        if k==1:
                for x in arr_rec :
                        bottom.append(x)
                
                fld[:]     = []
                coff[:]    = []
                arr_rec[:] = []
                
                return tempi
        else:
                return temp

def polynomial_top(temp,x,y):
        temp
        polynomial_start(temp,True,x,y)
        (k,tempi)=confirm(show.copy())
        if k==1:
                top.append([coff[:],fld[:],0])
                fld[:]=[]
                coff[:]=[]
                
                return tempi
        else:
                return temp
                
def polynomial_bottom(temp,x,y):
        temp
        polynomial_start(temp,True,x,y)
        (k,tempi)=confirm(show.copy())
        if k==1:
                bottom.append([coff[:],fld[:],0])
                fld[:]=[]
                coff[:]=[]
                
                return tempi
        else:
                return temp
                

def menu_udl():
        side.fill(red)
        pygame.draw.rect(side,button,button_udll)
        pygame.draw.rect(side,button,button_udlp)
        pygame.draw.rect (side, button, button_back)
        texts_butt("poly",txt,22)
        texts_butt("line",txt,52)
        texts_butt("BACK",txt,442)
        pygame.display.flip()
        p=True
        while p:
                for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                                pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                                (xt,yt)=pos
                                ## check if cursor is on button ##
                                if button_pointl.collidepoint((xt-540,yt)):
                                        show.blit(load_udl_poly(show.copy(),1),(0,0))
                                        pygame.display.flip()
                                        
                                
                                elif button_pointc.collidepoint((xt-540,yt)):
                                        show.blit(load_udl_line(show.copy(),0),(0,0))
                                        pygame.display.flip()
                                        
                                elif button_back.collidepoint((xt-540,yt)):
                                        p=False




def menu_load():
        side.fill(red)
        pygame.draw.rect(side,button,button_pointl)
        pygame.draw.rect(side,button,button_pointc)
        pygame.draw.rect (side, button, button_back)
        texts_butt("point",txt,22)
        texts_butt("UDL",txt,52)
        texts_butt("BACK",txt,442)
        pygame.display.flip()
        p=True
        while p:
                for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                                pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                                (xt,yt)=pos
                                ## check if cursor is on button ##
                                if button_pointl.collidepoint((xt-540,yt)):
                                        show.blit(load_point(show.copy()),(0,0))
                                        pygame.display.flip()
                                        
                                
                                elif button_pointc.collidepoint((xt-540,yt)):
                                        menu_udl()
                                        pygame.display.flip()
                                        
                                elif button_back.collidepoint((xt-540,yt)):
                                        p=False


        


def menu(k):
        side.fill(red)
        pygame.draw.rect(side,button,button_polynomial)
        pygame.draw.rect(side,button,button_linear)
        pygame.draw.rect (side, button, button_back)
        texts_butt("poly",txt,22)
        texts_butt("line",txt,52)
        texts_butt("BACK",txt,442)
        pygame.display.flip()
        p=True
        while p:
                for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                                pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                                (xt,yt)=pos
                                ## check if cursor is on button ##
                                if button_polynomial.collidepoint((xt-540,yt)):
                                        show.blit(func_poly[k](show.copy(),x,y),(0,0))
                                        pygame.display.flip()
                                        
                                
                                elif button_linear.collidepoint((xt-540,yt)):
                                        show.blit(func_line[k](show.copy(),x,y),(0,0))
                                        pygame.display.flip()
                                        
                                elif button_back.collidepoint((xt-540,yt)):
                                        p=False





def reset():
        global pt_arr,arr_rec
        pt_arr[:]=[]
        arr_rec[:]=[]


def display_support():
        side.fill(red)  
        pygame.draw.rect (side, button, button_hinge)
        pygame.draw.rect (side, button, button_fixed)
        pygame.draw.rect (side, button, button_shre)
        pygame.draw.rect (side, button, button_inhi)
        pygame.draw.rect (side, button, button_back)
        texts_butt("Hinge",txt,22)
        texts_butt("Fixed",txt,52)
        texts_butt("SH Re",txt,82)
        texts_butt("In Hin",txt,112)
        texts_butt("BACK",txt,442)
        pygame.display.flip()
        p=True
        while p:
                for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                                pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                                (xt,yt)=pos
                                ## check if cursor is on button ##
                                if button_hinge.collidepoint((xt-540,yt)):
                                        show.blit(support_f(show.copy(),1),(0,0))
                                        pygame.display.flip()
                                        
                                
                                elif button_fixed.collidepoint((xt-540,yt)):
                                        show.blit(support_f(show.copy(),0),(0,0))
                                        pygame.display.flip()
                                        
                                elif button_shre.collidepoint((xt-540,yt)):
                                        show.blit(support_f(show.copy(),3),(0,0))
                                        pygame.display.flip()
                                        
                                elif button_inhi.collidepoint((xt-540,yt)):
                                        show.blit(support_f(show.copy(),2),(0,0))
                                        pygame.display.flip()
                                        
                                elif button_back.collidepoint((xt-540,yt)):
                                        p=False



def display_main():
        reset()
        side.fill(red)  
        pygame.draw.rect (side, button, button_top)
        pygame.draw.rect (side, button, button_bottom)
        pygame.draw.rect (side, button, button_load)
        pygame.draw.rect (side, button, button_sup)
        pygame.draw.rect (side, button, button_export)
        pygame.draw.line(show,(150,100,10),(x,0),(x,ph))
        pygame.draw.line(show,(150,100,10),(0,y),(pw,y))
        texts_butt("Top",txt,22)
        texts_butt("Bottom",txt,52)
        texts_butt("Load",txt,82)
        texts_butt("Support",txt,112)
        texts_butt("Export",txt,142)
        pygame.display.flip()

def main():     
        display_main()
        while True:
                for event in pygame.event.get():
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        
                        ## if mouse is pressed get position of cursor ##
                        pos = pygame.mouse.get_pos()
                        (xt,yt)=pos
                        ## check if cursor is on button ##
                        if button_bottom.collidepoint((xt-540,yt-0)):
                                menu(0)
                                display_main()
                        elif button_top.collidepoint((xt-540,yt-0)):
                                menu(1)
                                display_main()
                        elif button_load.collidepoint((xt-540,yt-0)):
                                menu_load()
                                display_main()
                        elif button_sup.collidepoint((xt-540,yt-0)):
                                display_support()
                                display_main()
                        elif button_export.collidepoint((xt-540,yt-0)):
                                wrt_file()
func_poly=[polynomial_bottom,polynomial_top]
func_line=[linear_bottom,linear_top]
func_load_udl=[udl_linear,udl_polygo]
main()
