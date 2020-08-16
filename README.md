# QuizBot

Simple NLP project.  
Created by [Francesco Zoccheddu](https://www.github.com/francescozoccheddu).


## Installation

Run:
```bash
pip install -v .
python -m spacy download en_core_web_lg
```  


## Usage examples

### Show help message

Run:
```bash
quizbot -h
```  

### Chat via CLI

Run:
```bash
quizbot --cli
```

### Start Telegram bot

Create new file `quizbot/resources/configs/telegram.json` like this:
```javascript
{
    "token": "your bot's token"
}
```
then run:
```bash
quizbot
```