const CACHE_NAME = 'offline-v1';
const assets = [
  '/',
  'index.html',
  './icons/angle-small-left.png',
  './icons/angle-small-right.png',
  './icons/cards-blank_filled.png',
  './icons/cards-blank.png',
  './icons/disk.png',
  './icons/document.png',
  './icons/github.png',
  './icons/heart.png',
  './icons/house-blank_filled.png',
  './icons/house-blank.png',
  './icons/icon.png',
  './icons/insurance.png',
  './icons/plus.png',
  './icons/search.png',
  './icons/settings_filled.png',
  './icons/settings.png',
  './icons/terms-info.png',
  './icons/trash-xmark.png',
  './screens/cards.html',
  './screens/creator.html',
  './screens/main.html',
  './screens/settings.html',
  './screens/legal/credits.html',
  './screens/legal/policy.html',
  './screens/legal/terms.html',
  './styles/style.css'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(assets);
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
