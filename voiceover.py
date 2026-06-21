#!/usr/bin/env python3
"""
AI Voiceover Tool v1.0
AI 配音工具 — 输入文字，AI润色后生成自然语音MP3
永久免费 · 零成本运行（使用 Edge-TTS + GLM-4-Flash）

用法:
  python voiceover.py --text "你好世界"                # 直接输入
  python voiceover.py --file article.txt               # 从文件读取
  python voiceover.py --demo                           # 示例
  python voiceover.py --list-voices                    # 列出可用语音
"""

import argparse
import json
import os
import sys
import subprocess
import re
from datetime import datetime

# ===== 配置 =====
FREE_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
API_KEY = "c9a977acd8044c34b4db930bfa05949f.l8XJrkkloPXRPwAZ"
FREE_MODEL = "glm-4-flash"

VERSION = "1.0.0"

# ===== 工具函数 =====

def print_banner():
    print(f"""
    ╔═══════════════════════════════════╗
    ║     AI Voiceover Tool v{VERSION}         ║
    ║     文字 → AI润色 → 语音MP3       ║
    ║     永久免费 · 零成本运行          ║
    ╚═══════════════════════════════════╝
    """)

def call_ai(prompt, system_prompt=None):
    """调用免费 GLM-4-Flash 润色文案"""
    try:
        import requests
    except ImportError:
        os.system("pip install requests -q")
        import requests
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    try:
        resp = requests.post(
            FREE_API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": FREE_MODEL,
                "messages": messages,
                "max_tokens": 2000,
                "temperature": 0.3
            },
            timeout=60
        )
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        else:
            print(f"⚠️ AI 返回错误: {resp.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ AI 调用失败: {e}")
        return None


def polish_text(raw_text):
    """AI 润色文本，使其更适合朗读"""
    system = "你是一个专业的文案润色助手。将以下文本润色为适合语音朗读的版本：自然口语化、去掉书面语冗余词、保持原意。直接输出润色后的文本，不要加任何解释。"
    return call_ai(raw_text, system)


def list_voices():
    """列出 Edge-TTS 支持的中文语音"""
    try:
        result = subprocess.run(
            ["edge-tts", "--list-voices"],
            capture_output=True, text=True, timeout=30
        )
        lines = result.stdout.split('\n')
        chinese_voices = []
        print("\n🎤 所有可用中文语音：\n")
        print(f"{'语音名称':<40} {'性别':<8} {'风格':<20}")
        print("-"*70)
        for line in lines:
            if 'zh-' in line.lower():
                parts = line.split()
                if len(parts) >= 2:
                    chinese_voices.append(line.strip())
                    print(line.strip())
        
        print(f"\n共 {len(chinese_voices)} 个中文语音")
        print("\n💡 推荐语音：")
        print("  zh-CN-XiaoxiaoNeural  (女生，温暖自然)")
        print("  zh-CN-YunxiNeural     (男生，阳光)")
        print("  zh-CN-XiaoyiNeural    (女生，活泼)")
        print("  zh-CN-YunyangNeural   (男生，专业沉稳)")
        print("  zh-HK-HiuGaaiNeural   (粤语，女生)")
        return chinese_voices
    except Exception as e:
        print(f"❌ 获取语音列表失败: {e}")
        return []


def generate_audio(text, voice="zh-CN-XiaoxiaoNeural", output_path=None):
    """使用 Edge-TTS 生成语音 MP3"""
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"voiceover_{timestamp}.mp3"
    
    print(f"🎤 语音: {voice}")
    print(f"⏳ 生成中...")
    
    try:
        result = subprocess.run(
            ["edge-tts", "--voice", voice, "--text", text, "--write-media", output_path],
            capture_output=True, text=True, timeout=120
        )
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            size_kb = os.path.getsize(output_path) / 1024
            duration = len(text) / 4  # rough estimate: ~4 chars/sec
            print(f"✅ 生成成功: {output_path}")
            print(f"   大小: {size_kb:.1f} KB")
            print(f"   时长: 约{duration:.0f}秒")
            return output_path
        else:
            print(f"❌ 生成失败: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ 生成异常: {e}")
        return None


