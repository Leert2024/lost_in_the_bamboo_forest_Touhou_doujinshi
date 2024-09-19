#coding:utf-8
from time import sleep
from random import uniform,randint,choice
import threading
from scene import *
from Touhou_class import Enemy,Boss
from Touhou_shoot_bullet import *

#第一阶段敌机：P妖精(red_sprite)
def part_1_spawn_item(sel):
	sel.enemy_to_destroy=15
	while 1:
		sleep(2)
		if sel.game_part!=1.5:
			return 
		elif sel.game_over==True:
			sleep(2)
		if sel.enemy_spawned<15:
			if len(sel.yukkuri)<=4:#油库里同时存在的最大个数为此处数字-1
				sleep(0.1)
				meteor = Enemy(800,1,3,parent=sel,texture=Texture('Enemy/red_sprite.PNG'))
				meteor.position = (randint(int(sel.size.w*0.3), int(sel.size.w*0.7)),sel.size.h+10)
				threading.Thread(target=shoot_small_bullet,args=[sel,meteor,['Bullet/small_bullet_red.PNG'],7,2]).start()
				meteor.run_action (A.move_to(randint(50,int(sel.size.w-50)),randint(int(sel.size.h-400),int(sel.size.h-100)),randint(3,5),TIMING_EASE_OUT))
					
#第二阶段敌机：大蝴蝶(butterfly)	
def part_2_spawn_item(sel):
	sel.enemy_to_destroy=12
	while 1:
		sleep(0.5)
		if sel.game_part!=2.5:
			return 
		elif sel.enemy_spawned<12:
			if len(sel.yukkuri)<=1:#油库里最大个数为此处数字+1
				meteor = Enemy(1500,1,5,parent=sel,texture=Texture('Enemy/butterfly.PNG'),position = (randint(int(sel.size.w*0.3), int(sel.size.w*0.7)),sel.size.h+10))
				meteor.run_action (A.repeat_forever(A.sequence (A.wait(2.6),A.call(sel.shoot_bullet_3,0.01),A.wait(0.2),A.call(sel.shoot_bullet_3,0.01),A.wait(0.2),A.call(sel.shoot_bullet_3,0.01))))
				meteor.run_action(A.move_by(choice([randint(int(-0.2*sel.size.w),0),randint(0,int(0.2*sel.size.w))]), randint(-400,-100), randint(3,5),TIMING_EASE_OUT))
#第三阶段敌机：点妖精(blue_sprite)	
def part_3_spawn_item(sel):
	sel.enemy_to_destroy=12
	while 1:
		sleep(0.5)
		if sel.enemy_spawned>=12:
			if len(sel.yukkuri)==0:
				sel.game_part=4
				sel.enemy_spawned=0
				return 
		elif sel.enemy_spawned<12 and len(sel.yukkuri)<=3:#油库里最大个数为此处数字+1
			meteor = Enemy(800,0,3,parent=sel,texture=Texture('Enemy/blue_sprite.PNG'),position = (-10,randint(int(sel.size.h-250),int(sel.size.h-100))))
			meteor.run_action (A.repeat_forever(A.sequence (A.wait(3.6),A.call(shoot_big_bullet,0.01),A.wait(0.2),A.call(shoot_big_bullet,0.01),A.wait(0.2),A.call(shoot_big_bullet,0.01))))
			meteor.run_action (A.sequence(A.move_to(sel.size.w+10,randint(int(sel.size.h-300),int(sel.size.h-50)),10),A.remove()))
#生成boss
def spawn_boss(sel,name,name_x,pic,num,card_x):
#boss名称载入	
		sel.boss_name=LabelNode(name,('Futura',16),parent=sel,position = (name_x,sel.size.h-53),z_position=2)
#boss载入
		sel.boss = Boss (name,parent=sel,texture=Texture(pic),position=(sel.size.w/2,sel.size.h+150))
		sel.boss.life_being_charged=True
		#上方变量为True时，无法对boss造成伤害
		sel.life_charged=False
#boss的符卡数量图标载入
		sel.spell_card_number=num
		sel._spell_card_pics (x_position=card_x)
#boss“六角星”图样载入
		sel.boss_ring = SpriteNode('Boss/ring.PNG',parent=sel,z_position=-1,alpha=0.5,position=(sel.size.w/2,sel.size.h+150))
		sel.boss_ring.size*=1.5
		sel.items.append(sel.boss_ring)
	
		sel.boss_ring.run_action (A.repeat_forever(A.rotate_by(-0.5,2)))
		sel.boss_ring.run_action (A.repeat_forever (A.sequence(A.scale_to(1.5,2),A.scale_to(1/1.5,2))))
