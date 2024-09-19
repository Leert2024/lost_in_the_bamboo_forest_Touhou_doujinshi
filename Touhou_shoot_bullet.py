#coding:utf-8
from time import sleep
from random import randint,uniform,choice
from math import pi,sin,cos,acos,asin
from scene import *
from Touhou_class import Bullet,Laser
from sound import play_effect,stop_all_effects
A=Action
#定义常量以存储子弹的判定半径

SMALL_BULLET = 3
SMALL_RING = 4
BIG_BULLET = 8
BIG_JADE = 12
STAR = 8
JELLY_FISH = 4
BUTTERFLY = 4

def shoot_small_bullet(sel,meteor,tex,num,sle):
	sleep(1)
	while 1:
		if sel.game_part==4.35 or not meteor.parent:
			return 
		elif sel.game_over==True:
			sleep(1)
		else:
			play_effect('Sound/se_tan02.mp3')
			for i in range(num):
				try:
					bullet =Bullet(SMALL_BULLET,texture=Texture(choice(tex)),parent=sel)
				except KeyError:
					pass
				bullet.position = meteor.position
				actions = [A.move_by(randint(-200,200),-1.1*sel.size.h,randint(6,10)), A.remove()]
				bullet.run_action (A.sequence(actions))
			sleep(sle)
			
def shoot_big_bullet(meteor,progress):
	if not meteor.parent or meteor.parent.game_over==True:
		return
	play_effect('Sound/shoot_bullet_1.m4a')
	bullet = Bullet(BIG_BULLET,parent = meteor.parent,texture = Texture('Bullet/big_bullet.PNG'),position=meteor.position)
	dis=((meteor.parent.player.position.x-bullet.position.x)**2+(meteor.parent.player.position.y-bullet.position.y)**2)**0.5
	actions = [A.move_by(meteor.parent.size.h*(meteor.parent.player.position.x-bullet.position.x)/dis, meteor.parent.size.h*(meteor.parent.player.position.y-bullet.position.y)/dis,3),A.remove()]
	bullet.run_action (A.sequence(actions))

def shoot_bullet_6(sel,meteor):
	time_=0
	lis1=[BIG_BULLET,BIG_JADE,STAR]
	lis2=['Bullet/big_bullet.PNG','Bullet/big_jade_blue.PNG','Bullet/star_green.PNG']
	lis3=[3,6,4]
	while 1:
		time_+=1
		for i in range(21):
			if sel.game_part==4.45:
				return 
			elif sel.game_over==True:
				sleep(2)
			else:
				play_effect('Sound/se_tan02.mp3')
				bullet = Bullet(lis1[i%3],texture=Texture(lis2[i%3]),parent=sel)
				bullet.position=meteor.position
				if i%3==2:
					bullet.run_action (A.rotate_by(6*pi,4))
				actions =[A.move_by(sel.size.h*math.cos(time_/6+i*pi/10),-1*sel.size.h*math.sin(time_/6+i*pi/10),lis3[i%3]),A.remove()]
				bullet.run_action (A.sequence(actions))
				sleep(0.03)

#符卡「虚无缥缈蓬莱山」
def shoot_bullet_7(sel,meteor):
	while 1:
		if sel.game_part==4.55:
			return 
		elif sel.game_over==True:
				sleep(2)
		else:
			lis=[]
			start_pos_x = randint(-10,int(sel.size.w)+10)
			play_effect('Sound/shoot_bullet_1.m4a')
			for i in range(20):
				bullet = Bullet(SMALL_BULLET,texture=Texture('Bullet/small_bullet_green.PNG'),parent=sel)
				bullet.position = (start_pos_x+math.cos(i*pi/10)*100+randint(-5,5),sel.size.h+20+math.sin(i*pi/10)*100+randint(-5,5))
				lis.append(bullet)
			end_x=randint(-10,int(sel.size.w+10))
			for	i in lis:
				i.run_action (A.sequence(A.move_to(i.position.x+end_x,i.position.y-sel.size.h-200,7,TIMING_EASE_IN_2),A.remove()))
			play_effect('Sound/se_laser01.mp3')
			laser=Laser(texture=Texture('Bullet/laser_blue.PNG'),parent=sel,position=(-130,randint(0,int(sel.size.h))))
			laser.run_action(A.sequence(A.move_by(260+sel.size.w,0,2),A.remove()))
			sleep(0.5)
			
