#coding:utf-8
#编写者：李睿彤
#项目开始时间:2023年2月3日
#项目主体部分完成时间:2023年5月21日
from Touhou_class import *
from Touhou_enemy_spawn import *
from Touhou_dialogue import *
from Touhou_setup import *

def distance_square(a,b):
	return (a.position.x-b.position.x)**2+(a.position.y-b.position.y)**2

class Game (Scene):
#----游戏初始化
	def setup(self,**kwargs):
		self.WIDTH = self.size.w
		self.HEIGHT = self.size.h
		self.MAX_LENGTH = (self.WIDTH**2+self.HEIGHT**2)**0.5
		self.game_over=True#防止update()在初始化完成前就被调用
#显示音乐停止按钮
		self.music_button = SPR('Menus_and_buttons/music_button.PNG',parent=self,z_position=2,position=(self.size.w-60,self.size.h-25))
		self.music_button.size*=0.08
#显示bomb按钮
		bomb_button= SPR('Menus_and_buttons/bomb_button.PNG',parent=self,z_position=2,alpha=0.5,position=(30,30))
		bomb_button.run_action (A.scale_to(0.5,0))	
#建立自机对象
		self.player = SPR('Player/rimon.PNG',parent=self,anchor_point=(0.5, 0.5))		
		self.player_anchor_point = SpriteNode('Player/anchor_point.PNG',parent=self,anchor_point= (0.51,0.53),z_position=1)
		self.player_anchor_point.run_action (A.repeat_forever(A.rotate_by(-0.01,0)))
		self.player_harmable=HARMABLE
#显示分数及擦弹数
		self.score_label = LabelNode('',('Futura',16),parent=self,position = (self.size.w/1.18, self.size.h - 43),z_position=2)
		self.graze_label = LabelNode('',('Futura',16),parent=self,position = (self.size.w/2, self.size.h - 43),z_position=2)
#显示自机火力
		self.power_label = LabelNode('power:0',('Futura', 16), parent=self,position=(self.size.w/2-35,self.size.h-15),z_position=2,anchor_point=(0,0.5))
#显示player与bomb文字
		self.life_label = LabelNode('''player
bomb''',('Futura', 16), parent=self,position = (25, self.size.h-25),z_position=2)
#显示顶部状态栏
		self.top_bar = SpriteNode('Menus_and_buttons/top_bar.PNG',parent=self,position=(self.size.w/2,self.size.h+53),alpha=0.5,z_position=1)
#建立列表
		self.items = []
		self.lasers = []
		self.yukkuri = []
		self.player_jades = []
		self.bombs = []
#初始化完成，可以开始游戏		
		self.game_over=False
		self.new_game()#开始游戏
#开始新的一局
	def new_game(self):
#游戏进度变量加载
		self.game_part=GAME_PART
		if self.game_part<=4:
			play_effect('Music/night_bird.m4a')
		self.enemy_spawned=0
		self.enemy_destroyed=0
		self.boss_spawned=False
		self.if_bonus=True
		self.if_bomb=False
#残机贴图	
		self.life_pics=[]
		self.life_number=LIFE_NUMBER
		for i in range(self.life_number):
			player_life = SpriteNode('Menus_and_buttons/heart.PNG',parent=self,z_position=2,position=(20*i+58,self.size.h-17))
			self.life_pics.append(player_life)
#bomb贴图
		self.bomb_pics=[]
		self.bomb_number=BOMB_NUMBER
		for i in range(self.bomb_number):
			bomb_pic = SpriteNode('Menus_and_buttons/bomb.PNG',parent=self,z_position=2,position=(20*i+58,self.size.h-36))
			self.bomb_pics.append(bomb_pic)
#建立列表储存物体、油库里
#设定各个变量
		self.speed = SPEED
		self.score = 0
		self.graze = 0
		self.laser_power = LASER_POWER
		self.laser_number = LASER_NUMBER
		self.score_label.text = '''
   score:0'''
		self.graze_label.text = '''
   graze:0'''
		self.power_label.text = 'power:'+str(self.laser_power)
		self.player.position = self.player_anchor_point.position = (self.size.w/2,32)
		self.add_power(self.laser_number)
		self.game_over = False
		self.run_action(A.repeat_forever(A.sequence(A.wait(0.03),A.call(self.shoot_laser))))
		self.run_action(A.repeat_forever(A.sequence(A.wait(0.075),A.call(self.jades_update))))
		self.background_init()
		
	def update(self):#update()每帧调用一次
#在任何状态下均调用的函数
		for i in self.player_jades:
			i.position = self.player.position+i.relative_position
		#print(str(len(self.life_pics))+' '+str(self.life_number))
		#若去除上一句代码前的注释符号，可实时显示一些参数
		if self.game_over==True:
			return
		
#只在game_over=False时调用
		self.prev_graze=int(self.graze/12)
		self.items_update()
		self.check_laser_collisions()
		self.score+=1
		self.score_label.text = '''
   score:'''+str(self.score)
		if int(self.graze/12)>self.prev_graze:
			self.graze_label.text = '''
   graze:'''+str(int(self.graze/12))
			self.graze_()
