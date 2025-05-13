import numpy as np
import random
import sys

def randPair(s, e):
    # 生成隨機座標對 (x, y)，範圍從 s 到 e-1
    # s: 最小值（包含）
    # e: 最大值（不包含）
    # 返回: 隨機座標元組，例如 (2, 3)
    return np.random.randint(s, e), np.random.randint(s, e)

class BoardPiece:
    def __init__(self, name, code, pos):
        # 初始化網格上的遊戲元素
        # name: 元素名稱（例如 'Player'）
        # code: 在網格上顯示的 ASCII 字符（例如 'P'）
        # pos: 元素位置，2D 元組（例如 (1, 4)）
        self.name = name  # 元素名稱
        self.code = code  # 顯示字符
        self.pos = pos    # 當前位置

class BoardMask:
    def __init__(self, name, mask, code):
        # 初始化網格上的遮罩（用於表示邊界或其他區域）
        # name: 遮罩名稱（例如 'boundary'）
        # mask: 2D numpy 陣列，1 表示遮罩位置，0 表示無遮罩
        # code: 在網格上顯示的 ASCII 字符（例如 '#'）
        self.name = name  # 遮罩名稱
        self.mask = mask  # 遮罩陣列
        self.code = code  # 顯示字符

    def get_positions(self):
        # 返回遮罩中所有標記為 1 的位置
        # 返回: 元組 (x陣列, y陣列)，表示遮罩位置的座標
        return np.nonzero(self.mask)

def zip_positions2d(positions):
    # 將兩個座標陣列 (x, y) 壓縮為座標元組列表
    # positions: 元組，包含兩個陣列 (x陣列, y陣列)
    # 返回: 座標元組列表，例如 [(0,1), (2,3)]
    x, y = positions
    return list(zip(x, y))

class GridBoard:
    def __init__(self, size=4):
        # 初始化網格遊戲板
        # size: 網格尺寸（預設 4x4）
        self.size = size                    # 網格邊長
        self.components = {}                # 字典，儲存遊戲元素（名稱: BoardPiece 對象）
        self.masks = {}                     # 字典，儲存遮罩（名稱: BoardMask 對象）

    def addPiece(self, name, code, pos=(0,0)):
        # 在網格中添加一個遊戲元素
        # name: 元素名稱
        # code: 顯示字符
        # pos: 初始位置（預設 (0,0)）
        newPiece = BoardPiece(name, code, pos)  # 創建新元素
        self.components[name] = newPiece        # 加入元素字典

    def addMask(self, name, mask, code):
        # 在網格中添加一個遮罩（例如邊界）
        # name: 遮罩名稱
        # mask: 2D numpy 陣列，標記遮罩位置
        # code: 顯示字符
        newMask = BoardMask(name, mask, code)  # 創建新遮罩
        self.masks[name] = newMask             # 加入遮罩字典

    def movePiece(self, name, pos):
        # 移動指定元素到新位置，檢查是否被遮罩阻擋
        # name: 元素名稱
        # pos: 目標位置（2D 元組）
        move = True
        for _, mask in self.masks.items():
            # 檢查目標位置是否在任何遮罩中
            if pos in zip_positions2d(mask.get_positions()):
                move = False  # 在遮罩中，禁止移動
        if move:
            self.components[name].pos = pos  # 更新元素位置

    def delPiece(self, name):
        # 刪除指定名稱的遊戲元素
        # name: 元素名稱
        # 注意：程式碼中存在錯誤，應為 self.components[name]
        del self.components['name']  # 錯誤，應改為 del self.components[name]

    def render(self):
        # 渲染網格為 2D 文字陣列，用於顯示
        # 返回: 2D numpy 陣列，包含遊戲元素和遮罩的顯示字符
        dtype = '<U2'  # 字串類型，支援最多 2 個字符
        displ_board = np.zeros((self.size, self.size), dtype=dtype)  # 初始化空網格
        displ_board[:] = ' '  # 填充空白字符
 
        # 添加遊戲元素的顯示字符
        for name, piece in self.components.items():
            displ_board[piece.pos] = piece.code
 
        # 添加遮罩的顯示字符
        for name, mask in self.masks.items():
            displ_board[mask.get_positions()] = mask.code
 
        return displ_board
 
    def render_np(self):
        # 渲染網格為 3D 數值陣列，用於數值處理（例如強化學習）
        # 返回: 3D numpy 陣列，shape (層數, size, size)，每層表示一個元素或遮罩
        num_pieces = len(self.components) + len(self.masks)  # 總層數
        displ_board = np.zeros((num_pieces, self.size, self.size), dtype=np.uint8)  # 初始化 3D 陣列
        layer = 0  # 當前層
 
        # 為每個遊戲元素生成一層
        for name, piece in self.components.items():
            pos = (layer,) + piece.pos  # 層索引 + 元素位置
            displ_board[pos] = 1        # 標記元素位置
            layer += 1
 
        # 為每個遮罩生成一層
        for name, mask in self.masks.items():
            x, y = self.masks['boundary'].get_positions()  # 注意：硬編碼 'boundary'，可能需修正
            z = np.repeat(layer, len(x))                   # 層索引
            a = (z, x, y)                                  # 座標索引
            displ_board[a] = 1                             # 標記遮罩位置
            layer += 1
 
        return displ_board
 
def addTuple(a, b):
    # 將兩個元組座標相加
    # a, b: 2D 元組，例如 (1,2) 和 (0,1)
    # 返回: 新座標元組，例如 (1,3)
    return tuple([sum(x) for x in zip(a, b)])