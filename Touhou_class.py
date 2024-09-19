#coding:utf-8
from scene import *
from random import randint,uniform,choice
from sound import play_effect
from math import pi,cos,sin
SPR=SpriteNode
A=Action
COIN_LIST=['Coins/score.PNG','Coins/P.PNG','Coins/big_P.png','Coins/bomb+1.png','Coins/life+1.png']
BONUS_PART={4.25:0,4.45:1,8.25:2,8.45:3,8.65:4}
BONUS_TYPE=[3,4,4,3,3]
#分数点类
class Coin(SPR):
	def __init__(self,type,**kwargs):
		SpriteNode.__init__(self, **kwargs)
		self.to_collect=False
		self.parent.items.append(self)
		self.type=type
		self.texture=Texture(COIN_LIST[type])
		self.run_action (A.sequence(A.move_by(0,10,0.1),A.move_by(0,-1*self.parent.size.h,8),A.remove()))
	def collect_detect(self):
		if self.to_collect==False:
			dis=(self.position.x-self.parent.player.position.x)**2+(self.position.y-self.parent.player.position.y)**2
			if dis<=2500:
				self.approach()
		else:
			return 		
	def approach(self):
		if not self.parent:
			return 
		self.to_collect=True
		self.run_action (A.sequence(A.move_to(self.parent.player.position.x,self.parent.player.position.y,0.2),A.call(self.collect)))
	def collect(self):
		if not self.parent:
			return 
		if self.type==1:
			prev_power=self.parent.laser_power
			self.parent.laser_power+=0.2
			if self.parent.laser_number<=3:
				if self.parent.laser_power//10-prev_power//10==1:
					self.parent.laser_number+=1
					self.parent.add_power(1)
			self.parent.power_label.text ='power:'+str(round(self.parent.laser_power,1))
			#play_effect ('digital:ZapThreeToneUp')
		elif self.type==0:
			#play_effect ('digital:PowerUp7')
			self.parent.score+=1000
		elif self.type==3:
			self.parent.bomb_number+=1
			bomb_pic = SpriteNode('Menus_and_buttons/bomb.PNG',parent=self.parent)
			bomb_pic.z_position=2
			bomb_pic.position = (20*(self.parent.bomb_number+1)+18,self.parent.size.h-36)
			self.parent.bomb_pics.append (bomb_pic)
		elif self.type==2:
			prev_power=self.parent.laser_power
			self.parent.laser_power+=2
			if self.parent.laser_number<=3:
				if self.parent.laser_power//10-prev_power//10==1:
					self.parent.laser_number+=1
					self.parent.add_power(1)
			self.parent.power_label.text ='power:'+str(round(self.parent.laser_power,1))
			#play_effect ('digital:ZapThreeToneUp')
		elif self.type==4:
			self.parent.life_number+=1
			life_pic = SpriteNode('Menus_and_buttons/heart.PNG',parent=self.parent)
			life_pic.z_position=2
			life_pic.position = (20*(self.parent.life_number+1)+18,self.parent.size.h-17)
			self.parent.life_pics.append (life_pic)
		self.remove_from_parent()

class Bullet(SPR):
	def __init__(self,r,**kwargs):
		self.r=r
		SpriteNode.__init__(self,**kwargs)
		self.parent.items.append(self)
	def destroy(self):
		self.remove_all_actions()
		self.run_action (A.fade_to(0,0.3))
		self.run_action (A.sequence(A.scale_to(3,0.3),A.remove()))
		
class Enemy(SPR):
	def __init__(self,life,drop_type,drop_num,**kwargs):
		SpriteNode.__init__(self,**kwargs)
		self.life=life
		self.drop_type=drop_type
		self.drop_num=drop_num
		self.parent.items.append(self)
		self.parent.yukkuri.append(self)
		self.parent.enemy_spawned+=1
	def drop(self):
		for i in range(self.drop_num):
			coin = Coin (self.drop_type,parent=self.parent,position=(uniform(self.position.x-20,self.position.x+20),uniform(self.position.y-20,self.position.y+20)))

class Boss(SPR):
	def __init__(self,name,**kwargs):
		SpriteNode.__init__(self,**kwargs)
		self.name=name
		self.destroyed=True
		self.parent.items.append(self)
		self.parent.yukkuri.append(self)
	def drop(self):
		for i in range(40):
			angle = uniform (0,2*pi)
			dis = randint (15,50)
			coin = Coin (0,parent=self.parent,position=self.position+(cos(angle)*dis,sin(angle)*dis))
		
class Laser(SPR):
	def __init__(self,**kwargs):
		SpriteNode.__init__(self,**kwargs)
		self.parent.items.append(self)
	def update(self):
		self.hitbox = Rect(self.position.x-self.size.w/2,self.position.y-4,self.size.w,8)
		
class Bomb(SPR):
	def __init__(self,**kwargs):
		SpriteNode.__init__(self,**kwargs)
		self.effect=False
		#将bomb对象添加入items和bombs两个列表
		self.parent.items.append(self)
		self.parent.bombs.append(self)