#只在特定游戏进度下调用
#----part 0～3
		if self.game_part==0:
			self.game_part=0.5
			threading.Thread (target=self.stage_pic,args=['Menus_and_buttons/stage_pic.PNG',self.size.w/3,self.size.h/2.5,-1]).start()
			threading.Thread (target=self.stage_pic,args=['Menus_and_buttons/bgm_1.PNG',self.size.w/3*2,self.size.h/2.5-50,1]).start()
		elif self.game_part==1:
			self.game_part=1.5
			threading.Thread (target=part_1_spawn_item,args=[self]).start()
		elif self.game_part==2:
			self.game_part=2.5
			threading.Thread (target=part_2_spawn_item,args=[self]).start()
		elif self.game_part==3:
			self.game_part=3.5
			threading.Thread (target=part_3_spawn_item,args=[self]).start()
#----part 4
		elif 5>self.game_part>=4:
			if self.game_part==4:
				self.game_part=4.1
				self.collect_all()
			if self.boss_spawned==False:
				self.boss_spawned=True
				spawn_boss(self,'Houraisan Kaguya',68.5,'Enemy/kaguya.PNG',2,150)
			#上述3行操作只会进行一次，用于生成kaguya、boss_life和boss_ring			
				
#----part 4.1					
		if self.game_part==4.1:
			self.game_part=4.11
			self.dialogue_part=-1
			self.run_action (A.sequence(A.wait(3),A.call(dialogue1,0.01)))#此处dialogue_part=-1时调用一次dialogue1()，以建立对象
			#game_part由4.11到4.12的过程由对话结束触发，见touch_began
			
		elif self.game_part==4.12:
			self.game_part=4.15
			self.boss_life_()
			self.boss_life_charge(8000)
			threading.Thread (target=self.stage_pic,args=['Menus_and_buttons/bgm_2.PNG',self.size.w/3*2,self.size.h/2.5-50,1]).start()
			stop_all_effects()
			play_effect('Music/lunatic_princess.m4a')
			self.boss_background_('Background/kaguya_background.PNG')#背景更换为kaguya的背景
			self.t=0#时间设为0，为第一次非符准备
#显示时间标签
			self.time_display=LabelNode ('',('Futura',24),parent=self,z_position=2,anchor_point=(0,0.5),position=(self.size.w/2-30,self.size.h-35))
			part_4_1_spawn_item(self)
		elif self.game_part==4.15:
			if self.t>=30:
				self.boss.remove_all_actions ()
				self.remove_all()
				self.game_part=4.2
			self.time_display.text= str(round(30-self.t,2))
#----part 4.2		
		elif self.game_part==4.2:
			self.game_part=4.25
			self.boss_life_charge(12000)
			self.t=0
			self.spell_card_attack (self.boss,'新难题「木樨清露」')
			part_4_2_spawn_item(self)
			
		elif self.game_part==4.25:
			if self.t>=30:
				self.boss.remove_all_actions ()
				self.spell_card_defeat(False)
				self.remove_all()
				self.game_part=4.3
			self.time_display.text= str(round(30-self.t,2))
			for i in [self.boss_ring,self.boss_life,self.boss_life_full_1,self.boss_life_empty_2,self.boss_life_full_2,self.border_of_life,self.white_ring]:
					i.run_action (A.move_to(self.boss.position.x,self.boss.position.y,0))
#----part 4.3		
		elif self.game_part==4.3:
			self.game_part=4.35
			self.boss_life_charge(8000)
			self.t=0
			threading.Thread (target=shoot_bullet_6,args=[self,self.boss]).start()
			for i in [self.boss,self.boss_ring,self.boss_life,self.boss_life_full_1,self.boss_life_empty_2,self.boss_life_full_2]:
					i.run_action (A.move_to(self.size.w/2,self.size.h-175,3))
				
		elif self.game_part==4.35:
			if self.t>=30:
				self.boss.remove_all_actions ()
				self.remove_all()
				self.game_part=4.4
			self.time_display.text= str(round(30-self.t,2))
#----part 4.4		
		elif self.game_part==4.4:
			self.game_part=4.45
			self.t=0
			self.boss_life_charge(15000)
			self.spell_card_attack (self.boss,'「虚无缥缈蓬莱山」')
			threading.Thread (target=shoot_bullet_7,args=[self,self.boss]).start()
		
		elif self.game_part==4.45:
			if self.t>=30:
				self.boss.remove_all_actions ()
				self.spell_card_defeat(False)
				self.remove_all()
				self.game_part=4.5
			self.time_display.text= str(round(30-self.t,2))
#----part 4.5
		elif self.game_part==4.5:
			self.game_part=4.55
			self.time_display.remove_from_parent()
			self.dialogue_part=-1
			self.run_action (A.sequence(A.wait(3),A.call(dialogue2,0.01)))
			self.collect_all()
#----part 4.6
		elif self.game_part==4.6:
			self.game_part=5
			threading.Thread (target=self.flower,args=[0,(self.size.w/2,self.size.h-175)]).start()
			for i in [self.boss,self.boss_life,self.boss_ring,self.boss_life_full_1,self.boss_life_empty_2,self.boss_life_full_2,self.boss_name]:
				i.remove_from_parent()
			self.boss_spawned=False
			self.boss_background.run_action(A.sequence(A.fade_to(0,1),A.remove()))
			self.background_init()

#----part 5
		elif self.game_part==5:
			self.game_part=5.5
			stop_all_effects()
			play_effect('Music/night_bird.m4a')
			threading.Thread (target=part_5_spawn_item,args=[self]).start()
#----part 6
		elif self.game_part==6:
			self.enemy_destroyed = self.enemy_spawned = 0
			self.game_part=6.5
			threading.Thread (target=part_6_spawn_item,args=[self]).start()
