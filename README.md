# 说明文档
开发者：Leert2024
开发者说：“本程序仅适用于pythonista，难以脱离开发环境运行！”

## 基础思路
1.本游戏使用名为 **self.game_part** 的旗变量进行游戏进度的更新标识。常用的结构（例）：

	def update(self):
		if self.game_part==1:
			#一次性操作
			self.game_part=2
		if self.game_part==2:
			#操作

2.游戏中，敌机的生成与子弹的发射由多线程进行控制。

## 游戏规则与一些常量的记录
1.各种子弹的判定半径：
	(子弹贴图的名称包含子弹类型与颜色两部分，由贴图名称可知晓子弹类型)
	具体值见Touhou_shoot_bullet.py
2.各种对象的z_position属性：
	z_position为2的有：
		各类按钮、文字
3.Enemy类的drop_type属性：
	drop_type为0时，生成分数点（蓝点）。
	drop_type为1时，生成P点。
	drop_type为2时，生成大P点。
	drop_type为3时，生成bomb道具。
	drop_type为4时，生成残机道具。

## 一些函数与变量的说明
1.move_by()和move_to()的部分参数：
TIME_EASE_IN为加速；
TIME_EASE_OUT为减速；
TIME_EASE_IN_OUT为先加速后减速。

2.Game类的game_over属性用于控制游戏的更新。

3.self.player的harmable属性用于决定玩家是否处于无敌状态，若为False则玩家处于无敌状态。

4.Game类的laser_number属性，为0时玩家没有子机，为1时有1个子机，以此类推。

5.Game类的if_bonus属性用于判定击破符卡能否获得奖励，游戏初始化时为True，若player_hit函数被调用，则变为Flase。每次新符卡开始时会更新if_bonus为True。符卡若到时间自动结束，则不论if_bonus为True或False都无法获得奖励。
