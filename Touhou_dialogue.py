#coding:utf-8
from scene import *
A=Action
def start(sel):
	sel.game_over=True
	sel.player_harmable=False
	sel.player.position = sel.player_anchor_point.position=(sel.size.w/2,32)
	sel.dialogue_bar = SpriteNode('Dialogue/dialogue_bar.PNG',parent=sel,z_position=2,position=(sel.size.w/2,-300),alpha=0.7)
	sel.dialogue_bar.size*= sel.size.w/sel.dialogue_bar.size.w
def end(sel):
	for i in [sel.dialogue_bar,sel.dialogue_kaguya,sel.dialogue_rimon,sel.dialogue_text]:
		i.run_action (A.sequence(A.move_by(0,-400,1),A.remove()))
		sel.game_over=False
		sel.player_harmable=True

def dialogue1(sel,progress):
		sel.dialogue_part+=1	
		if sel.dialogue_part==0:
			start(sel)
			sel.dialogue_kaguya =SpriteNode('Dialogue/kaguya_puzzled.PNG',parent=sel,z_position=1.5,position=(sel.size.w/2+130,-250),x_scale=-1)
			sel.dialogue_kaguya.size*=0.35
			
			sel.dialogue_rimon =SpriteNode('Dialogue/rimon_normal_dark.PNG',parent=sel,z_position=1.5,position=(sel.size.w/2-130,-250))
			sel.dialogue_rimon.size*=0.35
			
			sel.dialogue_text=LabelNode('是灵梦小姐呢，您是在竹林中迷路了吗？',('Futura',16),parent=sel,z_position=3,anchor_point=(0,1),position=(sel.size.w/2-160,-260))
			 
			for i in [sel.dialogue_bar,sel.dialogue_kaguya,sel.dialogue_rimon,sel.dialogue_text]:
				i.run_action(A.move_by(0,400,1))
				
		elif sel.dialogue_part==1:			
			sel.dialogue_kaguya.texture = Texture('Dialogue/kaguya_puzzled_dark.PNG')
			sel.dialogue_kaguya.size*=0.35
			sel.dialogue_rimon.texture = Texture('Dialogue/rimon_normal.PNG')
			sel.dialogue_rimon.size*=0.35
			sel.dialogue_text.text='是的啊，我该怎么走出竹林呢……'
			
		elif sel.dialogue_part==2:
			sel.dialogue_text.text='''不过，辉夜小姐为什么离开永远亭来到了竹林
里呢？'''
			
		elif sel.dialogue_part==3:			
			sel.dialogue_kaguya.texture = Texture('Dialogue/kaguya_normal.PNG')
			sel.dialogue_kaguya.size*=0.35	
			sel.dialogue_rimon.texture = Texture('Dialogue/rimon_normal_dark.PNG')
			sel.dialogue_rimon.size*=0.35
			sel.dialogue_text.text='帝不知道跑到哪里去了，我去寻找一下。'
		
		elif sel.dialogue_part==4:
			sel.dialogue_text.text='''据说，碰见因幡帝的人能利用其赋予的幸运走
出竹林哦，灵梦小姐不妨与我一同去寻找呢……'''

		elif sel.dialogue_part==5:			
			sel.dialogue_kaguya.texture = Texture('Dialogue/kaguya_normal_dark.PNG')
			sel.dialogue_kaguya.size*=0.35	
			sel.dialogue_rimon.texture = Texture('Dialogue/rimon_normal.PNG')
			sel.dialogue_rimon.size*=0.35
			sel.dialogue_text.text='好啊，不过要先在弹幕游戏中取胜哦！'
			
		elif sel.dialogue_part==6:			
			sel.dialogue_kaguya.texture = Texture('Dialogue/kaguya_laugh.PNG')
			sel.dialogue_kaguya.size*=0.35
			
			sel.dialogue_rimon.texture = Texture('Dialogue/rimon_normal_dark.PNG')
			sel.dialogue_rimon.size*=0.35
			sel.dialogue_text.text='嗯……行的呢。'
		
		elif sel.dialogue_part==7:
			end(sel)
			sel.game_part=4.12
		
def dialogue2(sel,progress):
	sel.dialogue_part+=1		
	if sel.dialogue_part==0:
		start(sel)		
		sel.dialogue_kaguya =SpriteNode('Dialogue/kaguya_defeated.PNG',parent=sel,z_position=1.5,position=(sel.size.w/2+130,-250))
		sel.dialogue_kaguya.size*=0.35
			
		sel.dialogue_rimon =SpriteNode('Dialogue/rimon_smile_dark.PNG',parent=sel,z_position=1.5,position=(sel.size.w/2-130,-250))
		sel.dialogue_rimon.size*=0.35
			
		sel.dialogue_text=LabelNode('呜呜呜……',('Futura',16),parent=sel,z_position=3,anchor_point=(0,1),position=(sel.size.w/2-160,-260))
			 
		for i in [sel.dialogue_bar,sel.dialogue_kaguya,sel.dialogue_rimon,sel.dialogue_text]:
			i.run_action (A.move_by(0,400,1))				
	elif sel.dialogue_part==1:
		sel.dialogue_text.text='对不起啊，打得太狠了呢……'
			
		sel.dialogue_kaguya.texture = Texture('Dialogue/kaguya_defeated_dark.PNG')
		sel.dialogue_kaguya.size*=0.35
			
		sel.dialogue_rimon.texture = Texture('Dialogue/rimon_smile.PNG')
		sel.dialogue_rimon.size*=0.35
	elif sel.dialogue_part==2:
		sel.dialogue_text.text='不过寻找帝的事，我是可以去帮忙的哦。'
	elif sel.dialogue_part==3:
		end(sel)
		sel.game_part=4.6

