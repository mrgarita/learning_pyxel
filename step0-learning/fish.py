# -*- coding: utf-8 -*-
import pyxel
import random
from datetime import datetime

direction = True		# True -> False -> True ....
today = datetime.now()  # 現在時刻

class App:
	def __init__(self):
		# 魚
		self.x = 8
		self.y = 8
		self.speed = 1

		# 画面初期化
		width = 64
		height = 64

		pyxel.init(width, height, title="dot_fish", fps=15)
		pyxel.load("cat.pyxres")	# リソースファイルを読み込む

		# 実行
		pyxel.run(self.update, self.draw)

	def update(self):
		global direction, today

		# 現在時刻
		today = datetime.now()
		self.hour = today.hour
		self.minute = today.minute

		# 魚の動き
		if direction == True:
			self.x = self.x + self.speed  # 右に移動
		else:
			self.x = self.x - self.speed  # 左に移動

		if self.x < 0 or self.x >= pyxel.width:  # 端まで行ったら向きを変える
			self.y = random.randint(1, pyxel.height)
			direction = not(direction)

	def draw(self):
		# 画面をクリア
		pyxel.cls(1)

		# 時計の「:」をチカチカさせる
		if pyxel.frame_count % 15 == 0:
			mytime = "{} {}".format(self.hour, self.minute)
		else:
			mytime = "{}:{}".format(self.hour, self.minute)

		pyxel.text(23, 29, mytime, 0)	# 時刻描画

		# 魚表示
		img = 0		# イメージバンク 0~2で指定
		w = 8		# 切り出す幅
		h = 8		# 切り出す高さ
		colkey = 0	# 透明色扱いにする色

		rx = (pyxel.frame_count % 2) * 8 + 8		# イメージバンク切り出し位置のx座標
		ry = 0		# イメージバンク切り出し位置のy座標

		if direction == True:
			pyxel.blt(self.x, self.y, img, rx, ry, -w, h, colkey)		# 右向
		else:
			pyxel.blt(self.x, self.y, img, rx, ry, w, h, colkey)		# 左向

App()
