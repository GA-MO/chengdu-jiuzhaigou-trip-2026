"""Rebuild the GUIDE literal in index.html from the researched JSON files.

Usage: python3 -I build_guide.py /path/to/index.html
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).parent
load = lambda name: json.loads((HERE / f"{name}.json").read_text())

# Thai titles that read better as plain Thai than as a full transliteration
TH = {
    "peoples-park": "สวนประชาชน · ร้านน้ำชาเฮ่อหมิง",
    "dufu": "กระท่อมตู้ฝู่",
    "qingyang": "วังชิงหยาง",
    "panda-base": "ศูนย์แพนด้าเฉิงตู",
    "taikoo-li": "ไท่กู่หลี่ · วัดต้าฉือซื่อ",
    "chunxi-ifs": "ชุนซีลู่ · ไอเอฟเอส",
    "anshun-bridge": "สะพานอานซุ่น · จิ่วเหยี่ยนเฉียว",
    "chenmapo": "เฉินหมาโผวโต้วฝุ",
    "zhanglaoer": "จางเหล่าเอ้อร์เหลียงเฝิ่น",
    "no37": "เกี๊ยวเสฉวนร้านเบอร์ 37",
    "ifs": "ไอเอฟเอส",
    "skp": "เอสเคพี",
    "shop:taikoo-li": "ไท่กู่หลี่",
    "hotpot-base": "ซุปหม้อไฟก้อน · พริกหมาล่า",
    "doubanjiang": "เต้าเจี้ยวพริกผีเซี่ยน",
    "tea": "ชาเสฉวน",
    "panda-goods": "ของที่ระลึกแพนด้า",
    "shu-brocade": "ผ้าไหมซู่จิ่น",
}
KEYS = ["id", "name", "zh", "addr", "th", "at", "photo", "photoCredit", "note", "tags", "ask"]
js = lambda v: json.dumps(v, ensure_ascii=False)


def item(section, it):
    it = dict(it, th=TH.get(f"{section}:{it['id']}", TH.get(it["id"], it["th"])))
    return "{ " + ", ".join(f"{k}:{js(it[k])}" for k in KEYS if it.get(k) is not None or k in ("at", "photo")) + " }"


def groups(section, data, inner):
    out = []
    for g in data["groups"]:
        rows = ",\n".join(f"      {inner(x)}" for x in g["items" if "items" in g else "phrases"])
        key = "items" if "items" in g else "phrases"
        out.append(f"    {{ title:{js(g['title'])}, {key}:[\n{rows},\n    ]}}")
    return ",\n".join(out)


phrase = lambda p: "{ " + ", ".join(f"{k}:{js(p[k])}" for k in ("thai", "zh", "reading")) + " }"
sections = [
    ("see", "Places", "ที่เที่ยว", groups("see", load("places"), lambda x: item("see", x))),
    ("eat", "Food", "ของกิน", groups("eat", load("food"), lambda x: item("eat", x))),
    ("shop", "Shopping", "ช้อปปิ้ง", groups("shop", load("shop"), lambda x: item("shop", x))),
    ("say", "Phrases", "ประโยคจีน", groups("say", load("phrases"), phrase)),
]
body = ",\n".join(f"  {{ id:{js(i)}, title:{js(t)}, th:{js(th)}, groups:[\n{g},\n  ]}}" for i, t, th, g in sections)
tips = ",\n".join(f"    {{ title:{js(t['title'])}, text:{js(t['text'])} }}" for t in load("tips")["tips"])
literal = f"const GUIDE = [\n{body},\n  {{ id:\"tips\", title:\"Tips\", th:\"เคล็ดลับ\", tips:[\n{tips},\n  ]}},\n];"

page = pathlib.Path(sys.argv[1])
src = page.read_text()
start = src.index("const GUIDE = [")
end = src.index("\n];", start) + 3
page.write_text(src[:start] + literal + src[end:])
n = sum(len(g["items"]) for f in ("places", "food", "shop") for g in load(f)["groups"])
print(f"GUIDE rebuilt: {n} items, {sum(len(g['phrases']) for g in load('phrases')['groups'])} phrases, {len(load('tips')['tips'])} tips")