def dialogue3(sel,progress):
		sel.dialogue_part+=1		
		if sel.dialogue_part==0:
			start(sel)
			sel.dialogue_kaguya = SpriteNode ('Dialogue/tewi_normal_dark.PNG',parent=sel,z_position=1.5,position=(sel.size.w/2+130,-250),x_scale=-1)
			sel.dialogue_kaguya.size*=0.35	
			sel.dialogue_rimon = SpriteNode('Dialogue/rimon_normal.PNG',parent=sel,z_position=1.5,position=(sel.size.w/2-130,-250))
			sel.dialogue_rimon.size*=0.35			
			sel.dialogue_text=LabelNode('这不是妖怪兔嘛，怎么跑到这里来了？',('Futura',16),parent=sel,z_position=3,anchor_point=(0,1),position=(sel.size.w/2-160,-260))
			 
			for i in [sel.dialogue_bar,sel.dialogue_kaguya,sel.dialogue_rimon,sel.dialogue_text]:
				i.run_action(A.move_by(0,400,1))
				
		elif sel.dialogue_part==1:			
			sel.dialogue_kaguya.texture = Texture('Dialogue/tewi_normal.PNG')
			sel.dialogue_kaguya.size*=0.35	
			sel.dialogue_rimon.texture = Texture ('Dialogue/rimon_normal_dark.PNG')
			sel.dialogue_rimon.size*=0.35
			sel.dialogue_text.text='''是博丽的巫女啊，我准备去夜雀食堂吃点烤八
目鳗哦！您有什么事吗？'''
			
		elif sel.dialogue_part==2:
			sel.dialogue_kaguya.texture= Texture('Dialogue/tewi_normal_dark.PNG')
			sel.dialogue_kaguya.size*=0.35	
			sel.dialogue_rimon.texture=Texture('Dialogue/rimon_normal.PNG')
			sel.dialogue_rimon.size*=0.35
			sel.dialogue_text.text='辉夜小姐在寻找你呢，她或许不久就会跟上来。'
			
		elif sel.dialogue_part==3:			
			sel.dialogue_kaguya.texture = Texture('Dialogue/tewi_laugh.PNG')
			sel.dialogue_kaguya.size*=0.35	
			sel.dialogue_rimon.texture = Texture('Dialogue/rimon_normal_dark.PNG')
			sel.dialogue_rimon.size*=0.35
			sel.dialogue_text.text='公主出门去走动，真是难得的事情呢（笑）。'
		
		elif sel.dialogue_part==4:
			sel.dialogue_kaguya.texture = Texture ('Dialogue/tewi_laugh_dark.PNG')
			sel.dialogue_kaguya.size*=0.35	
			sel.dialogue_rimon.texture = Texture ('Dialogue/rimon_normal.PNG')
			sel.dialogue_rimon.size*=0.35
			sel.dialogue_text.text='''对了，我不小心在这个竹林里迷路了，听说
遇见你的话，可以变得幸运从而走出竹林？'''

		elif sel.dialogue_part==5:			
			sel.dialogue_kaguya.texture = Texture('Dialogue/tewi_laugh.PNG')
			sel.dialogue_kaguya.size*=0.35
			
			sel.dialogue_rimon.texture = Texture('Dialogue/rimon_normal_dark.PNG')
			sel.dialogue_rimon.size*=0.35
			sel.dialogue_text.text='的确如此，但是要在弹幕游戏中取胜哦！'
			
		elif sel.dialogue_part==6:			
			sel.dialogue_kaguya.texture = Texture('Dialogue/tewi_laugh_dark.PNG')
			sel.dialogue_kaguya.size*=0.35	
			sel.dialogue_rimon.texture = Texture('Dialogue/rimon_normal.PNG')
			sel.dialogue_rimon.size*=0.35
			sel.dialogue_text.text='奉陪到底！'
		
		elif sel.dialogue_part==7:
			end(sel)
			sel.game_part=8.12
			
def dialogue4(sel,progress):
	sel.dialogue_part+=1
	if sel.dialogue_part==0:
		start(sel)
		sel.dialogue_kaguya =SpriteNode('Dialogue/tewi_defeated.PNG',parent=sel,z_position=1.5,position=(sel.size.w/2+130,-250))
		sel.dialogue_kaguya.size*=0.35
			
		sel.dialogue_rimon =SpriteNode('Dialogue/rimon_smile_dark.PNG',parent=sel,z_position=1.5,position=(sel.size.w/2-130,-250))
		sel.dialogue_rimon.size*=0.35
			
		sel.dialogue_text=LabelNode('呜……投降投降!',('Futura',16),parent=sel,z_position=3,anchor_point=(0,1),position=(sel.size.w/2-160,-260))
			 
		for i in [sel.dialogue_bar,sel.dialogue_kaguya,sel.dialogue_rimon,sel.dialogue_text]:
			i.run_action (A.move_by(0,400,1))				
	elif sel.dialogue_part==1:
		sel.dialogue_text.text='往那里走，就能走出去的!'
			
	elif sel.dialogue_part==2:
		sel.dialogue_text.text='很感谢哦!希望能快点走出去呢……'
		sel.dialogue_kaguya.texture = Texture('Dialogue/tewi_defeated_dark.PNG')
		sel.dialogue_kaguya.size*=0.35
			
		sel.dialogue_rimon.texture = Texture('Dialogue/rimon_smile.PNG')
		sel.dialogue_rimon.size*=0.35
	elif sel.dialogue_part==3:
		end(sel)
		sel.game_part=8.8
