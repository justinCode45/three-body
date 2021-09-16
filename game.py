import random
import neat
import pygame as pg
import math
import numpy
import time







G=50            #萬有引力常數
WIDTH = 1280    #視窗寬
HEIGT=  720     #視窗長
FPS=30          #FPS
MAX_SPEED=17    #球體的速限
PLAYER_MASS=500 #玩家的質量





def indt (x,y) :
    '''
    象限判斷
    '''
    if x>0 and y>0 :
        return 1
    if x<0 and y>0 :
        return 2
    if x<0 and y<0 :
        return 3
    if x>0 and y<0 :
        return 4

def timec(x) :
    '''
    把時間的數字轉換成字串
    '''
    x=int(x)
    if x< 60 :
        if x<10 :
            return "00 : 0"+str(x)
        else :
            return "00 : "+str(x)
    if x>60 :
        min= x//60
        x=x%60
        if min<10 and x<10 :
            return "0"+str(min)+" : "+"0"+str(x)
        if min<10 and x>=10 :
            return "0"+str(min)+" : "+str(x)
        if min>=10 and x<10 :
            return str(min)+" : "+"0"+str(x)
        if min>=10 and x>=10 :
            return str(min)+" : "+str(x)

    
    
class points(pg.sprite.Sprite) :
    '''
    分數的角色
    '''
    def __init__(self) :
        super().__init__()
        self.point=pg.Surface((30,30)).convert()
        self.point.set_colorkey((0, 0, 0))
        pg.draw.circle(self.point, (255,96,10), (15,15), 15, 0)
        self.rect = self.point.get_rect()
        self.rect.center =( random.randint(100,1100),random.randint(100,600))
        self.x =self.rect.centerx
        self.y = self.rect.centery 




class ball(pg.sprite.Sprite) :
    '''
    一顆有引力的球
    '''

    def __init__(self,hh,mas=10) :
        super().__init__() 
        self.mass=mas
        self.ball = pg.Surface((70,70)).convert() #建立球矩形繪圖區
        self.ball.set_colorkey((0, 0, 0))    #矩形區塊背景為透明
        pg.draw.circle(self.ball, (random.randint(100,200),random.randint(100,200),random.randint(100,200)), (35,35), 35, 0)  #畫藍色球
        self.rect = self.ball.get_rect()
        if hh==0 :
            self.rect.center =( 350,250)
        else :
            self.rect.center =( 930,250)
    
        
    
        self.x =self.rect.centerx
        self.y = self.rect.centery   
    
        self.speed_x=0
        self.speed_y=0
        
        
    def move (self,o1,o2):
        #判定碰撞,邊界,移動方向 
        self.vector(o1,o2)  
        self.hit(o1)   
        self.br()
        
        #速度限制
        if self.speed_x>MAX_SPEED :
            self.speed_x=MAX_SPEED 
        if self.speed_y>MAX_SPEED :
            self.speed_y=MAX_SPEED  

        #移動
        self.x += self.speed_x
        self.y +=self.speed_y 
        self.rect.center=(self.x,self.y)
    
    def hit  (self,o1) :
        '''
        球與球的碰撞判斷
        '''

        r1=((self.x-o1.x)**2+(self.y-o1.y)**2)**0.5
        #判斷碰撞
        if r1<=70  :
            
            #取得原本的角度和利用斜率取得些線的角度
            orth,jkjk=self.gravity(o1)
            m=(self.y-o1.y)/(self.x-o1.x)
            mthat=math.atan(m)
            #這裡切線的角度會有兩個,以原點分為兩段
            if mthat<0 :
                mthat+=2*math.pi
                cutline1,cutline2=mthat-(math.pi),mthat
            cutline1,cutline2=mthat,mthat+(math.pi)
            
            #判斷最終反彈的角度
            if abs(cutline1-orth)>abs(cutline2-orth) :
                kt=cutline2-orth
                fina=cutline1+kt
            else :
                kt=cutline1-orth
                fina=cutline2+kt

            #更改移動速度
            f=(self.speed_x**2+self.speed_y**2)**0.5
            self.speed_x=f*math.cos(fina)
            self.speed_y=f*math.sin(fina)
        



    def br (self) :
        '''
        球與邊界的碰撞判斷
        '''
        #為了防止球卡在邊界裡，所以在反彈時強制移動到邊界上
        if self.rect.left <=0  :
            self.speed_x *=-1
            self.x=36
        if  self.rect.right >= WIDTH :
            self.speed_x *=-1
            self.x=WIDTH-36
        if self.rect.top <=0  :
            self.speed_y*=-1
            self.y=36
        if  self.rect.bottom >= HEIGT :
            self.speed_y*=-1
            self.y=HEIGT-36

    def gravity (self,o1) :
        '''
        引力大小方向計算
        '''
        #取得距離
        del_x = o1.x-self.x
        del_y = o1.y-self.y
        r2 =del_x**2 +del_y **2
        #計算引力
        f=self.mass*o1.mass*G/r2

        #算出引力的角度
        theta=math.acos(del_x/r2**0.5)
        Quadr=indt(del_x,del_y)
        if Quadr==3 or Quadr==4 :
            #當角度為第三第四象限時，補上角度
            theta= 2*math.pi-theta
        
        return theta,f
  
    def vector (self,o1,o2) :
        '''
        兩個引力合成
        '''
        #分別算出兩個引力在xy上的分量，在合成
        theta1,f1=self.gravity(o1)
        theta2,f2=self.gravity(o2)
        fx1,fy1=f1*math.cos(theta1),f1*math.sin(theta1)
        fx2,fy2=f2*math.cos(theta2),f2*math.sin(theta2)
        
        f_x=fx1+fx2
        f_y=fy1+fy2

        a_x=f_x/self.mass
        a_y=f_y/self.mass
        self.speed_x += a_x
        self.speed_y +=a_y
        
        
