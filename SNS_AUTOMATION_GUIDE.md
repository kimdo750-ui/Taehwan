# 🚀 영농사업화 플랫폼 SNS 자동화 가이드

## 개요

영농사업화 플랫폼의 콘텐츠를 자동으로 여러 SNS에 포스팅하고, 댓글에 자동으로 응답하는 시스템입니다.

- **현재 활성화**: Threads (Meta)
- **준비중**: Instagram, Twitter/X, 텔레그램, 네이버 블로그

---

## 1️⃣ 설정 (첫 1회)

### 1.1 환경 변수 설정

`sns-automation/config.json`에서 플랫폼별 설정을 관리합니다.

#### Threads 설정 (이미 완료한 경우)
```
THREADS_USER_ID=숫자ID
THREADS_ACCESS_TOKEN=long-lived token (60일)
HANALL_LINK=https://hannol.sixshop.com (또는 당신의 쇼핑몰 링크)
PLATFORM_LINK=https://youngnong.example.com (영농사업화 플랫폼 링크)
```

GitHub Secrets에 등록:
1. Repository → Settings → Secrets and variables → Actions
2. New repository secret 클릭
3. 위의 4개 값 추가

---

## 2️⃣ 콘텐츠 전략

매주 요일별로 다른 주제를 자동 포스팅합니다:

| 요일 | 주제 | 내용 |
|------|------|------|
| **월** | 영농형태 진단 | 당신의 성향 파악하기 |
| **화** | KREI 데이터 | 내년 농산물 시장 예측 |
| **수** | 투입비용 계산 | 초기 자금 규모 결정 |
| **목** | 수익 시뮬레이션 | 월별·연간 현금흐름 |
| **금** | 사업계획서 | 금융기관 제출용 문서 |
| **토** | 정부 지원금 | 청년농업인 지원 안내 |
| **일** | 위험 관리 | 사전 대비 체크리스트 |

---

## 3️⃣ 로컬에서 테스트

### 포스팅 테스트
```bash
cd sns-automation
export THREADS_USER_ID=your_id
export THREADS_ACCESS_TOKEN=your_token
export HANALL_LINK=https://...

python sns_bot.py post threads    # Threads만 포스팅
python sns_bot.py post all        # 모든 플랫폼 (현재는 Threads만)
```

### 댓글 응답 테스트
```bash
python sns_bot.py reply threads   # Threads 댓글 '✓' 자동 응답
```

### 일정 확인
```bash
python sns_bot.py schedule        # 모든 플랫폼 포스팅 일정 보기
```

### 분석 리포트
```bash
python sns_bot.py analytics       # 조회수·상호작용 등 통계
```

---

## 4️⃣ GitHub Actions 자동화

### 자동 포스팅 워크플로우
**파일**: `.github/workflows/sns-daily-post.yml`

- **시간**: 매일 20:30 KST
- **내용**: 요일별 콘텐츠 자동 포스팅
- **수동 실행**: Actions 탭에서 "Run workflow" 클릭

### Threads 댓글 응답 워크플로우 (기존)
**파일**: `.github/workflows/threads-reply.yml`

- **시간**: 3시간마다
- **내용**: '✓' 댓글 감지 → 자동 응답
- **대상**: Threads, 향후 다른 SNS

---

## 5️⃣ 포스팅 커스터마이징

### 콘텐츠 수정하기

**파일**: `sns-automation/sns_bot.py` > `CONTENT_TEMPLATES`

```python
CONTENT_TEMPLATES = {
    "monday": {
        "title": "원하는 제목",
        "text": """
원하는 콘텐츠
{LINK} 은 플랫폼 링크로 자동 치환됩니다.
"""
    },
    # 나머지 요일도 동일하게 수정
}
```

### 해시태그 수정하기

**파일**: `sns-automation/config.json` > `content_strategy.hashtags`

```json
"hashtags": {
  "korean": ["#영농사업화", "#농사", ...],
  "general": ["#농업", "#영농", ...]
}
```

### 포스팅 시간 변경

**Threads 포스팅 시간**: `.github/workflows/sns-daily-post.yml`
```yaml
- cron: "30 11 * * *"   # UTC 기준 (KST = UTC+9)
# 예: 19:00 KST = 10:00 UTC = "0 10 * * *"
```

**댓글 응답 주기**: `.github/workflows/threads-reply.yml`
```yaml
- cron: "0 */3 * * *"   # 3시간마다
```

---

## 6️⃣ 향후 추가 플랫폼

### Instagram (준비중)
```
env:
  INSTAGRAM_ACCESS_TOKEN: (필요)
  INSTAGRAM_BUSINESS_ACCOUNT_ID: (필요)
```

### Twitter/X (준비중)
```
env:
  TWITTER_BEARER_TOKEN: (필요)
  TWITTER_API_KEY: (필요)
  TWITTER_API_SECRET: (필요)
```

### 텔레그램 (준비중)
```
env:
  TELEGRAM_BOT_TOKEN: (필요)
  TELEGRAM_CHANNEL_ID: (필요)
```

### 네이버 블로그 (준비중)
```
env:
  NAVER_CLIENT_ID: (필요)
  NAVER_CLIENT_SECRET: (필요)
  NAVER_BLOG_ID: (필요)
```

---

## 7️⃣ 문제 해결

### Threads 포스팅 실패
```
❌ 인증 정보 없음
→ GitHub Secrets 확인 (THREADS_USER_ID, THREADS_ACCESS_TOKEN)

❌ 토큰 만료
→ python sns_bot.py refresh 실행 후 새 토큰으로 업데이트
```

### 댓글 응답 안 됨
```
→ Threads에서 '✓' 댓글 있는지 확인
→ replied_ids.json이 중복 방지하고 있는지 확인
→ 수동 테스트: python sns_bot.py reply threads
```

### 일정대로 실행 안 됨
```
→ GitHub Actions 탭에서 워크플로우 실행 로그 확인
→ 시간 설정이 UTC 기준인지 확인 (KST = UTC+9)
→ Secrets 값이 올바른지 재확인
```

---

## 8️⃣ 모니터링

### 자동 리포트 받기

**파일**: `sns-automation/state/analytics.json`

주요 지표:
- **total_posts**: 누적 포스팅 수
- **total_views**: 누적 조회수
- **total_engagement**: 누적 상호작용 (좋아요+댓글+공유)
- **ctr**: 클릭률 (클릭 ÷ 조회)

### 실시간 모니터링

```bash
# 최근 포스팅 확인
python sns_bot.py schedule

# 분석 리포트
python sns_bot.py analytics
```

---

## 🎯 체크리스트

- [ ] GitHub Secrets에 `THREADS_USER_ID`, `THREADS_ACCESS_TOKEN` 등록
- [ ] `sns-automation/config.json` 활성화 플랫폼 확인
- [ ] 로컬에서 `python sns_bot.py post threads` 테스트
- [ ] GitHub Actions 워크플로우 활성화 확인 (`.github/workflows/`)
- [ ] 첫 자동 포스팅 결과 확인 (내일 20:30 KST)
- [ ] 콘텐츠 커스터마이징 (필요시)
- [ ] 주간 분석 리포트 설정 (선택)

---

## 📞 문의

문제가 발생하면:
1. GitHub Actions 로그 확인 (Repository → Actions)
2. `sns-automation/state/` 의 오류 로그 확인
3. 환경 변수 및 토큰 유효성 재확인

Happy farming! 🌾
