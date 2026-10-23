# Writes data/categories.json: the Aipex categories and which source boards feed each one.
import json
A = "Arena (arena.ai)"; AA = "Artificial Analysis"
C = []  # (id, name, group, [source keys])
def add(i, n, g, *keys): C.append((i, n, g, list(keys)))
T = "Text & reasoning"
add("text", "Overall chat", T, f"{A} :: Text: Overall", f"{AA} :: LLM Intelligence Index", "LiveBench 2.0 :: LLM overall (LiveBench 2.0)")
add("expert", "Expert questions", T, f"{A} :: Text: Expert")
add("hard", "Hard prompts", T, f"{A} :: Text: Hard Prompts")
add("math", "Math", T, f"{A} :: Text: Math", f"{A} :: Text: Occupational - Mathematical")
add("instr", "Instruction following", T, f"{A} :: Text: Instruction Following")
add("multiturn", "Multi-turn conversation", T, f"{A} :: Text: Multi-Turn")
add("long", "Long queries", T, f"{A} :: Text: Longer Query")
add("writing", "Creative writing", T, f"{A} :: Text: Creative Writing", f"{A} :: Text: Occupational - Writing, Literature, & Language")
add("document", "Document understanding", T, f"{A} :: Document")
add("search", "Search & web answers", T, f"{A} :: Search")
add("science", "Science", T, f"{A} :: Text: Occupational - Life, Physical, & Social Science")
add("medicine", "Medicine & health", T, f"{A} :: Text: Occupational - Medicine & Healthcare")
add("legal", "Law & government", T, f"{A} :: Text: Occupational - Legal & Government")
add("business", "Business & finance", T, f"{A} :: Text: Occupational - Business, Management, & Financial Ops")
add("media", "Entertainment & media", T, f"{A} :: Text: Occupational - Entertainment, Sports, & Media")
K = "Code"
add("coding", "Coding", K, f"{A} :: Text: Coding", f"{A} :: Text: Occupational - Software & IT Services", "LiveBench 2.0 :: LLM coding (LiveBench 2.0)")
add("agents", "Coding agents (harness + model)", K, f"{AA} :: Coding Agent Index")
add("webdev", "Web development", K, f"{A} :: WebDev")
add("img2web", "Screenshot to website", K, f"{A} :: Image-to-WebDev")
L = "Languages"
add("multilingual", "Non-English overall", L, f"{A} :: Text: Non-English")
for lang in ["German", "French", "Spanish", "Russian", "Polish", "Chinese", "Japanese", "Korean"]:
    add(lang.lower(), lang, L, f"{A} :: Text: {lang}")
