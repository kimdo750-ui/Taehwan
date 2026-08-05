# 🚀 배포 가이드

영농사업화 플랫폼을 웹에 배포하는 방법입니다.

---

## 📍 현재 상태

✅ **GitHub 리포지토리 생성 완료**
- 주소: https://github.com/kimdo750-ui/Taehwan
- 모든 파일 커밋 및 푸시 완료
- main 브랜치 설정 완료

---

## 🌐 배포 방법 3가지

### ✨ 방법 1: GitHub Pages (가장 간단)

**Step 1: GitHub 설정**
1. GitHub 리포지토리 열기: https://github.com/kimdo750-ui/Taehwan
2. **Settings 클릭**
3. 왼쪽 메뉴에서 **Pages** 클릭
4. **Source** 설정:
   - Deploy from a branch 선택
   - Branch: `main`
   - Folder: `/ (root)` 선택
5. **Save** 클릭

**Step 2: 확인**
- 2~3분 후 배포 완료
- 웹사이트: `https://kimdo750-ui.github.io/Taehwan/`

**장점**:
- ✅ 설정 간단 (2분)
- ✅ 완전 무료
- ✅ GitHub와 자동 동기화
- ✅ 인증서 자동 포함

**단점**:
- 속도가 Vercel보다 약간 느림

---

### ⚡ 방법 2: Vercel (권장 - 가장 빠름)

**Step 1: Vercel 가입**
1. https://vercel.com 방문
2. "Sign up" → GitHub로 로그인
3. GitHub 권한 허용

**Step 2: 배포**

**옵션 A: 웹 인터페이스**
1. Vercel 대시보드 → "New Project"
2. GitHub에서 `Taehwan` 리포지토리 선택
3. "Deploy" 클릭
4. 완료! 자동으로 배포됨

**옵션 B: 터미널 (빠른 배포)**
```bash
cd "e:\트레이딩\농업사업화"

# Vercel CLI 설치 (처음 1회만)
npm install -g vercel

# 배포
vercel --prod
```

**Step 3: 확인**
- 배포 URL: `https://taehwan.vercel.app/`

**장점**:
- ✅ 매우 빠른 로딩 속도
- ✅ 자동 최적화
- ✅ 커스텀 도메인 지원
- ✅ 매 커밋마다 자동 배포
- ✅ 무료 플랜도 충분함

**단점**:
- 가입 필요 (GitHub 로그인으로 간단)

---

### 🎯 방법 3: Netlify (대안)

**Step 1: Netlify 가입**
1. https://netlify.com 방문
2. "Sign up" → GitHub로 로그인

**Step 2: 배포**

**옵션 A: 웹 인터페이스**
1. Netlify 대시보드 → "Add new site"
2. "Import an existing project" → GitHub 선택
3. `Taehwan` 리포지토리 선택
4. "Deploy site" 클릭

**옵션 B: 터미널**
```bash
cd "e:\트레이딩\농업사업화"

# Netlify CLI 설치
npm install -g netlify-cli

# 배포
netlify deploy --prod --dir .
```

**Step 3: 확인**
- 배포 URL이 표시됨 (커스텀 가능)

**장점**:
- ✅ 매우 간단한 배포
- ✅ 커스텀 도메인 무료
- ✅ 높은 안정성

---

## 🎯 권장 배포 조합

**최고 성능**: Vercel 추천 ⭐⭐⭐⭐⭐
- 가장 빠른 로딩
- 자동 배포
- 무료 플랜 충분

**간단함**: GitHub Pages 추천 ⭐⭐⭐⭐
- 가장 간단 (설정만)
- 코딩 불필요
- GitHub 통합

**균형**: Netlify 추천 ⭐⭐⭐⭐
- 간단하면서 빠름
- 자동 배포

---

## 🔄 자동 배포 설정

모든 플랫폼이 **자동 배포**를 지원합니다:

### Vercel
```
main 브랜치에 푸시 → 자동으로 배포 (1~2분)
```

### Netlify
```
main 브랜치에 푸시 → 자동으로 배포 (1~2분)
```

