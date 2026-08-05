// Service Worker - 오프라인 지원 및 캐싱
const CACHE_NAME = 'youngnong-v1';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './data-resources.html',
  './manifest.json',
  './diagnosis/farm-path-check.html',
  './diagnosis/channel-margin-calc.html',
  './diagnosis/crop-entry-check.html',
  './planning/investment-cost.html',
  './planning/profit-simulator.html',
  './planning/business-plan-generator.html',
  './support/subsidy-guide.html',
  './support/risk-checklist.html',
  './support/contacts.html'
];

// 설치 단계
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS_TO_CACHE).catch(() => {
        console.log('캐싱 실패 (네트워크 문제 또는 일부 파일): 온라인 상태에서 다시 시도됩니다.');
      });
    })
  );
  self.skipWaiting();
});

// 활성화 단계
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// 요청 단계
self.addEventListener('fetch', event => {
  // 외부 API(KAMIS, KREI 등)는 캐싱하지 않음
  if (event.request.url.includes('kamis') || event.request.url.includes('krei') || event.request.url.includes('garak')) {
    event.respondWith(
      fetch(event.request).catch(() => {
        return new Response('오프라인 상태에서는 실시간 데이터를 불러올 수 없습니다. 인터넷 연결을 확인하세요.', {
          status: 503,
          statusText: 'Service Unavailable'
        });
      })
    );
    return;
  }

  // 로컬 자산은 캐시 우선
  event.respondWith(
    caches.match(event.request).then(response => {
      if (response) {
        return response;
      }
      return fetch(event.request).then(response => {
        if (!response || response.status !== 200 || response.type !== 'basic') {
          return response;
        }
        const responseToCache = response.clone();
        caches.open(CACHE_NAME).then(cache => {
          cache.put(event.request, responseToCache);
        });
        return response;
      }).catch(() => {
        // 네트워크 실패 + 캐시도 없으면
        return new Response('오프라인 상태입니다. 인터넷 연결을 확인하세요.', {
          status: 503,
          statusText: 'Service Unavailable'
        });
      });
    })
  );
});
