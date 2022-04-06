import pygame
import os
import datetime
from datetime import date
pygame.font.init()

from tkinter import *
from tkinter import messagebox



present_date=str(date.today())

#create database connection
import mysql.connector
mydb=mysql.connector.connect(host="127.0.0.1", user="root", password="mysqllogin@13", database="db1")
mycursor=mydb.cursor()

query1="insert into opm_game(winner,dated) values(%s,%s)"
query2="select * from opm_game"
values=[]


w,h=1000,600
win=pygame.display.set_mode((w,h))
pygame.display.set_caption("shooting game ")
white=(255,255,255)
black=(0,0,0)
YELLOW=(255,255,0)
GREEN=(0,255,0)
vel=5
fps=60
cw,ch=60,80
border=pygame.Rect(w//2 -2,0,4,h)

max_b=3
bullet_vel=15

genos_image=pygame.image.load(os.path.join("images","939400.jpg"))
genos=pygame.transform.scale(genos_image,(cw,ch))
saitama_image=pygame.image.load(os.path.join("images","939408.jpg"))
saitama=pygame.transform.scale(saitama_image,(cw,ch))
background_image=pygame.image.load(os.path.join("images","499522.jpg"))
background=pygame.transform.scale(background_image,(w,h))

redhit=pygame.USEREVENT +1
yellowhit=pygame.USEREVENT + 2

red_health=10
yellow_health=10

health_font=pygame.font.SysFont("comicsans",40)
winner_font=pygame.font.SysFont("comicsans",100)



def draw_window(red,yellow,red_b,yellow_b,red_health,yellow_health):
    win.blit(background,(0,0))
    pygame.draw.rect(win,black,border)
    red_ht=health_font.render("health: "+ str(red_health),1,white)
    yellow_ht=health_font.render("health: "+ str(yellow_health),1,white)
    win.blit(red_ht,(10,10))
    win.blit(yellow_ht,(w - red_ht.get_width() -10,10))
    win.blit(genos,(red.x,red.y))
    win.blit(saitama,(yellow.x,yellow.y))

    for bullet in red_b:
        pygame.draw.rect(win,GREEN,bullet)
    for bullet in yellow_b:
        pygame.draw.rect(win,YELLOW,bullet)
    pygame.display.update()

def draw_winner(text):
    draw_text=winner_font.render(text,1,white)
    win.blit(draw_text,(w//2 -draw_text.get_width()//2,h//2 -draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(2000)
    win.blit(background, (0,0))
    pygame.display.update()


def red_mov(kp,red):
    if kp[pygame.K_a] and red.x -vel >0:
        red.x -=vel
    if kp[pygame.K_d] and red.x + vel + red.width <border.x:
        red.x +=vel
    if kp[pygame.K_w] and red.y- vel>0:
        red.y -=vel
    if kp[pygame.K_s] and red.y + vel + red.height < h:
        red.y +=vel

def yellow_mov(kp,yellow):
    if kp[pygame.K_LEFT] and yellow.x - vel >border.x + border.width:
        yellow.x -=vel
    if kp[pygame.K_RIGHT] and yellow.x + vel + yellow.width<w:
        yellow.x +=vel
    if kp[pygame.K_UP] and yellow.y-vel >0:
        yellow.y -=vel
    if kp[pygame.K_DOWN] and yellow.y +vel + yellow.height < h:
        yellow.y +=vel


def bullet_movement(red_b,yellow_b,red,yellow):
    for bullet in red_b:
        bullet.x +=bullet_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellowhit))
            red_b.remove(bullet)
        elif bullet.x>w:
            red_b.remove(bullet)
    for bullet in yellow_b:
        bullet.x -=bullet_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(redhit))
            yellow_b.remove(bullet)
        elif bullet.x<0:
            yellow_b.remove(bullet)
        
def main():
    red_b=[]
    yellow_b=[]

    red_health=10
    yellow_health=10


    red=pygame.Rect(100,300,cw,ch)
    yellow=pygame.Rect(750,300,cw,ch)
    clock =pygame.time.Clock()


    run=True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                if event.key ==pygame.K_LCTRL and len(red_b)<max_b:
                    bullet=pygame.Rect(red.x +red.width, red.y +red.height//2 -2,10,5)
                    red_b.append(bullet)
                if event.key ==pygame.K_RCTRL and len(yellow_b)<max_b:
                    bullet=pygame.Rect(yellow.x, yellow.y +yellow.height//2 -2,10,5)
                    yellow_b.append(bullet)

            if event.type==redhit:
                red_health -=1
            if event.type==yellowhit:
                yellow_health -=1
        
        winnertext=""
        if red_health <=0:
            winnertext="Saitama wins "
            value=(winnertext,present_date)
            values.append(value)
            mycursor.executemany(query1,values)
            mydb.commit()

        if yellow_health<=0:
            winnertext="Genos wins "
            value=(winnertext,present_date)
            values.append(value)
            mycursor.executemany(query1,values)
            mydb.commit()

        if winnertext !="":
            draw_winner(winnertext)
            mycursor.execute(query2)
            score_card=mycursor.fetchall()
            Tk().wm_withdraw() #to hide the main window
            messagebox.showinfo('Scorecard','\n'.join(map(str, score_card)))
            break

        kp=pygame.key.get_pressed()
        red_mov(kp,red)
        yellow_mov(kp,yellow)
        bullet_movement(red_b,yellow_b,red,yellow)
        draw_window(red,yellow,red_b,yellow_b,red_health,yellow_health)
    main()

if __name__=="__main__":

    main()


    