def shoot_bullet_8(sel,meteor,type):
	while 1:
		if not meteor.parent:
			return
		elif sel.game_over==True:
			sleep(2)
		else:
			play_effect('Sound/se_tan02.mp3')
			for i in [-1,1]:
				bullet=Bullet (JELLY_FISH,parent=sel,position=meteor.position,y_scale=-i)
				if type==-1:
					bullet.texture=Texture ('Bullet/jelly_fish_yellow.PNG')
					bullet.run_action (A.sequence(A.move_by(0,-sel.size.h*i,4,TIMING_EASE_IN),A.remove()))
				else:
					bullet.texture=Texture ('Bullet/jelly_fish_blue.PNG')
					bullet.run_action (A.sequence(A.move_by(0,-sel.size.h*i,6,TIMING_EASE_IN),A.remove()))
		sleep(0.5)
		
def shoot_bullet_9(sel,meteor):
	sleep(1)
	while 1:
		if not meteor.parent:
			return
		elif sel.game_over==True:
			sleep(2)
		else:
			play_effect('Sound/shoot_bullet_1.m4a')
			lis=[]
			for i in range(12):
				bullet = Bullet (SMALL_BULLET,texture=Texture('Bullet/small_bullet_red.PNG'),parent=sel,position=meteor.position)
				bullet.run_action (A.sequence (A.move_by (100*cos(pi*i/6) ,100*sin (pi*i/6),0.5,TIMING_EASE_OUT),A.move_by(sel.size.h*(sel.player.position.x-bullet.position.x-100*cos(pi*i/6))/((sel.player.position.x-bullet.position.x)**2+(sel.player.position.y-bullet.position.y)**2)**0.5, sel.size.h*(sel.player.position.y-bullet.position.y-100*sin(pi*i/6))/((sel.player.position.x-bullet.position.x)**2+(sel.player.position.y-bullet.position.y)**2)**0.5,1.5),A.remove()))
			sleep(0.5)
			for i in range(2):
				sleep(0.15)
				play_effect('Sound/se_tan02.mp3')
				for i in range(10):
					rot=uniform(0,2*pi)
					bullet = Bullet (JELLY_FISH,texture=Texture('Bullet/jelly_fish_white.PNG'),parent=sel,position=meteor.position)
					bullet.rotation=rot-pi/2
					bullet.run_action (A.sequence(A.move_by(sel.size.h*cos(rot),sel.size.h*sin(rot),6),A.remove()))
		sleep(0.2)
def shoot_bullet_10(sel,meteor):
	sleep(1)
	while 1:
		if not meteor.parent:
			return
		elif sel.game_over==True:
			sleep(2)
		else:
			dis=((sel.player.position.x-meteor.position.x)**2+(sel.player.position.y-meteor.position.y)**2)**0.5
			rot_cos=(sel.player.position.x-meteor.position.x)/dis
			rot_sin=(sel.player.position.y-meteor.position.y)/dis
			for i in range(5):
				play_effect('Sound/se_tan02.mp3')
				for j in range(i+1):
					bullet = Bullet (SMALL_RING,texture=Texture('Bullet/small_ring_red.PNG'),parent=sel,position=meteor.position+(-rot_sin*30*(j-i/2),rot_cos*30*(j-i/2)))
					bullet.run_action (A.sequence(A.move_by(sel.size.h*rot_cos,sel.size.h*rot_sin,3),A.remove()))
				sleep(0.1)
			sleep(2)
			
