self.addEventListener("install", e => { self.skipWaiting(); e.waitUntil(caches.open("ara-v1").then(c => c.addAll(["./","./index.html","./avatar.jpg","./manifest.webmanifest"]))); });
self.addEventListener("fetch", e => { e.respondWith(caches.match(e.request).then(r => r || fetch(e.request))); });
