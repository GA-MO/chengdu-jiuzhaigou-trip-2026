// เปลี่ยนเลขเวอร์ชันเมื่อเพิ่มหรือเปลี่ยนชื่อไฟล์ในรายการ FILES (รูปอยู่ในแคชแยกและไม่ถูกลบตอนอัปเดต)
const CACHE = "chengdu-trip-v16";
const IMAGE_CACHE = "chengdu-trip-images";
const FILES = ["./", "index.html", "manifest.webmanifest", "icon.svg", "plan.jpg", "fonts/bodoni-moda.woff2", "fonts/trirong.woff2", "fonts/trirong-500.woff2", "fonts/trirong-600.woff2"];
const IMAGE_HOSTS = ["commons.wikimedia.org", "thumb.wikimedia.org", "upload.wikimedia.org"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE && k !== IMAGE_CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) return cached;
  const res = await fetch(request);
  if (res.ok) await (await caches.open(IMAGE_CACHE)).put(request, res.clone());
  return res;
}

// หน้าเว็บ: ออนไลน์ให้ได้ของล่าสุดเสมอ (และอัปเดตแคช) ออฟไลน์ค่อยใช้แคช
async function networkFirst(request) {
  try {
    // เน็ตช้าในจีน: รอได้ไม่เกิน 3 วินาที แล้วใช้แคชแทน
    const res = await Promise.race([fetch(request), new Promise((_, reject) => setTimeout(reject, 3000))]);
    if (res.ok) await (await caches.open(CACHE)).put(request, res.clone());
    return res;
  } catch (err) {
    const cached = await caches.match(request, { ignoreSearch: true });
    if (cached) return cached;
    throw err;
  }
}

self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  const url = new URL(e.request.url);
  if (IMAGE_HOSTS.includes(url.hostname)) e.respondWith(cacheFirst(e.request));
  else if (url.origin === location.origin) e.respondWith(networkFirst(e.request));
});