def shoot_bullet_11(sel,meteor):
	sleep(1)
	while 1:
		if sel.game_part!=8.15:
			return 
		elif sel.game_over==True:
			sleep(2)
		else:
			play_effect('Sound/se_tan02.mp3')
			for i in range(30):
				bullet = Bullet(SMALL_BULLET,texture=Texture('Bullet/small_bullet_yellow.PNG'),parent=sel,position=meteor.position)
				bullet.run_action(A.sequence(A.move_by(80*cos(2*pi*i/30),80*sin(2*pi*i/30),0.5,TIMING_EASE_OUT),A.move_by(sel.size.h*cos(2*pi*i/30+2*(-1)**i),sel.size.h*sin(2*pi*i/30+2*(-1)**i),12,TIMING_EASE_OUT),A.remove()))
			meteor.run_action (A.call(shoot_big_bullet,0.01))
			sleep(0.6)
			
def shoot_bullet_12(sel,meteor):
	sleep(1)
	while 1:
		for j in range(3):
			play_effect('Sound/shoot_bullet_1.m4a')
			for i in range(20-j):
				bullet = Bullet(SMALL_BULLET,texture=Texture('Bullet/small_bullet_yellow.PNG'),parent=sel,position=meteor.position)
				bullet.run_action (A.move_to(15+30*j,sel.size.h-100-(sel.size.h-100)/20*i,3,TIMING_EASE_OUT))
			for i in range(20-j):
				bullet = Bullet(SMALL_BULLET,texture=Texture('Bullet/small_bullet_yellow.PNG'),parent=sel,position=meteor.position)
				bullet.run_action (A.move_to(sel.size.w-15-30*j,sel.size.h-100-(sel.size.h-100)/20*i,3,TIMING_EASE_OUT))
			for i in range(11-2*j):
				bullet = Bullet(SMALL_BULLET,texture=Texture('Bullet/small_bullet_yellow.PNG'),parent=sel,position=meteor.position)
				bullet.run_action (A.move_to(j*30+15+(sel.size.w-30-j*60)*(i+1)/(12-2*j),15+30*j,3,TIMING_EASE_OUT))
			sleep(0.5)
		while 1:
			if sel.game_part!=8.25:
				return 
			elif sel.game_over==True:
				break
			else:
				play_effect('Sound/shoot_bullet_1.m4a')
				bullet = Bullet (BIG_JADE,texture=Texture('Bullet/big_jade_white.PNG'),parent=sel,position=meteor.position)
				bullet.run_action (A.sequence(A.move_to(randint(75,int(sel.size.w)-75),90,3,TIMING_EASE_IN),A.call(shoot_bullet_13,0.01),A.wait(0.1),A.remove()))
				sleep(1)
		sleep(2)

def shoot_bullet_13(meteor,progress):
	play_effect('Sound/se_tan02.mp3')
	for i in range(10):
		bullet = Bullet (BIG_BULLET,texture=Texture('Bullet/big_bullet_white.PNG'),parent=meteor.parent)
		bullet.position=meteor.position
		bullet.run_action (A.sequence(A.move_by(meteor.parent.size.h*cos(2*pi*i/10),meteor.parent.size.h*sin(2*pi*i/10),4),A.remove()))

def shoot_bullet_14(sel,meteor):
	sleep(1)
	while 1:
		if sel.game_part!=8.35:
			return 
		elif sel.game_over==True:
			sleep(2)
		else:
			play_effect('Sound/se_tan02.mp3')
			for i in range(30):
				bullet = Bullet(SMALL_BULLET,texture=Texture('Bullet/small_bullet_red.PNG'),parent=sel,position=meteor.position)
				bullet.run_action(A.sequence(A.move_by(80*cos(2*pi*i/30),80*sin(2*pi*i/30),0.5,TIMING_EASE_OUT),A.move_by(sel.size.h*cos(2*pi*i/30+2),sel.size.h*sin(2*pi*i/30+2),12,TIMING_EASE_OUT),A.remove()))
			meteor.run_action (A.call(shoot_big_bullet,0.01))
			sleep(0.6)
			
