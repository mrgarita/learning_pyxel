# sokoban.py
# step2 フェーズ2：主人公を矢印キーで動かす

import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
TILE = 8                # 1 マスの大きさ（ドット）
HUD_HEIGHT = 12         # 画面の上、手数などを出すために空けておく高さ

# イメージバンク 0 の、切り出し位置
V_TILE = 0              # タイルの段
V_PLAYER = 8            # 主人公の段（コマ A）
U_FLOOR =0
U_WALL = 8
U_GOAL = 16
U_BOX = 24

# 向き。この番号がそのまま主人公の絵の切り出し位置になる
DIR_DOWN = 0
DIR_UP = 1
DIR_LEFT = 2
DIR_RIGHT = 3

# 向きごとの、1 歩ぶんのずれ（x のずれ, y のずれ）
MOVES = [
    (0, 1),         # 下
    (0, -1),        # 上
    (-1, 0),        # 左
    (1, 0),         # 右
]

# ステージの地図
# # 壁  . 床  O ゴール  $ 荷物  @ 主人公
STAGE1 = [
    "########",
    "#......#",
    "#..O...#",
    "#..$...#",
    "#..@...#",
    "########",
]

class App:
    def __init__(self):
        """起動時の設定"""
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Sokoban")
        pyxel.load("sokoban.pyxres")
        self.load_stage(STAGE1)
        pyxel.run(self.update, self.draw)

    def load_stage(self, rows):
        """文字の地図を読んで、壁・主人公・荷物に分ける"""
        self.tiles = []
        self.boxes = []
        self.player_dir = DIR_DOWN  # はじめは下を向いている

        for y in range(len(rows)):
            line = []
            for x in range(len(rows[y])):
                mark = rows[y][x]
                if mark == "@":
                    self.player_x = x
                    self.player_y = y
                    mark = "."      # 主人公の足元は床
                elif mark == "$":
                    self.boxes.append([x, y])
                    mark = "."      # 荷物の下も床
                line.append(mark)
            self.tiles.append(line)

        # 盤面を画面の中央に置くための、ずらし幅
        board_w = len(self.tiles[0]) * TILE
        board_h = len(self.tiles) * TILE
        self.ox = (SCREEN_WIDTH - board_w) // 2
        self.oy = HUD_HEIGHT + (SCREEN_HEIGHT - HUD_HEIGHT - board_h) // 2

    def update(self):
        """フレーム毎の更新処理"""
        self.handle_key()

    def handle_key(self):
        """矢印キーを見て、押された向きへ 1 歩進もうとする"""
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.try_move(DIR_DOWN)
        elif pyxel.btnp(pyxel.KEY_UP):
            self.try_move(DIR_UP)
        elif pyxel.btnp(pyxel.KEY_LEFT):
            self.try_move(DIR_LEFT)
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.try_move(DIR_RIGHT)

    def try_move(self, direction):
        """その向きへ動けるか調べて、動けるときだけ 1 マス進む"""
        self.player_dir = direction     # 動けなくても、向きだけは変える

        dx, dy = MOVES[direction]
        next_x = self.player_x + dx
        next_y = self.player_y + dy

        if self.tiles[next_y][next_x] == "#":   # 行き先が壁なら
            return                              # 何もしないで戻る

        self.player_x = next_x
        self.player_y = next_y

    def draw(self):
        """描画処理"""
        pyxel.cls(pyxel.COLOR_BLACK)

        # 壁を、上の行から 1 マスずつ描く
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                mark = self.tiles[y][x]
                if mark == "#":
                    u = U_WALL
                elif mark == "O":
                    u = U_GOAL
                else:
                    u = U_FLOOR
                pyxel.blt(self.ox + x * TILE, self.oy + y * TILE,
                            0, u, V_TILE, TILE, TILE)

        # 荷物
        for box in self.boxes:
            pyxel.blt(self.ox + box[0] * TILE, self.oy + box[1] * TILE,
                        0, U_BOX, V_TILE, TILE, TILE, pyxel.COLOR_BLACK)

        # 主人公
        pyxel.blt(self.ox + self.player_x * TILE, self.oy + self.player_y *TILE,
                    0, self.player_dir * TILE, V_PLAYER, TILE, TILE, pyxel.COLOR_BLACK)

App()