#----part 7
		elif self.game_part==7:		
			self.game_part=7.5
			threading.Thread (target=part_7_spawn_item,args=[self]).start()
#----part 8
		elif self.game_part>=8:
			if self.game_part==8:
				self.game_part=8.1
				self.collect_all()
			if self.boss_spawned==False:
				self.boss_spawned=True
				spawn_boss (self,'Tewi Inaba',42,'Enemy/tewi.PNG',3,95)
			#上述3行操作只会进行一次，用于生成tewi、boss_life和boss_ring	
#----part 8.1		
		if self.game_part==8.1:
			self.game_part=8.11
			self.dialogue_part=-1
			self.run_action (A.sequence(A.wait(3),A.call(dialogue3,0.01)))
		elif self.game_part==8.12:
			self.game_part=8.15
			self.boss_life_()
			self.boss_life_charge(8000)
			threading.Thread (target=self.stage_pic,args=['Menus_and_buttons/bgm_3.PNG',self.size.w/3*2,self.size.h/2.5-50,1]).start()
			stop_all_effects()
			play_effect('Music/white_flag_of_usa_shrine.m4a')
			self.boss_background_('Background/tewi_background.PNG')#背景更换为tewi的背景
			self.t=0#时间设为0，为第一次非符准备
#显示时间标签
			self.time_display=LabelNode ('',('Futura',24),parent=self,z_position=2,anchor_point=(0,0.5),position=(self.size.w/2-30,self.size.h-35))
			threading.Thread (target=shoot_bullet_11,args=[self,self.boss]).start()
		elif self.game_part==8.15:
			if self.t>=30:
				self.boss.remove_all_actions ()
				self.remove_all()
				self.game_part=8.2
			self.time_display.text= str(round(30-self.t,2))
#----part 8.2
		elif self.game_part==8.2:
			self.game_part=8.25
			self.boss_life_charge(20000)
			self.t=0
			self.spell_card_attack (self.boss,'兔符「年糕冲击」')
			threading.Thread (target=shoot_bullet_12,args=[self,self.boss]).start()
			
		elif self.game_part==8.25:
			if self.t>=30:
				self.boss.remove_all_actions ()
				self.spell_card_defeat(False)
				self.remove_all()
				self.game_part=8.3
			self.time_display.text= str(round(30-self.t,2))
		
#----part 8.3
		elif self.game_part==8.3:
			self.game_part=8.35
			self.boss_life_charge(12000)
			self.t=0
			threading.Thread (target=shoot_bullet_14,args=[self,self.boss]).start()		
		elif self.game_part==8.35:
			if self.t>=30:
				self.boss.remove_all_actions ()
				self.remove_all()
				self.game_part=8.4
			self.time_display.text= str(round(30-self.t,2))
			
#----part 8.4
		elif self.game_part==8.4:
			self.game_part=8.45
			self.boss_life_charge(20000)
			self.t=0
			self.spell_card_attack (self.boss,'兔符「兔之跃」')
			threading.Thread (target=shoot_bullet_15,args=[self,self.boss]).start()		
		elif self.game_part==8.45:
			if self.t>=30:
				self.boss.remove_all_actions ()
				self.remove_all()
				self.game_part=8.5
			self.time_display.text= str(round(30-self.t,2))

#----part 8.5
		elif self.game_part==8.5:
			self.game_part=8.55
			self.boss_life_charge(15000)
			self.t=0
			threading.Thread (target=shoot_bullet_17,args=[self,self.boss]).start()		
		elif self.game_part==8.55:
			if self.t>=30:
				self.boss.remove_all_actions ()
				self.remove_all()
				self.game_part=8.6
			self.time_display.text= str(round(30-self.t,2))

#----part 8.6
		elif self.game_part==8.6:
			self.game_part=8.65
			self.boss_life_charge(60000)
			self.t=0
			self.spell_card_attack (self.boss,'兔符「超大型胡萝卜」')
			threading.Thread (target=shoot_bullet_18,args=[self,self.boss]).start()		
			
		elif self.game_part==8.65:
			if self.t>=40:
				self.boss.remove_all_actions ()
				self.remove_all()
				self.game_part=8.7
			self.time_display.text= str(round(40-self.t,2))			
#----part 8.7
		elif self.game_part==8.7:
			self.game_part=8.75
			self.time_display.remove_from_parent()
			self.dialogue_part=-1
			self.run_action (A.sequence(A.wait(3),A.call(dialogue4,0.01)))
			self.collect_all()
#----part 8.8
		elif self.game_part==8.8:
			self.game_part=9
			threading.Thread (target=self.flower,args=[0,(self.size.w/2,self.size.h-175)]).start()
			for i in [self.boss,self.boss_life,self.boss_ring,self.boss_life_full_1,self.boss_life_empty_2,self.boss_life_full_2,self.boss_name]:
				i.remove_from_parent()
			self.boss_spawned=False
			self.game_over=True
			stop_all_effects()
			
#----触控
#bomb按钮
	def touch_began(self,touch):
		if touch.location in self.music_button.frame:
			stop_all_effects()		
		if self.player_harmable==False:
			return 			
		elif touch.location.x<70 and touch.location.y<70:
			if self.bomb_number==0:
				return 
			threading.Thread(target=self.player_bomb).start()
	
	def touch_ended(self,touch):
		if self.game_part==4.11:
			if self.dialogue_part==-1:
				return
			dialogue1(self,0.01)
		elif self.game_part==4.55:
			if self.dialogue_part==-1:
				return
			dialogue2(self,0.01)
		elif self.game_part==8.11:
			if self.dialogue_part==-1:
				return
			dialogue3(self,0.01)
		elif self.game_part==8.75:
			if self.dialogue_part==-1:
				return
			dialogue4(self,0.01)