def shoot_bullet_15(sel,meteor):
	sleep(1)
	while 1:
		if sel.game_part!=8.45:
			return 
		elif sel.game_over==True:
			sleep(2)
		else:
			play_effect('Sound/shoot_bullet_1.m4a')
			for i in range(2):
				x1=randint(0,int(sel.size.w))
				bullet = Bullet(SMALL_BULLET,texture=Texture('Bullet/big_jade_white.PNG'),parent=sel,position=(x1,-10))
				x2=randint(0,int(sel.size.w))
				bullet.run_action(A.sequence(A.move_to((x2+x1)/2,sel.size.h-100,3,TIMING_EASE_OUT_2),A.call(shoot_bullet_16,0.01),A.move_to(x2,-10,3,TIMING_EASE_IN_2),A.remove()))
				sleep(0.1)
			sleep(0.7)

def shoot_bullet_16(meteor,progress):
	play_effect('Sound/se_tan02.mp3')
	for i in range(6):
		bullet = Bullet (BUTTERFLY,texture=Texture('Bullet/butterfly_purple.PNG'),parent=meteor.parent,position=meteor.position)
		bullet.rotation=2*pi/6*i-pi/2
		bullet.run_action (A.sequence(A.move_by(meteor.parent.size.h*cos(2*pi*i/6),meteor.parent.size.h*sin(2*pi*i/6),4),A.remove()))

def shoot_bullet_17(sel,meteor):
	sleep(1)
	while 1:
		if sel.game_part!=8.55:
			return 
		elif sel.game_over==True:
			sleep(2)
		else:
			play_effect('Sound/se_tan02.mp3')
			for i in range(30):
				bullet = Bullet(SMALL_BULLET,texture=Texture('Bullet/small_bullet_green.PNG'),parent=sel,position=meteor.position)
				bullet.run_action(A.sequence(A.move_by(60*cos(2*pi*i/30),60*sin(2*pi*i/30),0.5,TIMING_EASE_OUT),A.move_by(sel.size.h*sin(2*pi*i/30+3),sel.size.h*cos(2*pi*i/30+3),12,TIMING_EASE_OUT),A.remove()))
			meteor.run_action (A.call(shoot_big_bullet,0.01))
			sleep(0.6)

def shoot_bullet_18(sel,meteor):
	sleep(1)
	while 1:
		for j in [2,3,5,7,8,8,8,8,8,8,8,7]:
			play_effect('Sound/se_tan02.mp3')
			for i in range(j):
				bullet = Bullet(SMALL_BULLET,texture=Texture('Bullet/small_bullet_orange.PNG'),parent=sel,position=(meteor.position.x+(-(j-1)/2+i)*12,meteor.position.y))
				bullet.run_action(A.sequence(A.move_by(0,-meteor.position.y-10,2,TIMING_EASE_IN_2),A.move_to(randint(0,int(sel.size.w)),randint(0,int(sel.size.h)),8,TIMING_SINODIAL),A.move_to(randint(0,int(sel.size.w)),randint(0,int(sel.size.h)),8,TIMING_SINODIAL),A.move_to(randint(0,int(sel.size.w)),-10,8,TIMING_EASE_IN),A.remove()))
			sleep(0.05)
		for k in [2,3,4]:
			for l in range(k):
				bullet = Bullet(SMALL_BULLET,texture=Texture('Bullet/small_bullet_green.PNG'),parent=sel,position=(meteor.position.x+(-(k-1)/2+l)*20,meteor.position.y))
				bullet.run_action(A.sequence(A.move_by(0,-meteor.position.y,2,TIMING_EASE_IN_2),A.move_to(randint(0,int(sel.size.w)),randint(0,int(sel.size.h)),8,TIMING_EASE_OUT),A.move_to(randint(0,int(sel.size.w)),randint(0,int(sel.size.h)),8,TIMING_SINODIAL),A.move_to(randint(0,int(sel.size.w)),-10,8,TIMING_EASE_IN),A.remove()))
			sleep(0.05)
		time=sel.t
		while 1:
			if sel.game_part!=8.65:
				return 
			elif sel.game_over==True:
				break
			elif sel.if_bomb==True:
				sleep(4)
				break
			else:
				if sel.t-time>26/sel.speed:
					break
		sleep(2)
