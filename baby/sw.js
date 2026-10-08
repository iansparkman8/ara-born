const CACHE = "ara-baby-v13";
const FILES = ["./index.html", "./avatar.png", "./avatar.jpg", "./manifest.webmanifest", "./assets/ara.jpg", "./assets/virus.jpg", "./assets/microbe.jpg", "./assets/fungus.jpg", "./assets/plant.jpg", "./assets/animal.jpg", "./assets/human.jpg", "./assets/edge.jpg", "./assets/analog.jpg"];

self.addEventListener("install", (event) => {
  self.skipWaiting();
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(FILES)));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key)))
    )
  );
});

self.addEventListener("fetch", (event) => {
  event.respondWith(caches.match(event.request).then((hit) => hit || fetch(event.request)));
});