def read_text_from_file(file_path):
    """从文件读取文本"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return None


# ===== 演示模式 =====

def demo_mode():
    """演示模式"""
    sample_texts = [
        "生活就像一盒巧克力，你永远不知道下一颗是什么味道。",
        "今天天气真好，适合出去走走。阳光明媚，微风不燥。",
        "编程是一门艺术，也是一门科学。它需要创造力，也需要严谨的逻辑。",
        "在这个快节奏的时代，我们常常忘记了停下来，感受生活的美好。",
    ]
    
    print("📝 选择示例文案：")
    for i, t in enumerate(sample_texts, 1):
        print(f"  {i}. {t}")
    
    choice = input("\n选择 (1-4，默认1): ").strip()
    try:
        idx = int(choice) - 1 if choice else 0
        text = sample_texts[min(idx, len(sample_texts)-1)]
    except:
        text = sample_texts[0]
    
    print(f"\n📄 原文: {text}")
    
    polish = input("🤖 是否AI润色? (y/n, 默认n): ").strip().lower()
    if polish == 'y':
        print("🧠 AI润色中...")
        polished = polish_text(text)
        if polished:
            print(f"✨ 润色后: {polished}")
            text = polished
    
    print("\n🎤 选择语音：")
    print("  1. 女生-自然 (Xiaoxiao)")
    print("  2. 男生-沉稳 (Yunxi)")
    print("  3. 女生-活泼 (Xiaoyi)")
    voice_choice = input("选择 (1-3，默认1): ").strip()
    
    voices = ["zh-CN-XiaoxiaoNeural", "zh-CN-YunxiNeural", "zh-CN-XiaoyiNeural"]
    try:
        idx = int(voice_choice) - 1 if voice_choice else 0
        voice = voices[min(idx, len(voices)-1)]
    except:
        voice = voices[0]
    
    generate_audio(text, voice)


# ===== 交互模式 =====

def interactive_mode():
    """交互式输入"""
    print("\n📝 输入要配音的文字（输入空行结束）：")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    
    if not lines:
        print("❌ 没有输入")
        return
    
    text = '\n'.join(lines)
    
    polish = input("\n🤖 是否AI润色? (y/n, 默认n): ").strip().lower()
    if polish == 'y':
        print("🧠 AI润色中...")
        polished = polish_text(text)
        if polished:
            print(f"✨ 润色后: {polished}")
            text = polished
    
    # Show voice options
    print("\n🎤 选择语音：")
    voices = [
        ("zh-CN-XiaoxiaoNeural", "女生-自然亲切"),
        ("zh-CN-YunxiNeural", "男生-沉稳"),
        ("zh-CN-XiaoyiNeural", "女生-活泼"),
        ("zh-CN-YunyangNeural", "男生-专业"),
        ("zh-CN-XiaohanNeural", "女生-温柔"),
    ]
    for i, (_, desc) in enumerate(voices, 1):
        print(f"  {i}. {desc}")
    
    choice = input(f"选择 (1-{len(voices)}，默认1): ").strip()
    try:
        idx = int(choice) - 1 if choice else 0
        voice = voices[min(idx, len(voices)-1)][0]
    except:
        voice = voices[0][0]
    
    generate_audio(text, voice)


# ===== 主程序 =====

def main():
    parser = argparse.ArgumentParser(description='AI 配音工具 - 文字转语音MP3')
    parser.add_argument('--text', '-t', help='直接输入文字')
    parser.add_argument('--file', '-f', help='从文件读取文字')
    parser.add_argument('--voice', '-v', default='zh-CN-XiaoxiaoNeural', help='语音名称')
    parser.add_argument('--output', '-o', help='输出MP3路径')
    parser.add_argument('--polish', '-p', action='store_true', help='AI润色文案')
    parser.add_argument('--demo', action='store_true', help='演示模式')
    parser.add_argument('--list-voices', action='store_true', help='列出可用语音')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互模式')
    
    args = parser.parse_args()
    
    print_banner()
    
    # Check edge-tts
    try:
        subprocess.run(["edge-tts", "--help"], capture_output=True, timeout=5)
    except:
        print("📦 正在安装 edge-tts...")
        os.system("pip install edge-tts -q")
        print("✅ edge-tts 已安装")
    
    if args.list_voices:
        list_voices()
        return
    
    if args.demo:
        demo_mode()
        return
    
    if args.interactive:
        interactive_mode()
        return
    
    # 获取文本
    text = None
    if args.text:
        text = args.text
    elif args.file:
        text = read_text_from_file(args.file)
    else:
        interactive_mode()
        return
    
    if not text:
        print("❌ 没有输入文字")
        return
    
    # AI润色
    if args.polish:
        print("🧠 AI润色中...")
        polished = polish_text(text)
        if polished:
            text = polished
            print(f"✨ 润色后: {text}")
    
    # 生成语音
    generate_audio(text, args.voice, args.output)


if __name__ == '__main__':
    main()