#触屏滑动时调用函数	
	def touch_moved(self,touch):
		if self.game_over==True or self.if_bomb==True:
			return 
		if self.player.position.y>= (self.size.h*3/4):
			self.collect_all()			
		x = min(max(self.player.position.x+touch.location.x-touch.prev_location.x,0),self.size.w)
		y = min(max(self.player.position.y+touch.location.y-touch.prev_location.y,0),self.size.h-67)
		self.player.position = self.player_anchor_point.position = (x,y)
	
		def scene_pause():
			stop_all_effects()

#----对象更新与碰撞检测
	def items_update(self):#对象状态更新
		#更新玩家碰撞箱位置：
		player_hitbox = Rect(self.player.position.x-0.4,self.player.position.y-0.5,1,1)
		#遍历items列表中的所有对象：
		for item in list(self.items):
			if not item.parent:
				if isinstance(item,Enemy) or isinstance(item,Boss):
					self.yukkuri.remove(item)
				elif isinstance(item,Bomb):
					self.bombs.remove(item)
				self.items.remove(item)
			elif isinstance(item,Bullet):
				if self.if_bomb==True:
					for i in self.bombs:
						if item.frame.intersects(i.frame):
							item.destroy()
				elif distance_square(item,self.player)<=(2+item.r)**2:
					if self.player_harmable==True:
						self.player_hit()#自机miss
						return
				elif distance_square(item,self.player)<=(15+item.r)**2:
					self.graze+=1
			elif isinstance(item,Coin):
				if self.if_bomb==True:
					item.approach()
					continue
				item.collect_detect()
			elif isinstance(item,Enemy) or isinstance(item,Boss):
				if self.player_harmable==True:
					if item.frame.intersects (player_hitbox):
						self.player_hit()#自机miss
						return
			elif isinstance(item,Bomb):
				if item.effect==True:
					item.effect=False
					item.remove_from_parent()
					for j in self.yukkuri:
						if item.frame.intersects(j.frame):
							if isinstance(j,Boss) and j.destroyed==True:
								continue
							j.life-=2000
							if isinstance(j,Boss):
								self.boss_attacked()
							if j.life<=0:
								if not j.parent:
									continue
								if isinstance(j,Enemy):
									self.destroy_meteor (j)
								elif isinstance(j,Boss):
									if self.game_part in [4.25,4.45,8.25,8.45,8.65]:
										self.spell_card_defeat(self.if_bonus)
										if self.if_bonus==True:
											self.bonus(self.game_part)
							
									self.game_part = round(self.game_part+0.05,2)
							#若boss被击破,则game_part增加0.05,以进行下一阶段
									self.boss_life_full_1.run_action(A.rotate_to(-pi,0))
									j.remove_all_actions()
									j.destroyed=True
									self.remove_all()
			elif isinstance(item,Laser):
				item.update()
				if item.hitbox.intersects (player_hitbox):
					if self.player_harmable==True:
						self.player_hit()#自机miss
						return
	
	def check_laser_collisions(self):
		for laser in list(self.lasers):
			if not laser.parent:
				self.lasers.remove(laser)
				continue
			for item in self.yukkuri:
				if laser.position in item.frame:
					if isinstance(item,Boss):
						if item.destroyed==True:
							return 
						if item.life<=0:
							if self.game_part in [4.25,4.45,8.25,8.45,8.65]:
								self.spell_card_defeat(self.if_bonus)
								if self.if_bonus==True:
									self.bonus(self.game_part)
							self.lasers.remove(laser)
							laser.remove_from_parent ()
							self.game_part = round(self.game_part+0.05,2)
							#若boss被击破，则game_part增加0.05，以进行下一阶段
							item.remove_all_actions()
							item.destroyed=True
							#boss的一切发射子弹行为停止
							self.remove_all()
							#消除本次符卡或非符的所有子弹
							self.boss_life_full_1.run_action(A.rotate_to(-pi,0))
							break
						else:
							item.life-=self.laser_power
							self.meteor_attacked (laser)
							self.boss_attacked()
							self.lasers.remove(laser)
							laser.remove_from_parent ()
							break
					if isinstance(item,Enemy):
						if not item.parent:
							continue
						if item.life<=0:
							self.destroy_meteor(item)
							self.lasers.remove(laser)
							laser.remove_from_parent ()
							return 
						else:
							self.meteor_attacked (laser)
							item.life-=self.laser_power
							self.lasers.remove(laser)
							laser.remove_from_parent ()
							break
