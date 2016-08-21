# Chatbot

Chatbot 可以將對話向量化，基於與規則庫間的主題相似度匹配，來依照使用者可能的需求提供答覆。

## 匹配示例

更多的樣例可以參照 `example/output.txt`

    Case# 明天早上叫我起床。
    ------------------
    0.4521	鬧鐘      起床
    0.3904	天氣      早上
    0.3067	住宿      起床
    0.1747	病症      起床
    0.1580	購買      早上
    0.1270	股票      早上
    0.1096	觀光      早上

    Case# 明天上海會不會下雨？
    ------------------
    0.5665	天氣      下雨
    0.3918	鬧鐘      下雨
    0.1807	病症      下雨
    0.1362	住宿      下雨
    0.0000	股票
    0.0000	觀光
    0.0000	購買

## 環境需求

* 安裝 python3 開發環境
* 安裝 [gensim – Topic Modelling in Python](https://github.com/RaRe-Technologies/gensim)
* 安裝 [jieba 结巴中文分词 ](https://github.com/fxsjy/jieba)
* 有已訓練好的中文詞向量，根據目錄調整 `Class Console` 的初始化參數
```
import console
c = console.Console(model_path='your_model')
```

## 使用方式

### 聊天機器人

演示可見 `python3 chatbot.py`

### 計算匹配度

```
import console
c = console.Console(model_path='your_model')
speech = input('Input a sentence:')
res,path = c.rule_match(speech) #取得已照相似度排序的規則
c.write_output(speech,res,path)
```

## 規則格式

規則採用 json 格式，樣板規則放置於`\RuleMatcher\rule`中，

```
    {
        "domain": 代表這個規則的抽象概念,
        "response": [
			對應到該規則後，
            機器人所會給予的回覆，
            機器人會隨機抽取一條 response
        ],
        "concepts": [
            該規則的可能表示方式
        ],
        "children": [該規則的子規則，如購買 -> 購買飲料,購買衣服......]
    }
```

### Example

```
    {
        "domain": "購買",
        "response": [
        	"正在將您導向購物模組"
        ],
        "concepts": [
            "購買","購物","訂購"
        ],
        "children": [
            "購買生活用品",
            "購買家電",
            "購買食物",
            "購買飲料",
            "購買鞋子",
            "購買衣服",
            "購買電腦產品"
        ]
    },
```

## 開發日誌

## TODO
* 追加規則案例
* 實作平台 adapter

