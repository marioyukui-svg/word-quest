#!/usr/bin/env python3
"""Parse the 5000-word list markdown into words.js"""
import re, json

INPUT = "/Users/xuan/.hanako/uploads/英语高频五千词 带链接版_副本_mp7vnawc_a8184ea6.md"
OUTPUT = "/Users/xuan/Desktop/OH-WorkSpace/word-quest/words.js"

with open(INPUT, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.strip().split("\n")
words = []

for line in lines:
    line = line.strip()
    if not line:
        continue
    word_match = re.search(r'\[\[([^\]]+)\]\]\s*(.+)$', line)
    if not word_match:
        continue
    word = word_match.group(1).strip()
    rest = word_match.group(2).strip()
    
    first_eng = None
    for i, ch in enumerate(rest):
        if ch.isascii() and ch.isalpha():
            first_eng = i
            break
    
    if first_eng is None:
        meaning = rest
        sentence = ""
        translation = ""
    else:
        meaning = rest[:first_eng].strip()
        sentence_and_trans = rest[first_eng:].strip()
        split_match = re.split(r'(\.\s*)([\u4e00-\u9fff])', sentence_and_trans, maxsplit=1)
        sentence = sentence_and_trans
        translation = ""
        if len(split_match) >= 3:
            sentence = split_match[0] + split_match[1]
            translation = split_match[2] + (split_match[3] if len(split_match) > 3 else "")
        elif "？" in sentence_and_trans:
            parts = sentence_and_trans.split("？", 1)
            if len(parts) >= 2 and any("\u4e00" <= c <= "\u9fff" for c in parts[1]):
                sentence = parts[0] + "？"
                translation = parts[1]
        elif "!" in sentence_and_trans or "！" in sentence_and_trans:
            parts = re.split(r"([！!]\s*)", sentence_and_trans, maxsplit=1)
            if len(parts) >= 3 and any("\u4e00" <= c <= "\u9fff" for c in parts[2]):
                sentence = parts[0] + parts[1]
                translation = parts[2]
    
    words.append({
        "word": word,
        "meaning": meaning,
        "sentence": sentence.strip(),
        "translation": translation.strip()
    })

# Write words.js
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("// Word Quest - Vocabulary Data\n")
    f.write("// Auto-generated from 英语高频五千词\n\n")
    f.write("const WORD_DATA = [\n")
    for w in words:
        wd = json.dumps(w, ensure_ascii=False)
        f.write(f"  {wd},\n")
    f.write("];\n\n")
    f.write(f"// Total: {len(words)} words\n")

print(f"✅ Parsed {len(words)} words → {OUTPUT}")