#----事件			
	def add_power(self,num):
		for i in range(num):
			jade=SPR('Player/rimon_jade.PNG',parent=self)
			self.player_jades.append(jade)
			jade.run_action(A.repeat_forever(A.rotate_by(2,1)))
		for i in range(self.laser_number):
			self.player_jades[i].relative_position = Vector2(30*cos(pi*(-1/2+i/3-(self.laser_number-1)/6)),30*sin(pi*(-1/2+i/3-(self.laser_number-1)/6)))
			self.player_jades[i].position = self.player.position+self.player_jades[i].relative_position
		
	def collect_all(self):
		for i in self.items:
			if isinstance(i,Coin):
				i.approach()
				
	def boss_attacked(self):
		if self.boss.life>self.boss.full_life/2:
			self.boss_life_full_2.run_action (A.rotate_to(-1*(self.boss.full_life/2-self.boss.life)*pi/(self.boss.full_life/2),0))
		elif 0<=self.boss.life<=self.boss.full_life/2:
			self.boss_life_full_2.alpha=0
			self.boss_life_full_1.run_action (A.rotate_to(-1*(self.boss.full_life/2-self.boss.life)*pi/(self.boss.full_life/2),0))

	def meteor_attacked(self,laser):
		for i in range(5):
			particle=SPR (choice(['Effect/under_attack1.png','Effect/under_attack2.png']),parent=self,position= (laser.position+(uniform(-20,20),uniform(-15,-5))))
			#particle.size=particle.size/15
			particle.run_action (A.sequence(A.wait(0.04),A.remove()))
	
	def destroy_meteor(self,meteor):
		if self.game_part not in [3.5,5.5,6.5]:
			if self.enemy_destroyed < self.enemy_to_destroy-1:
				self.enemy_destroyed+=1
			else:
				self.game_part+=0.5
				self.enemy_spawned=0
				self.enemy_destroyed=0
		play_effect ('arcade:Explosion_2',0.2)
		meteor.drop()
		meteor.remove_from_parent()
#击破特效
		for i in range(5):
			m = SpriteNode('Effect/flower.PNG', parent=self)
			m.position = meteor.position + (uniform(-20, 20), uniform(-20, 20))
			angle = uniform(0, pi*2)
			dx, dy = cos(angle) * 20, sin(angle) * 20
			m.run_action(A.move_by(dx, dy, 0.6, TIMING_EASE_OUT))
			m.run_action(A.rotate_by(2*pi,0.8))
			m.run_action(A.fade_to(0,0.8))
	
	def remove_all(self):
		for k in self.items:
				if isinstance(k,Bullet):
					k.destroy()
				elif isinstance(k,Enemy):
					self.destroy_meteor(k)
			
	def player_hit(self):
		self.game_over=True
		self.player_harmable=False
		self.if_bonus=False
		#中弹特效
		self.red_screen = SpriteNode('Effect/red_screen.PNG',parent=self,position=(self.size.w/2,self.size.h/2),alpha=0.2)
		
		hit_ring = SpriteNode('Effect/hit_ring.PNG',parent=self,position=self.player.position,z_position=1)
		hit_ring.size*=0.4
		hit_ring.run_action (A.sequence(A.scale_to(0,1),A.remove()))
		threading.Thread (target=self.flower,args=[1,self.player.position]).start()
		
		for i in self.items:
				i.paused=True
#如果没有残机，则开始新一局
		if self.life_number==0:
			stop_all_effects()	
#清除所有上局留存的对象（玩家与玩家的判定点除外，若有其他不想清除掉的物品，在建立之时不要添加进items列表）
			for item in self.items:
				item.remove_from_parent()
			for i in self.bomb_pics:
				i.remove_from_parent()
			self.run_action (A.sequence(A.wait(3), A.call(self.new_game)))
			return
#残机-1，bomb+2
		self.life_pics[self.life_number-1].remove_from_parent()
		self.life_pics.remove(self.life_pics[self.life_number-1])
		self.life_number-=1
		self.bomb_number+=1
		for i in range(1):
			bomb_pic = SpriteNode('Menus_and_buttons/bomb.PNG',parent=self)
			bomb_pic.z_position=2
			bomb_pic.position = (20*(self.bomb_number+i)+18,self.size.h-36)
			self.bomb_pics.append(bomb_pic)
#播放中弹音效
		play_effect('Sound/player-1.m4a')
		self.run_action (A.sequence(A.wait(1.5), A.call(self.game_over_False)))

	def flower(self,tim,pos):
		sleep(tim)
		for i in range(60):
			m = SpriteNode(choice(['Effect/flower.PNG','Effect/flower_white.png']), parent=self)
			m.position = pos + (uniform(-20, 20), uniform(-20, 20))
			angle = uniform(0, pi*2)
			dx, dy = cos(angle) * 40, sin(angle) * 40
			m.run_action(A.move_by(dx, dy, 0.6, TIMING_EASE_OUT))
			m.run_action (A.rotate_by(2*pi,0.6))
			m.run_action(A.fade_to(0,0.6))
			sleep(0.01)
		return 
	
	def boss_background_(self,pic):
		self.if_moving = False
		for i in self.grounds:
			i.remove_all_actions()
			i.run_action (A.sequence(A.fade_to(0,1),A.remove()))
		self.grounds = []
