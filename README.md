# AI Voiceover Tool — AI 配音工具

输入文字，AI 润色后一键生成自然语音 MP3。**永久免费**，零成本运行。

## 快速开始

```bash
# 安装依赖
pip install edge-tts requests

# 生成语音
python voiceover.py --text "你好，欢迎使用AI配音工具"

# AI润色后生成
python voiceover.py --text "生活就像一盒巧克力" --polish

# 从文件读取
python voiceover.py --file article.txt --polish

# 列出可用语音
python voiceover.py --list-voices

# 交互模式
python voiceover.py -i
```

## 功能

- **文字转语音** — 输入文字，生成自然 MP3
- **AI 润色** — 使用 GLM-4-Flash 免费模型优化文案，更适合朗读
- **多种语音** — 支持中英文数十种语音（女生/男生/活泼/沉稳）
- **永久免费** — Edge-TTS 零成本，AI 润色使用免费模型

## 示例

```bash
# 直接生成
python voiceover.py --text "今天天气真好" --output 天气.mp3

# 润色后生成
python voiceover.py --text "这个功能很实用" --polish
```

## 可用语音

| 语音名称 | 风格 |
|:---------|:-----|
| zh-CN-XiaoxiaoNeural | 女生，自然亲切 |
| zh-CN-YunxiNeural | 男生，沉稳 |
| zh-CN-XiaoyiNeural | 女生，活泼 |
| zh-CN-YunyangNeural | 男生，专业 |
| zh-CN-XiaohanNeural | 女生，温柔 |
| zh-HK-HiuGaaiNeural | 粤语女生 |

---

## ☕ 赞赏支持

如果这个工具帮到了你，欢迎请我喝杯咖啡 ❤️

| 微信扫一扫赞赏 |
|:--------------:|
| ![微信赞赏码](donate.jpg) |

所有赞赏都会用于持续改进和开发更多免费工具 🙏

## License

MIT
