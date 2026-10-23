# Monocular depth: mean AbsRel over NYUv2, KITTI, ETH3D, ScanNet and DIODE from Table 1 of the
# Marigold V2 paper (arXiv 2609.08084, read 2026-10-23). Rows missing a dataset are left out.
import json
SRC = "Marigold V2 paper, Table 1"
URL = "https://arxiv.org/html/2609.08084v1"
rows = {  # method: (org, [NYUv2, KITTI, ETH3D, ScanNet, DIODE] AbsRel %)
    "Depth Anything V2": ("ByteDance / HKU", [4.5, 7.4, 13.1, 6.5, 6.6]),
    "MoGe": ("Microsoft", [3.1, 7.2, 10.0, 3.3, 29.0]),
    "MoGe-2": ("Microsoft", [3.1, 6.9, 5.0, 3.1, 9.6]),
    "π3": ("Shanghai AI Lab", [2.9, 5.9, 2.9, 2.1, 4.4]),
    "Marigold Depth V1": ("ETH Zurich", [5.5, 9.9, 6.5, 6.4, 10.0]),
    "GeoWizard": ("HKUST", [5.2, 9.7, 6.4, 6.1, 12.0]),
    "Lotus": ("HKUST", [5.4, 8.5, 5.9, 5.9, 9.8]),
    "Lotus-2": ("HKUST", [3.7, 6.7, 4.1, 4.0, 6.5]),
    "Pixel-Perfect Depth (512)": ("Zhejiang University", [4.3, 8.0, 4.5, 4.5, 7.0]),
    "Pixel-Perfect Depth (1024)": ("Zhejiang University", [4.1, 7.0, 4.3, 4.6, 6.8]),
    "InfiniDepth": (None, [4.3, 8.7, 6.1, 4.7, 6.4]),
    "DepthMaster": (None, [4.8, 9.1, 5.4, 5.8, 8.0]),
    "FE2E": (None, [3.8, 6.5, 3.8, 4.3, 5.6]),
    "Marigold V2": ("HUAWEI Bayer Lab", [3.6, 5.4, 2.8, 3.7, 5.2]),
}
entries = sorted(({"model": m, "org": o, "score": round(sum(v) / 5, 2)} for m, (o, v) in rows.items()), key=lambda e: e["score"])
for i, e in enumerate(entries, 1):
    e["rank"] = i
out = {"sources": [{"source": SRC, "url": URL, "categories": [{
    "category": "Monocular depth (mean AbsRel, 5 datasets)", "url": URL,
    "metric": "mean AbsRel %, NYUv2/KITTI/ETH3D/ScanNet/DIODE (π3 trained on ScanNet)",
    "higher_is_better": False, "data_date": "2026-09-08", "entries": entries}]}]}
json.dump(out, open("data/raw/extra-depth.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(len(entries), "entries")