#boss背景载入
		self.boss_background= SpriteNode(pic,parent=self,z_position=-2,alpha=0,position=(self.size.w/2,self.size.h/2))
		self.boss_background.size*=self.size.x/self.boss_background.size.x
		self.boss_background.run_action (A.fade_to(1,1))
		
	def game_over_False(self):
		for i in self.items:
				i.paused=False
		self.red_screen.remove_from_parent ()
		#玩家移动到屏幕下方
		self.player.run_action (A.move_to(self.size.w/2,32,0))
		self.player_anchor_point.run_action (A.move_to(self.size.w/2,32,0))
		self.remove_all()
		self.game_over=False
		self.run_action (A.sequence(A.wait(2),A.call(self.player_harmable_True)))
		
	def player_harmable_True(self):
		self.player_harmable=True
					
	def boss_destroyed_False(self):
		self.boss.destroyed=False
		
	def stage_pic(self,pic,x,y,direction):
		sleep(2)
		stage_pic = SPR(pic,parent=self,position=(x,y),z_position=2,alpha=0)
		stage_pic.size*=0.2
		stage_pic.run_action (A.sequence(A.move_by(0,direction*50,2),A.wait(4),A.move_by(0,-50*direction,2)))
		stage_pic.run_action (A.sequence(A.fade_to(1,2),A.wait(4),A.fade_to(0,2),A.remove()))
		sleep(6)
		if self.game_part==0.5:
			self.game_part=1
		return	
	
	def graze_(self):
		play_effect('Sound/se_graze.mp3')
		for i in range(5):
			direction=uniform(0,pi)
			graze=SPR('Effect/graze.png',parent=self,position=(self.player.position.x+cos(direction)*5,self.player.position.y+sin(direction)*5))
			#graze.rotation=direction+pi/2
			graze.run_action (A.sequence(A.move_by(cos(direction)*40,sin(direction)*40,0.4),A.remove()))
#----符卡
	def spell_card_attack(self,item,name):
#此函数对任意boss都适用，但在加载立绘时需要判断角色
		#如果boss是kaguya，则显示kaguya立绘
		if self.boss.name=='Houraisan Kaguya':
			spell_card_animation= SpriteNode('Spell_card/kaguya_spell_card.PNG',parent=self,alpha=0,position=(self.size.w+100,self.size.h+100),z_position=1)
		else:
			spell_card_animation= SpriteNode('Spell_card/tewi_spell_card.PNG',parent=self,alpha=0,position=(self.size.w+100,self.size.h+100),z_position=1)
		spell_card_animation.size*=0.35
		spell_card_animation.run_action (A.sequence(A.move_to(self.size.w/3*2,self.size.h/3*2,0.75),A.move_to(self.size.w/3,self.size.h/3,1),A.move_to(-100,-100,0.75)))
		spell_card_animation.run_action (A.sequence(A.fade_to(1,0.75),A.wait(1),A.fade_to(0,0.75),A.remove()))
		#显示“spell card attack!!”文字的动画
		spell_card_text= SpriteNode('Spell_card/spell_card_text.PNG',parent=self,alpha=0,position=(self.size.w/5,self.size.h/5))
		spell_card_text.rotation=0.25*pi
		spell_card_text.size*=1.5
		spell_card_text.run_action (A.move_to(self.size.w/2,self.size.h/2,2.5))
		spell_card_text.run_action (A.sequence(A.fade_to(0.5,0.75),A.wait(1),A.fade_to(0,0.75),A.remove()))
#border of life载入
		self.border_of_life= SpriteNode('Spell_card/border_of_life.PNG',parent=self,alpha=0.5,position=self.boss.position)
		self.border_of_life.size*=0.03
		self.border_of_life.type=31
		self.items.append(self.border_of_life)
		self.border_of_life.run_action(A.repeat_forever(A.rotate_by(-0.3,0.1)))
		self.border_of_life.run_action(A.sequence(A.scale_to(25,0.75),A.wait(0.5),A.scale_to(10,0.75)))
#boss符卡“白色圈”图案载入
		self.white_ring= SpriteNode('Spell_card/white_ring.PNG',parent=self,alpha=0.5,position=self.boss.position)
		self.white_ring.size*=0.055
		self.white_ring.type=31
		self.items.append(self.white_ring)
		self.white_ring.run_action(A.repeat_forever(A.rotate_by(0.5,0.1)))
		self.white_ring.run_action(A.sequence(A.wait(0.2),A.scale_to(10,1.3)))
		
		#显示符卡名称及其动画。
		self.spell_card_name_pic = SpriteNode('Spell_card/spell_card_name.PNG',parent=self,position=(self.size.w-140,-10),z_position=2)
		self.spell_card_name_pic.size*=0.6
		
		self.spell_card_name = LabelNode(name, ('Futara', 13),parent=self)
		self.spell_card_name.position= (self.size.w-60,-10)
		self.spell_card_name.z_position=3
		self.spell_card_name.run_action (A.move_to(self.size.w-60,self.size.h-79,1))
		self.spell_card_name_pic.run_action (A.move_to(self.size.w-140,self.size.h-80,1))
		#符卡图标数量减少1
		self.spell_card_pics [self.spell_card_number-1].run_action(A.remove())
		self.spell_card_number-=1
		#更新if_bonus变量为True
		self.if_bonus=True
			
#boss符卡数量图标显示
	def _spell_card_pics(self,x_position):
		self.spell_card_pics=[]
		for i in range(self.spell_card_number):
			spell_card_pic = SpriteNode('Spell_card/spell_card_pic.PNG',parent=self)
			spell_card_pic.z_position=2
			spell_card_pic.position = (20*i+x_position,self.size.h-55)
			self.spell_card_pics.append(spell_card_pic)
			
	def spell_card_defeat(self,n):
		for i in [self.border_of_life,self.white_ring,self.spell_card_name_pic,self.spell_card_name]:
			i.remove_from_parent()
		if n==False:
			title=SPR('Spell_card/bonus_failed.PNG',parent=self,z_position=2,position=(self.size.w/2,self.size.h/2))
		elif n==True:
			title=SPR('Spell_card/bonus.PNG',parent=self,z_position=2,position=(self.size.w/2,self.size.h/2))
		self.boss.drop()
		title.size*=0.1
		title.run_action (A.sequence(A.scale_to(5,0.5),A.wait(1.5),A.fade_to(0,0.5),A.remove()))
	def bonus(self,part):
		bonus = Coin(BONUS_TYPE[BONUS_PART[part]],parent=self,position=self.boss.position)
		play_effect('Sound/se_cardget.mp3')