#boss血条底板载入	
		sel.boss_life = SpriteNode('Boss/boss_life.PNG',parent=sel)
		sel.boss_life.z_position=-0.5
		sel.boss_life.size*=0.17
		sel.boss_life.position=(sel.size.w/2,sel.size.h+150)
		sel.items.append(sel.boss_life)
#boss、“六角星”与血条下移
		for i in [sel.boss,sel.boss_life,sel.boss_ring]:
			i.run_action (A.move_to(sel.size.w/2,sel.size.h-175,3,TIMING_EASE_OUT))
		
def part_4_1_spawn_item(sel):
		sel.time=0
		sel.boss.run_action (A.repeat_forever(A.sequence (A.wait(0.8),A.call(sel.shoot_bullet_4,0.01))))
		sel.boss.run_action (A.repeat_forever(A.sequence(A.wait(1.6),A.call(shoot_big_bullet,0.01),A.wait(0.2),A.call(shoot_big_bullet,0.01),A.wait(0.2),A.call(shoot_big_bullet,0.01))))
		
def part_4_2_spawn_item(sel):
		sel.boss.run_action (A.repeat_forever(A.sequence (A.wait(1.5),A.call(sel.shoot_bullet_5,0.01))))
		sel.boss.run_action (A.repeat_forever(A.sequence(A.move_to(30,sel.boss.position.y,1,TIMING_SINODIAL),A.move_to(sel.size.w-30,sel.boss.position.y,2,TIMING_SINODIAL))))
		threading.Thread (target=shoot_small_bullet,args=[sel,sel.boss,['Bullet/drop_blue.PNG','Bullet/drop_indigo.PNG','Bullet/drop_purple.PNG'],2,0.3]).start()
		
def part_5_spawn_item(sel):
	sel.enemy_to_destroy=30
	while 1:
		sleep(1)#rabbit_yellow的生成机制为：每2秒检测一次已生成敌机个数与屏幕上现存活的敌机数，若符合条件则同时生成2个敌机
		if sel.enemy_spawned>=30:
			if len(sel.yukkuri)==0:
				sel.game_part=6
				sel.enemy_spawned=0
				return
		elif sel.game_over==True:
			sleep(2)
		elif sel.enemy_spawned<30 and len(sel.yukkuri)<=4:
			for i in [-1,1]:
				meteor = Enemy(1200,0,3,parent=sel,texture=Texture('Enemy/rabbit_yellow.PNG'),position=(sel.size.w/2*(1+i)+i*20,randint(int(sel.size.y/2),int(sel.size.y/2+300))))
				meteor.run_action (A.sequence(A.move_by(-i*sel.size.w-i*40,-300,12),A.remove()))
				threading.Thread (target=shoot_bullet_8,args=[sel,meteor,i]).start()
				
def part_6_spawn_item(sel):
	enemy = Enemy (20000,3,1,parent=sel,texture=Texture('Enemy/rabbit_red.PNG'),position=(sel.size.w/2,sel.size.h+50))
	enemy.run_action (A.move_by(0,-300,3))
	threading.Thread (target=shoot_bullet_9,args=[sel,enemy]).start()
	while 1:
		sleep(5)
		if len(sel.yukkuri)==0:
			sel.game_part=7
			sel.enemy_spawned=0
			return 

def part_7_spawn_item(sel):
	sel.enemy_to_destroy=12
	while 1:
		if sel.game_part!=7.5:
			return 
		elif sel.game_over==True:
			sleep(2)
		elif sel.enemy_spawned<sel.enemy_to_destroy:
			if len(sel.yukkuri)<=4:
				enemy = Enemy (5000,2,1,parent=sel,texture=Texture('Enemy/rabbit_green.PNG'),position = (randint(int(sel.size.w*0.3), int(sel.size.w*0.7)),sel.size.h+10))
				enemy.run_action (A.move_by(choice([randint(int(-0.2*sel.size.w),0),randint(0,int(0.2*sel.size.w))]), randint(-400,-100), randint(3,5)))
				threading.Thread (target=shoot_bullet_10,args=[sel,enemy]).start()
		sleep(2)
