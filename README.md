# DQN-and-its-variants

---

# HW 4.1
## Naive DQN 在 Static 與 Random 模式下的表現分析報告

### 實驗目標

* 比較 Naive DQN 在 Static 模式與 Random 模式下的學習表現差異。
* 檢驗加入 **Experience Replay Buffer** 與 **Target Network** 等改良機制對 DQN 訓練穩定性與效果的影響。
* 分析兩種模式下性能差異的原因，探討改良後性能提升的機制與原因。

### 實作內容說明

Naive DQN 基於深度 Q 學習，在每個時間步使用神經網絡估計各動作的 Q 值，並以 ε-greedy 策略選擇動作，之後根據經典 Q 學習 (Bellman Equation) 更新網絡參數。下列為對 Naive DQN 的改良版本描述：

* **Naive DQN（基礎版）**：直接將觀測到的狀態作為網絡輸入，輸出對應動作的 Q 值，並在每一步使用最新的網絡輸出計算訓練目標。此版本無額外機制，容易受到連續樣本相關性與目標值變動的影響。
* **加入經驗回放 (Experience Replay Buffer)**：將 agent 產生的 (狀態, 動作, 獎勵, 下個狀態) 序列存入緩衝區，訓練時隨機抽取批次 (minibatch) 進行更新。經驗回放使得訓練樣本「隨機化」，消除了連續樣本之間的相關性，從而平滑數據分佈並穩定訓練過程。正如文獻所述，隨機抽樣有助於去相關化，顯著提升 DQN 訓練的穩定度和收斂性。
* **加入目標網絡 (Target Network)**：建立一個與主網絡結構相同但參數延遲更新的副網絡，僅在每隔固定步數才將主網絡的權重複製過來。目標網絡用於計算 Q-learning 的目標值，這樣訓練時目標不會隨主網絡權重立即變化，避免強烈的自我反饋循環。目標網絡可產生更穩定的目標 Q 值，降低訓練中的震盪，從而提高收斂性。

### 實驗結果比較