#----自机bomb
	def player_bomb(self):
		self.if_bomb=True
		self.player_harmable=False
		self.if_bonus=False
		self.bomb_pics[self.bomb_number-1].remove_from_parent()
		self.bomb_pics.remove (self.bomb_pics[self.bomb_number-1])
		self.bomb_number-=1
		play_effect('game:Bleep')
		for i in range(8):
			a = Bomb(texture=Texture('Player/test.PNG'),parent=self,position=self.player.position)
			a.size*=0.18
			a.run_action (A.repeat(A.rotate_by(-2,1),6))
			a.run_action (A.sequence(A.move_by(120*cos(-pi*(-i+0.1*i)/4),120*sin(-pi*(-i+0.1*i)/4),0.75,TIMING_SINODIAL),A.repeat(A.sequence(A.call(self.bomb_rotate,0.01),A.wait(0.037)),50)))
			if i==7:
				sleep(3.6)
				self.run_action (A.sequence(A.repeat(A.sequence(A.move_to(0,5,0.03),A.move_to(0,-5,0.03),A.move_to(-5,0,0.03),A.move_to(5,0,0.03)),10),A.move_to(0,0,0.03)))
				sleep(0.2)
				self.bomb_approach()
			sleep(0.05)
		self.if_bomb=False
		sleep(2.5)
		self.player_harmable=True
		return 
	#为方便排序,临时定义一个计算敌机与自机间距离的平方的函数distance_to_player_square
	def distance_to_player_square(self,a):
		return distance_square(a,self.player)
		
	def bomb_approach(self):
		present_yukkuri=[]
		if len(self.yukkuri)!=0:
			for j in self.yukkuri:
				present_yukkuri.append(j)
			present_yukkuri.sort(key=self.distance_to_player_square)
			for i in range(8):
				self.bombs[i].run_action (A.sequence(A.move_to(present_yukkuri[(i+1)%len(present_yukkuri)].position.x,present_yukkuri[(i+1)%len(present_yukkuri)].position.y,0.5),A.call(self.bomb_explode,0.01)))
				sleep(0.1)
		else:
			for i in self.bombs:
				i.run_action (A.sequence(A.move_to(self.size.w/2,self.size.h*2/3,0.5),A.call(self.bomb_explode,0.01)))
				sleep(0.1)
		
	def bomb_rotate(self,i,progress):
		cosa=(i.position.x-self.player.position.x)/120
		sina=(i.position.y-self.player.position.y)/120
		cosb=cosa*cos(-0.1)-sina*sin(-0.1)
		sinb=sina*cos(-0.1)+sin(-0.1)*cosa
		i.run_action(A.move_to(self.player.position.x+cosb*120,self.player.position.y+sinb*120,0.075))
	def bomb_explode(self,i,progress):
		i.run_action (A.scale_to(2.5,1,TIMING_EASE_OUT))
		i.run_action (A.sequence(A.fade_to(0,1,TIMING_EASE_OUT),A.call(self.bomb_effect_True,0.01)))
	def bomb_effect_True(self,i,progress):
		i.effect=True
#----boss血条动画
#该函数仅仅在boss生成时被调用（通过A.call)
	def boss_life_(self):
		texture=['Boss/boss_life_full.PNG','Boss/boss_life_empty.PNG','Boss/boss_life_full.PNG',]
		a=0
		self.boss_life_full_1 = SPR(parent=self)
		self.boss_life_empty_2 = SPR(parent=self)
		self.boss_life_full_2 = SPR(parent=self)
		for i in [self.boss_life_full_1,self.boss_life_empty_2,self.boss_life_full_2]:
			i.texture = Texture(texture[a])
			i.z_position=0.1*a-0.4
			i.position=(self.size.w/2,self.size.h-175)
			i.anchor_point = (1,0.5)
			i.size*=0.17
			self.items.append(i)
			a+=1
		self.boss_life_empty_2.rotation=pi
		self.boss_life_full_1.rotation=-pi
		self.boss_life_full_2.alpha=0
		
	def boss_life_charge(self,life):#该函数每次充满boss血条时均需调用
		self.boss_life_full_1.run_action (A.rotate_to(0,1.5))
		self.boss_life_full_2.run_action (A.sequence(A.wait(1.5),A.fade_to(1,0),A.rotate_to(pi,1.5),A.call(self.boss_destroyed_False)))
		self.boss.life = self.boss.full_life = life
