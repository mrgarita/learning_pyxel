# star_voyager.py
# step0 フェーズ1: ウインドウを出して、黒い画面を表示する

import pyxel

def update():
	"""フレーム毎の更新処理。まだ何もしない"""
	pass

def draw():
	"""フレーム毎の描画処理"""
	pyxel.cls(0)	# 画面全体を色番号0（黒）で塗りつぶす

pyxel.init(160, 120, title="Star Voyager")	# 画面を用意する
pyxel.run(update, draw)				# ゲームループを開始する