Naive DQN 在 **Static 模式**和 **Player 模式**下的學習曲線與最終表現如圖所示。在 Static 模式中，初始狀態固定，原始 Naive DQN 可穩定地學到一定策略，隨著訓練逐漸收斂，累積獎勵逐步提升，表現尚可接受。

  **Naive DQN in Static mode**

  ![image](https://github.com/user-attachments/assets/8ab52a2b-edfd-45ae-b9dc-fd84812e106d) 

  **Naive DQN in Player mode**

  ![image](https://github.com/user-attachments/assets/3c177642-c9cb-4122-a006-ad1ae780837c) 


相較之下，在 **Random 模式**（每次 episode 初始狀態隨機）中，原始 Naive DQN 的訓練表現明顯較差。由於環境條件每次變化，訓練時的狀態分佈更加多樣，原始 DQN 容易陷入震盪，學習曲線波動大且最終平均獎勵低下，無法穩定找到最佳策略。
  
  **Naive DQN in Random mode**
  
  ![image](https://github.com/user-attachments/assets/50be9bb5-744e-4472-b19c-de1eb24b6201)


將 **經驗回放** 機制加入 Naive DQN 後，在 Random 模式下的學習效果有所改善。由於訓練時使用了多樣化的歷史樣本，樣本間相關性降低，使訓練曲線更加平滑，最終策略也更佳。經驗回放的應用令累積獎勵比原始版本提高，學習過程更加穩定。

  **Naive DQN + 經驗回放** 
  
  ![image](https://github.com/user-attachments/assets/e16a4ce7-3666-4255-ba0d-2abaa7cd6b31)


進一步加入 **目標網絡** 後，Random 模式下 DQN 的表現進一步提升。目標網絡的週期性更新使得訓練目標更穩定，訓練過程中 Q 值估計變化較小，收斂過程更加平緩，最終性能顯著優於僅用經驗回放的情況，並接近 Static 模式的水平。

**Naive DQN + 經驗回放 + 目標網絡**

![image](https://github.com/user-attachments/assets/cde8e4e9-a858-4132-a344-734090623cf0)

最後加入防止撞墻機制後最終結果收斂得非常好。

**Naive DQN + 經驗回放 + 目標網絡 + 防撞墻機制**

![image](https://github.com/user-attachments/assets/1ce2b0a4-6416-4930-893e-6cb37d6bc97c)


### 結果分析與推測原因

Naive DQN 在 Random 模式下表現不佳，主要原因可歸結為環境變化加劇了學習的困難度。強化學習演算法通常假設環境是平穩的，若環境每次初始條件不同，相當於增加了非平穩性，這使得無改良的 DQN 訓練過程震盪加劇且難以收斂。具體來說，不使用經驗回放時，訓練過程中樣本間的相關性很強，神經網絡容易過度擬合到連續走過的狀態序列，容易陷入局部最優，從而導致學習不穩定。此外，若未使用目標網絡，每一步更新同時影響當前和下一步的 Q 值估計，訓練目標會隨網絡參數即時改變，形成劇烈的反饋循環，使得 Q 值估計震盪，收斂困難。

透過加入經驗回放和目標網絡，上述問題得到有效緩解。經驗回放機制使得訓練時從歷史緩衝區隨機取樣，增強了訓練樣本的多樣性，降低了批次更新之間的相關性，這對於穩定訓練非常關鍵。目標網絡則將 Q 值目標的計算從當前網絡參數中隔離出來，使目標值在多次更新間保持相對固定，大幅度減少了估計中的抖動。這兩種改良共同提升了 DQN 在隨機環境下的學習穩定度和最終表現。

### 小結

本報告實驗結果顯示，Naive DQN 在靜態（Static）環境下可以學習到一定程度的策略，但面對隨機（Random）環境時表現不佳。引入經驗回放緩衝區和目標網絡後，DQN 的訓練穩定性顯著提高，在隨機環境中的性能也大幅提升。經驗回放提供了更多樣化的訓練樣本並去除了連續樣本間的相關性，目標網絡則通過固定目標值大幅降低了估計的震盪。這些技術是深度強化學習成功應用的關鍵因素。實驗過程中，我們深刻體會到穩定學習機制對 DQN 收斂的重要性。

# HW 4.1
# 強化學習報告：Double DQN 與 Dueling DQN 的比較分析

## 實驗目標
本次實驗旨在比較改良版深度 Q 網絡（DQN）架構──**Double DQN** 與 **Dueling DQN**──在三種環境模式（Static、Player、Random）下的學習表現，並探討這些方法如何改善基本 Naive DQN 的缺陷。

本次實驗未引入經驗回放（Experience Replay）、目標網路（Target Network）等輔助技術，單純觀察網路結構上的影響。

---

## 實作方法

### Double DQN（DDQN）
Double DQN 為了解決基本 DQN 過度估計 Q 值的問題，將「動作選擇」與「動作評估」分離：  
- 使用主網絡（online network）選擇最佳動作 \( a^* = \arg\max_a Q(s', a; \theta) \)
- 使用目標網絡（target network）評估該動作的 Q 值  
這樣能有效減少高估 Q 值的風險，提升學習的穩定性與準確性。

### Dueling DQN
Dueling DQN 將 Q 值函數拆解為：
- 狀態的價值函數 \( V(s) \)
- 動作的優勢函數 \( A(s, a) \)

網路結構中採用兩條分支分別估計 \( V \) 與 \( A \)，最終合併為：
\[ Q(s, a) = V(s) + \left( A(s, a) - \frac{1}{|\mathcal{A}|} \sum_{a'} A(s, a') \right) \]

此結構允許網路在某些狀態下更聚焦於「估計該狀態好壞」，而不是每次都強調每個動作的比較，特別適用於某些狀態下動作選擇差異性小的情境。

---

## 實驗結果與觀察

### 模式一：Static 模式

- Double DQN 與 Dueling DQN 均展現穩定的收斂特性，最終表現明顯優於基本 DQN。
- 表現幾乎無震盪，累積獎勵穩定上升。
  
**Double DQN in Static mode**

 ![image](https://github.com/user-attachments/assets/26930a1f-88cb-466d-bfc0-76b5366f6152)

**Dueling DQN in Static mode**

![image](https://github.com/user-attachments/assets/1fd7e304-a589-407b-94f5-4e03c2735f10)

---

### 模式二：Player 模式

- 兩種架構在與 Player 對抗時仍能學到有效策略，顯示其在策略選擇與價值評估上具備良好的泛化能力。
- Dueling DQN 表現略勝一籌，推測其能更好地學習「狀態本身」的價值，面對變化較大的玩家行為時，策略選擇較具韌性。

**Double DQN in Player mode**

![image](https://github.com/user-attachments/assets/81154ac8-cd08-4e34-84ef-11ce1018659e)


**Dueling DQN in Player mode**

![image](https://github.com/user-attachments/assets/0617d91b-dbc0-4e0e-8884-3ada9a0b9b57)

---

### 模式三：Random 模式

- 無論是 Double DQN 或 Dueling DQN，皆無法在 Random 模式下學習有效策略，表現明顯下降。
- 可能原因：
  - 初始狀態與對手策略完全隨機，導致樣本分布變異性大。
  - 本實驗未引入經驗回放與目標網路，使得網路難以從非穩定樣本中提取穩定策略。
  - Dueling 結構對狀態價值評估依賴明確特徵，而在隨機初始與對手策略中，這些特徵難以穩定學到。

 **Double DQN in Random mode**
 
 ![image](https://github.com/user-attachments/assets/9a6a382f-bfb4-4e07-b367-7d24cecc67e5)

 
 **Dueling DQN in Random mode**
 
 ![image](https://github.com/user-attachments/assets/37a28879-13d7-4e94-9552-2ba67e0a823c)

---

## 綜合比較與推測

| 模式        | Double DQN 表現 | Dueling DQN 表現 | 備註                       |
|-------------|------------------|------------------|----------------------------|
| Static      | 穩定收斂         | 穩定收斂         | 效果佳，提升明顯          |
| Player      | 穩定收斂         | 最佳表現         | Dueling 更具彈性與泛化能力 |
| Random      | 效果極差         | 效果極差         | 結構改良不足以克服隨機性   |

推測原因總結如下：

1. **結構改良雖提升學習品質，但需配合穩定機制（如經驗回放與目標網絡）才能應對非平穩環境。**
2. **Double DQN 能減少高估，但無法應對樣本分布劇烈變動。**
3. **Dueling DQN 雖能更好提取狀態價值，但在初始狀態與對手策略完全隨機的情境下，難以穩定聚焦學習方向。**

---

## 小結

本次實驗證實：**Double DQN 與 Dueling DQN 在結構上明確改善了基本 DQN 的估計偏差與策略泛化能力**，特別是在 Static 與 Player 模式中，均展現優秀的穩定性與最終表現。然而，**單靠網路結構的改進，仍無法克服高度隨機環境帶來的訓練不穩定性**。