#----子弹发射	
	def jades_update(self):
		if self.game_over==True:
			return 
		if len(self.yukkuri)!=0:
			diss=[]
			for item in self.yukkuri:
				diss.append (distance_square(item,self.player))
			MIN_DIS = min(diss)
			aim = self.yukkuri[diss.index(MIN_DIS)]
		for i in self.player_jades:
			laser = SpriteNode('Bullet/player_bullet_aim.PNG', parent=self,anchor_point=(0.5,1),position = i.position,z_position = -1,alpha=0.8)
			self.lasers.append(laser)
			if len(self.yukkuri)!=0:
				try:
					laser.run_action (A.sequence([A.move_by((aim.position.x-i.position.x)/MIN_DIS**0.5*self.MAX_LENGTH,(aim.position.y-i.position.y)/MIN_DIS**0.5*self.MAX_LENGTH,1), A.remove()]))
				except UnboundLocalError:
					continue
				laser.rotation = acos((aim.position.x-self.player.position.x)/MIN_DIS**0.5)-pi/2 if aim.position.y-self.player.position.y>=0 else -acos((aim.position.x-self.player.position.x)/MIN_DIS**0.5)-pi/2
				laser.run_action (A.fade_to(0,0.4))
			else:
				laser.run_action (A.sequence([A.move_by(0,self.size.h,1.2), A.remove()]))
				laser.run_action (A.fade_to(0,0.4))
			
	def shoot_laser(self):
		if self.game_over==True:
			return 
		laser = SpriteNode('Bullet/player_bullet.PNG', parent=self,anchor_point=(0.5,1),position = self.player.position+(0,20),z_position = -1)
		laser.run_action (A.sequence([A.move_by(0,self.size.h,1.2), A.remove()]))
		self.lasers.append(laser)
			
	def shoot_bullet_3(self,meteor,progress):
		if not meteor.parent:
			return 
		play_effect('Sound/shoot_bullet_1.m4a')
		for i in range(20):
			bullet=Bullet (3,parent=self,texture=Texture('Bullet/small_bullet_red.PNG'))
			bullet.position=meteor.position
			actions = [A.move_by(self.size.h*math.cos(i*pi/10),-1*self.size.h*math.sin(i*pi/10),5),A.remove()]
			bullet.run_action (A.sequence(actions))
		
	def shoot_bullet_4(self,meteor,progress):
		if self.game_over==True:
			return 
		play_effect('Sound/se_tan02.mp3')
		for i in range(10):
			self.time+=self.dt
			bullet=Bullet(12,parent=self)
			bullet.texture=Texture('Bullet/big_jade_green.PNG')
			bullet.position=meteor.position
			actions = [A.move_by(self.size.h*math.cos(self.time/2+i*pi/5),-1*self.size.h*math.sin(self.time/2+i*pi/5),6),A.remove()]
			bullet.run_action (A.sequence(actions))
		
	def shoot_bullet_5(self,meteor,progress):
		if self.game_over==True:
			return
		play_effect('Sound/se_tan02.mp3')
		bullet=Bullet(12,parent=self)
		bullet.texture=Texture('Bullet/big_jade_yellow.PNG')
		bullet.position = (uniform(20,self.size.w-20),-20)
		bullet.run_action (A.sequence(A.move_to(uniform(20,self.size.w-20),self.size.h+20,8),A.remove()))
#----背景动画相关
	def background_remove(self,item,progress):
		try:
			self.grounds.remove(item)
		except ValueError:
			pass
	def background_init(self):
		self.grounds = []
		background_grey = SpriteNode('Background/background_grey.PNG',z_position=-8,parent=self,position=(self.size.w/2,self.size.h/2))		
		self.if_moving=True
		self.background_t=6.5
		self.layer=-2
		threading.Thread(target=self.ground).start()
	def ground(self):
		while self.if_moving==True:
			if self.layer!=-8:
				self.layer-=1
			else:
				self.layer = -5
				for i in self.grounds:
					i.z_position+=3
			ground = SpriteNode('Background/IMG_6722.PNG',parent=self,alpha=0,position=(self.size.w/2,575),z_position=self.layer,anchor_point=(0.5,0.9))
			ground.x_scale*=2
			ground.y_scale*=0.1			
			ground.run_action (A.sequence(A.wait(self.background_t/4),A.fade_to(1,1*self.speed,TIMING_EASE_IN_2)))			
			ground.run_action (A.move_to(self.size.w/2,-100,self.background_t*1.25,TIMING_EASE_IN_2))			
			ground.run_action ((A.scale_y_by(0.8,self.background_t,TIMING_LINEAR)))			
			ground.run_action (A.sequence(A.scale_x_by(1.5,self.background_t*1.5,TIMING_EASE_IN_2),A.call(self.background_remove,0.01),A.remove()))			
			self.grounds.append(ground)
			self.bamboo(self.layer+0.5)
			sleep(0.7)
			self.bamboo(self.layer)
			sleep(0.7)
	def bamboo(self,z):
		for i in range(2):
			bamboo = SpriteNode('Background/bamboo.PNG',parent=self,alpha=0,position=(self.size.w/2+choice([randint(-150,-100),randint(100,150)]),500),z_position=z,anchor_point=(0.45,0))
			bamboo.size*=0.5
			if bamboo.position.x<self.size.w/2:
				bamboo.rotation = uniform(pi/12,0)
			else:
				bamboo.rotation = uniform(0,-pi/12)
			bamboo.run_action (A.sequence(A.wait(self.background_t/4),(A.fade_to(1,self.background_t/3,TIMING_LINEAR))))			
			bamboo.run_action (A.move_by((bamboo.position.x-self.size.w/2)*1.5,-1780,1.8*self.background_t,TIMING_EASE_IN_2))			
			bamboo.run_action (A.sequence(A.scale_by(1.8,1.8*self.background_t,TIMING_EASE_IN_2),A.call(self.background_remove,0.01),A.remove()))
			self.grounds.append(bamboo)
			
if __name__ == '__main__':
	run(Game(), PORTRAIT, show_fps=True)