### GitHub Pages
```
main 브랜치에 푸시 → 자동으로 배포 (2~3분)
```

즉, 코드를 푸시하면 자동으로 웹사이트가 업데이트됩니다!

---

## 📋 배포 후 확인 사항

배포 후 다음을 확인하세요:

- [ ] 웹사이트 열림 (로딩 확인)
- [ ] `index.html` 제대로 표시됨
- [ ] 모든 링크 작동 (diagnosis/, planning/, support/)
- [ ] 스타일 제대로 적용됨 (CSS 로드됨)
- [ ] 모바일 반응형 (휴대폰에서 확인)
- [ ] PWA 설치 가능 (홈 화면 추가)

---

## 🔗 도메인 연결 (선택)

커스텀 도메인을 사용하려면:

### Vercel에서
1. 프로젝트 → Settings → Domains
2. 도메인명 입력
3. DNS 설정 (안내 따라하기)

### Netlify에서
1. Site settings → Domain management
2. "Custom domain" 추가
3. DNS 설정

### 무료 도메인 추천
- **Freenom** (무료)
- **tld.bot** (무료)
- **GitHub Pages** (기본 도메인 무료)

---

## 🔒 HTTPS 보안

모든 배포 플랫폼이 **자동 HTTPS**를 지원합니다:

- Vercel: ✅ 자동 (Let's Encrypt)
- Netlify: ✅ 자동 (Let's Encrypt)
- GitHub Pages: ✅ 자동

특별한 설정 불필요!

---

## 📊 배포 상태 모니터링

### Vercel
```
대시보드 → 프로젝트 → Deployments
```

### Netlify
```
대시보드 → 사이트 → Deploys
```

### GitHub Pages
```
리포지토리 → Settings → Pages
```

---

## 🚨 배포 실패 시 해결법

### "Build failed" 에러
```bash
# 1. 로컬에서 index.html 확인
start index.html

# 2. 필요한 파일 모두 커밋했는지 확인
git status
git log

# 3. 다시 푸시
git push origin main
```

### "Site not found" 에러
- GitHub Pages: Settings → Pages에서 main/root 선택 재확인
- Vercel/Netlify: 리포지토리 재연결

### "스타일이 안 적용됨"
- 캐시 지우기 (Ctrl+Shift+Delete)
- 강력 새로고침 (Ctrl+F5)

---

## 📱 모바일 테스트

배포 후 모바일에서 확인:

1. 웹사이트 방문
2. 공유 → "홈 화면에 추가"
3. 앱처럼 열리는지 확인

PWA가 제대로 작동하면:
- ✅ 앱 아이콘 표시
- ✅ 앱처럼 실행됨 (주소창 없음)
- ✅ 오프라인 지원 (캐시된 페이지)

---

## 🎯 최종 체크리스트

- [ ] GitHub에 모든 파일 푸시 완료
- [ ] 배포 플랫폼 선택 (Vercel 권장)
- [ ] 배포 설정 완료
- [ ] 배포 URL 확인
- [ ] 웹사이트 열림 확인
- [ ] 모바일에서 테스트
- [ ] PWA 설치 테스트
- [ ] 링크 클릭 확인

---

## 🌐 최종 배포 URL

### GitHub Pages
```
https://kimdo750-ui.github.io/Taehwan/
```

### Vercel (권장)
```
https://taehwan.vercel.app/
```

### Netlify
```
https://taehwan.netlify.app/
```

---

## 📞 배포 지원

문제가 발생하면:

1. **Vercel 지원**: https://vercel.com/help
2. **Netlify 지원**: https://docs.netlify.com
3. **GitHub Pages 지원**: https://docs.github.com/pages

---

## 🎉 축하합니다!

영농사업화 플랫폼을 성공적으로 배포했습니다!

이제 아드님은 어디서나 이 도구를 사용할 수 있습니다:
- 💻 PC에서
- 📱 모바일에서
- 🌐 어디서나 인터넷 연결

**Happy Farming! 🌾✨**

---

**배포 날짜**: 2026년 1월  
**플랫폼 버전**: 1.0  
**마지막 업데이트**: 배포 후