class players(pg.sprite.Sprite) :

    def __init__ (self,mas=PLAYER_MASS) :
        super().__init__()
        self.mass=mas
        self.player=pg.Surface((70,70)).convert()
        self.player.set_colorkey((0, 0, 0))
        pg.draw.circle(self.player, (100,100,100), (35,35), 35, 0)
        self.rect = self.player.get_rect()
        self.rect.center =( 640,600)
        self.x =self.rect.centerx
        self.y = self.rect.centery

    def move(self,key) :
        #根據鍵盤移動
        if key ==0 :
            self.y-=10
        if key==1 :
            self.x+=10
        if key ==2 :
            self.x-=10 
        if key ==3:
            self.y+=10
        self.rect.center=(self.x,self.y)
        #防止穿牆
        ke=self.br()
        if 1 in ke :
            self.x=35
        if 2 in ke :
            self.x=WIDTH-35
        if 3 in ke :
            self.y=35
        if 4 in ke :
            self.y=HEIGT-35
        self.rect.center=(self.x,self.y)

    def br (self) :
        '''
        球與邊界的碰撞判斷
        '''
        ke=[]
        if self.rect.left <=0    :
            ke.append(1)
        if self.rect.right >= WIDTH:
            ke.append(2)
        if self.rect.top <=0  :
            ke.append(3)
        if  self.rect.bottom >= HEIGT :
            ke.append(4)
        return ke 


        



  
def main () :

    pg.init()

    screen = pg.display.set_mode((WIDTH,HEIGT)) 

    pg.display.set_caption("三體")         
    bg = pg.Surface((WIDTH,HEIGT))
    bg = bg.convert_alpha()
    bg.fill((255,255,255))
    screen.blit(bg, (0,0))
    qrun=True
    times =0
    best_point=0

    #大迴圈控制整的遊戲
    while qrun :
        bg.fill((255,255,255))
        dan=pg.sprite.Group()
        bal=[]
        mun=2
        for i in range(0,mun) :
            bal.append(ball(mas=20*(i+1),hh=i))
            dan.add(bal[i])
            
        player=players()     

        point=points() 
        ponum=0

        clock = pg.time.Clock()        #建立時間元件

        
        running = True
        
        font=pg.font.SysFont("./TaipeiSansTC.ttf", 30)

        #小迴圈控制每次的遊戲
        while running:

                
            times += 1/FPS  #時間計算
            clock.tick(FPS) 

            #分別顯示時間,分數,最佳分數       
            text = font.render(timec(times), True, (0,0,255), (255,255,255))
            po=font.render("Score : "+str(ponum),True,(0,0,255),(255,255,255))
            bp=font.render("Best Score : "+str(best_point),True,(0,0,255),(255,255,255))
            
            #按下叉叉時，退出兩個迴圈
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    qrun=False

            #得分判斷        
            rx=((player.x-point.x)**2+(player.y-point.y)**2)**0.5
            if rx<=50 :
                point.kill()
                point=points()
                ponum+=1

            #玩家移動判斷
            key=pg.key.get_pressed()
            if key[pg.K_w] :
                player.move(0)
            if key[pg.K_d] :
                player.move(1)
            if key[pg.K_a] :
                player.move(2)
            if key[pg.K_s] :
                player.move(3)
            
            #球體移動
            for x in [[0,1],[1,0]] :
                bal[x[0]].move(bal[x[1]],player)  
            

            #重畫背景    
            screen.blit(bg, (0,0))
            screen.blit(point.point,point.rect.topleft)
            for i in range(0,mun) :
                #畫出每一個球
                screen.blit(bal[i].ball, bal[i].rect.topleft)

            screen.blit(player.player,(player.rect.topleft))    
            screen.blit(text, (50,50))
            screen.blit(po, (300,50))
            screen.blit(bp,(450,50))
            
        
            pg.display.update()

            #判定球體與玩家是否碰撞
            r1=((player.x-bal[0].x)**2+(player.y-bal[0].y)**2)**0.5
            r2=((player.x-bal[1].x)**2+(player.y-bal[1].y)**2)**0.5

            if r1<=70 or r2<=70 :
                running=False
                player.kill()
                bal[0].kill()
                bal[1].kill()
                point.kill()
                bg.fill((0,0,0,40))
                screen.blit(bg, (0,0))
                pg.display.update()
                time.sleep(0.05)
                if ponum>best_point :
                    best_point=ponum
                

  
    

    

        
    pg.quit()





if __name__ =="__main__" :
    main()