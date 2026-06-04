#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

OLD = 'Estimate Whisper, ElevenLabs, Google Speech costs. Keyword: <em>speech to text API cost</em>.'

FIXES = {
    'de': 'Whisper, ElevenLabs, Google Speech und OpenAI TTS API-Kosten vergleichen. Keyword: <em>Spracherkennung API Kosten</em>.',
    'fr': 'Comparez Whisper, ElevenLabs, Google Speech et OpenAI TTS en 2026. Keyword: <em>coût API speech to text</em>.',
    'tr': 'Whisper, ElevenLabs, Google Speech ve OpenAI TTS API maliyetleri 2026. Keyword: <em>konuşma tanıma API maliyeti</em>.',
}

for lang, new_text in FIXES.items():
    path = os.path.join(BASE, lang, 'index.html')
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    if OLD in c:
        c = c.replace(OLD, new_text)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f'{lang}: STT pdesc fixed')
    else:
        print(f'{lang}: not found (already fixed or different text)')

print('Done.')
