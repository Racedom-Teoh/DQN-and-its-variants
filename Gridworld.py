from GridBoard import *

class Gridworld:
    def __init__(self, size=4, mode='static'):
        # 初始化網格世界，設置網格大小和模式
        # size: 網格邊長（預設 4x4）
        # mode: 初始化模式（'static'、'player' 或隨機）
        if size >= 4:
            self.board = GridBoard(size=size)  # 創建指定大小的網格
        else:
            print("Minimum board size is 4. Initialized to size 4.")
            self.board = GridBoard(size=4)  # 強制設為 4x4

        # 添加遊戲元素（玩家、終點、陷阱、牆）及其初始位置（稍後更新）
        self.board.addPiece('Player', 'P', (0,0))
        self.board.addPiece('Goal', '+', (1,0))
        self.board.addPiece('Pit', '-', (2,0))
        self.board.addPiece('Wall', 'W', (3,0))

        # 根據模式初始化網格
        if mode == 'static':
            self.initGridStatic()  # 靜態初始化
        elif mode == 'player':
            self.initGridPlayer()  # 玩家隨機位置
        else:
            self.initGridRand()  # 全隨機初始化

    def initGridStatic(self):
        # 初始化靜態網格，所有元素位置固定
        # 玩家 (0,3)、終點 (0,0)、陷阱 (0,1)、牆 (1,1)
        self.board.components['Player'].pos = (0,3)  # 玩家位置
        self.board.components['Goal'].pos = (0,0)    # 終點位置
        self.board.components['Pit'].pos = (0,1)     # 陷阱位置
        self.board.components['Wall'].pos = (1,1)    # 牆位置

    def validateBoard(self):
        # 驗證網格是否有效（無重疊元素且可解）
        valid = True

        # 獲取所有元素
        player = self.board.components['Player']
        goal = self.board.components['Goal']
        wall = self.board.components['Wall']
        pit = self.board.components['Pit']

        # 檢查是否有元素位置重疊
        all_positions = [player.pos, goal.pos, wall.pos, pit.pos]
        if len(all_positions) > len(set(all_positions)):
            return False  # 重疊則無效

        # 檢查角落位置（玩家或終點在角落是否可移動）
        corners = [(0,0), (0,self.board.size), (self.board.size,0), (self.board.size,self.board.size)]
        if player.pos in corners or goal.pos in corners:
            # 檢查玩家和終點周圍是否有可移動空間
            val_move_pl = [self.validateMove('Player', addpos) for addpos in [(0,1),(1,0),(-1,0),(0,-1)]]
            val_move_go = [self.validateMove('Goal', addpos) for addpos in [(0,1),(1,0),(-1,0),(0,-1)]]
            if 0 not in val_move_pl or 0 not in val_move_go:
                valid = False  # 無可移動空間則無效

        return valid

    def initGridPlayer(self):
        # 初始化網格，玩家位置隨機，其餘元素靜態
        self.initGridStatic()  # 先設置靜態元素
        self.board.components['Player'].pos = randPair(0, self.board.size)  # 隨機設置玩家位置

        # 驗證網格，若無效則重新初始化
        if not self.validateBoard():
            self.initGridPlayer()

    def initGridRand(self):
        # 初始化網格，所有元素位置隨機
        self.board.components['Player'].pos = randPair(0, self.board.size)  # 玩家隨機位置
        self.board.components['Goal'].pos = randPair(0, self.board.size)   # 終點隨機位置
        self.board.components['Pit'].pos = randPair(0, self.board.size)    # 陷阱隨機位置
        self.board.components['Wall'].pos = randPair(0, self.board.size)   # 牆隨機位置

        # 驗證網格，若無效則重新初始化
        if not self.validateBoard():
            self.initGridRand()

    def validateMove(self, piece, addpos=(0,0)):
        # 驗證指定元素的移動是否有效
        # piece: 移動的元素（通常為 'Player'）
        # addpos: 移動的偏移量（例如 (0,1) 表示右移）
        # 返回值：0（有效）、1（無效，撞牆或出界）、2（掉入陷阱）
        outcome = 0
        pit = self.board.components['Pit'].pos
        wall = self.board.components['Wall'].pos
        new_pos = addTuple(self.board.components[piece].pos, addpos)  # 計算新位置

        if new_pos == wall:
            outcome = 1  # 撞牆，無效
        elif max(new_pos) > (self.board.size-1):  # 超出上/右邊界
            outcome = 1
        elif min(new_pos) < 0:  # 超出下/左邊界
            outcome = 1
        elif new_pos == pit:
            outcome = 2  # 掉入陷阱

        return outcome

    def makeMove(self, action):
        # 根據動作執行玩家移動
        # action: 動作（'u' 上、'd' 下、'l' 左、'r' 右）
        def checkMove(addpos):
            # 檢查移動是否有效或掉入陷阱，若是則更新玩家位置
            if self.validateMove('Player', addpos) in [0,2]:
                new_pos = addTuple(self.board.components['Player'].pos, addpos)
                self.board.movePiece('Player', new_pos)

        # 根據動作選擇移動方向
        if action == 'u':  # 上
            checkMove((-1,0))
        elif action == 'd':  # 下
            checkMove((1,0))
        elif action == 'l':  # 左
            checkMove((0,-1))
        elif action == 'r':  # 右
            checkMove((0,1))
        else:
            pass  # 無效動作，跳過

    def reward(self):
        # 計算當前狀態的獎勵
        # 到達終點：+10，掉入陷阱：-10，其他：-1（鼓勵快速到達終點）
        if self.board.components['Player'].pos == self.board.components['Pit'].pos:
            return -10
        elif self.board.components['Player'].pos == self.board.components['Goal'].pos:
            return 10
        else:
            return -1

    def display(self):
        # 返回網格的可視化表示（文字形式）
        return self.board.render()