V = "Vision"
add("vision", "Image understanding", V, f"{A} :: Vision: Overall")
add("caption", "Image captioning", V, f"{A} :: Vision: Captioning")
add("diagram", "Diagrams & charts", V, f"{A} :: Vision: Diagram")
add("visionwriting", "Writing about images", V, f"{A} :: Vision: Creative Writing")
I = "Image generation"
add("t2i", "Text to image", I, f"{A} :: Text-to-Image: Overall", f"{AA} :: Text-to-Image")
add("t2i-photo", "Photoreal & cinematic", I, f"{A} :: Text-to-Image: Photorealistic & Cinematic Imagery")
add("t2i-portrait", "Portraits", I, f"{A} :: Text-to-Image: Portraits")
add("t2i-text", "Text in images", I, f"{A} :: Text-to-Image: Text Rendering")
add("t2i-art", "Art", I, f"{A} :: Text-to-Image: Art")
add("t2i-anime", "Cartoon, anime & fantasy", I, f"{A} :: Text-to-Image: Cartoon, Anime & Fantasy")
add("t2i-product", "Product & branding", I, f"{A} :: Text-to-Image: Product, Branding & Commercial Design")
add("t2i-3d", "3D-style imagery", I, f"{A} :: Text-to-Image: 3D Imaging & Modeling")
E = "Image editing"
add("edit", "Image editing", E, f"{A} :: Image Edit: Single Image Edit (Overall)", f"{AA} :: Image Editing")
add("edit-multi", "Multi-image editing", E, f"{A} :: Image Edit: Multi Image Edit (Overall)")
add("edit-photo", "Photo retouching", E, f"{A} :: Image Edit: Single Image - Photorealistic & Cinematic Imagery")
add("edit-portrait", "Portrait editing", E, f"{A} :: Image Edit: Single Image - Portraits")
add("edit-text", "Text editing in images", E, f"{A} :: Image Edit: Single Image - Text Rendering")
add("edit-product", "Product shots", E, f"{A} :: Image Edit: Single Image - Product, Branding & Commercial Design")
add("bgremoval", "Background removal", E, "Background Removal Arena (Hugging Face) :: Background Removal")
Vi = "Video"
add("t2v", "Text to video", Vi, f"{A} :: Text-to-Video", f"{AA} :: Text-to-Video (with audio, default view)", "VBench Leaderboard (Hugging Face) :: Text-to-Video (VBench automatic metrics)")
add("i2v", "Image to video", Vi, f"{A} :: Image-to-Video", f"{AA} :: Image-to-Video (default view)")
add("vedit", "Video editing", Vi, f"{A} :: Video Edit", f"{AA} :: Video Editing")
Au = "Audio & music"
add("tts", "Text to speech", Au, f"{AA} :: Text-to-Speech", "TTS Arena V2 (Hugging Face, TTS-AGI) :: Text-to-Speech")
add("stt", "Speech to text", Au, f"{AA} :: Speech-to-Text", "Hugging Face Open ASR Leaderboard :: Speech-to-Text (English short-form)")
add("stt-multi", "Speech to text, multilingual", Au, "Hugging Face Open ASR Leaderboard :: Speech-to-Text (multilingual, 7 languages)")
add("stt-long", "Long-form transcription", Au, "Hugging Face Open ASR Leaderboard :: Speech-to-Text (English long-form)")
add("music-vocal", "Songs with vocals", Au, f"{AA} :: Music (vocals)", "Music Arena (CMU G-CLef, Hugging Face) :: Music (vocal)")
add("music-inst", "Instrumental music", Au, f"{AA} :: Music (instrumental)", "Music Arena (CMU G-CLef, Hugging Face) :: Music (instrumental)")
D = "3D"
add("img23d", "Image to 3D", D, "3D Arena (Hugging Face) :: Image-to-3D")
add("scene3d", "3D scene coding (three.js)", D, f"{AA} :: LLM 3D scene building (AA-3D v1.0)")
add("depth", "Depth from a single image", D, "Marigold V2 paper, Table 1 :: Monocular depth (mean AbsRel, 5 datasets)")
R = "Embeddings & retrieval"
M = "MTEB Leaderboard (Hugging Face)"
add("emb-en", "Text embeddings, English", R, f"{M} :: Text Embeddings (MTEB English v2)")
add("emb-multi", "Text embeddings, multilingual", R, f"{M} :: Text Embeddings (MTEB Multilingual v2)")
add("emb-code", "Code embeddings", R, f"{M} :: Code Embeddings (MTEB Code v1)")
add("emb-img", "Image-text embeddings", R, f"{M} :: Image-Text Embeddings (MIEB Multilingual)")
add("emb-mm", "Multimodal embeddings", R, "MMEB Leaderboard (TIGER-Lab, Hugging Face) :: Multimodal Embeddings (MMEB)")
add("vidore", "Visual document retrieval", R, f"{M} :: Visual Document Retrieval (ViDoRe v3)")

skip = [  # duplicates or stale boards (newest data from 2025 / early 2026)
 f"{A} :: Text: Hard Prompts (English)", f"{A} :: Text: English", f"{A} :: Text: Exclude Ties",
 f"{A} :: Vision: English", f"{A} :: Vision: Chinese",
 "OpenCompass Open VLM Leaderboard (Hugging Face) :: Vision-Language Models (OpenVLM avg)",
 "OpenCompass Open VLM Leaderboard (Hugging Face) :: OCR (OCRBench v1 column of OpenVLM)",
 "OCRBench v2 Leaderboard (Hugging Face) :: OCR / Document VQA (OCRBench v2, English)",
 "olmOCR-Bench (Ai2, GitHub README) :: OCR / PDF-to-text (olmOCR-Bench)",
 "SWE-bench :: Coding agents (SWE-bench Multilingual)", "SWE-bench :: Coding agents (SWE-bench Verified)",
 "SWE-bench :: Coding agents (SWE-bench Multimodal)", "Aider Polyglot Leaderboard :: Code editing (Aider polyglot)",
 "Berkeley Function Calling Leaderboard (BFCL v4) :: Tool use / function calling (BFCL)",
 "Hugging Face Open ASR Leaderboard :: Speech-to-Text (English short-form, open weights only)",
]
for s in ["Single Image", "Multi Image"]:
    for sub in ["Product, Branding & Commercial Design", "3D Imaging & Modeling", "Cartoon, Anime & Fantasy", "Photorealistic & Cinematic Imagery", "Art", "Portraits", "Text Rendering"]:
        skip.append(f"{A} :: Image Edit: {s} - {sub}")
m = {k: None for k in skip}
for i, n, g, keys in C:
    for k in keys: m[k] = i
out = {"categories": [{"id": i, "name": n, "group": g} for i, n, g, _ in C], "map": m}
json.dump(out, open("data/categories.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(len(C), "categories")
