# Chatbot

Chatbot 透過將語句向量化來計算主題相似度，再依結果提供迎合使用者需求的答覆。

## 匹配示例

更多的樣例可以參照 `example/output.txt`

輸入：明天早上叫我起床。

|相似度|概念|匹配元|
|------|----|------|
|0.4521|鬧鐘|起床|
|0.3904|天氣|早上|
|0.3067|住宿|起床|
|0.1747|病症|起床|
|0.1580|購買|早上|
|0.1270|股票|早上|
|0.1096|觀光|早上|

輸入：明天上海會不會下雨？

|相似度|概念|匹配元|
|------|----|------|
|0.5665|天氣|下雨|
|0.3918|鬧鐘|下雨|
|0.1807|病症|下雨|
|0.1362|住宿|下雨|
|0.0000|股票||
|0.0000|觀光||
|0.0000|購買||

## 環境需求

* 安裝 python3 開發環境
* 安裝 [gensim – Topic Modelling in Python](https://github.com/RaRe-Technologies/gensim)
* 安裝 [jieba 结巴中文分词 ](https://github.com/fxsjy/jieba)
* 有已訓練好的中文詞向量，並根據檔案位置調整 `Console class` 的初始化參數。
```python
import console
c = console.Console(model_path='your_model')
```

## 使用方式

### 聊天機器人

演示可見 `python3 chatbot.py`

### 計算匹配度

```python
import console

c = console.Console(model_path='your_model')
speech = input('Input a sentence:')
res,path = c.rule_match(speech)
c.write_output(speech,res,path)
```

## 規則格式

規則採用 json 格式，樣板規則放置於`\RuleMatcher\rule`中，

```json
    {
        "domain": "代表這個規則的抽象概念",
        "response": [
		"對應到該規則後",
        	"機器人所會給予的回覆",
        	"機器人會隨機抽取一條 response"
        ],
        "concepts": [
            "該規則的可能表示方式"
        ],
        "children": ["該規則的子規則","如購買 -> 購買飲料,購買衣服......"]
    }
```

### Example

```json
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

* [以 gensim 訓練中文詞向量 ](http://zake7749.github.io/2016/08/28/word2vec-with-gensim/)
* [基於詞向量的主題匹配 ](http://zake7749.github.io/2016/08/30/chatterbot-with-word2vec/)

## TODO
* 追加規則案例
* 實作平台 adapter

