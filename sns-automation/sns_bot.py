#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
영농사업화 플랫폼 SNS 자동화 봇
========================================
여러 SNS 플랫폼에 자동으로 포스팅하고 댓글에 반응합니다.

사용법:
  python sns_bot.py post threads              # Threads에 포스팅
  python sns_bot.py reply threads             # Threads 댓글 확인 후 자동 답글
  python sns_bot.py schedule                  # 모든 플랫폼 예약 상태 확인
  python sns_bot.py analytics                 # 분석 리포트

지원 플랫폼:
  - Threads (활성화)
  - Instagram (준비중)
  - Twitter/X (준비중)
  - 텔레그램 (준비중)
  - 네이버 블로그 (준비중)
"""

import os
import sys
import json
import pathlib
import requests
from datetime import datetime

ROOT = pathlib.Path(__file__).parent.parent
STATE = ROOT / "sns-automation" / "state"
STATE.mkdir(parents=True, exist_ok=True)

# 환경 변수
THREADS_USER_ID = os.environ.get("THREADS_USER_ID", "").strip()
THREADS_TOKEN = os.environ.get("THREADS_ACCESS_TOKEN", "").strip()
HANALL_LINK = os.environ.get("HANALL_LINK", "https://hannol.sixshop.com").strip()
PLATFORM_LINK = os.environ.get("PLATFORM_LINK", "https://youngnong.example.com").strip()


# ========== 콘텐츠 템플릿 ==========

CONTENT_TEMPLATES = {
    "monday": {
        "title": "영농형태 진단 📋",
        "text": """당신은 영농형 vs 준비형?

영농을 시작하기 전에 자신의 성향을 파악해야 합니다.
• 영농형: 빨리 시작해서 배운다
• 준비형: 충분히 준비한 다음 시작한다

우리 플랫폼의 '영농형태 진단' 도구로 9개 질문만 답하면
당신에게 맞는 영농 방향이 나옵니다.

지금 바로 시작해보세요 → {LINK}

#영농사업화 #농사계획 #한농대""",
        "emoji": "🌾"
    },
    "tuesday": {
        "title": "KREI 데이터 읽기 📊",
        "text": """내년에 뭘 심을지 아세요?

KREI 농업관측센터는 매달 품목별 재배면적, 출하량,
도매가격 전망을 발표합니다.

이게 "내년 농산물 시장"의 가장 신뢰할 수 있는 신호입니다.

• 배추 면적 ↑ → 내년 배추 가격 ↓ 가능성
• 포도 가격 전망 ↑ → 투자 검토 신호

KREI 데이터를 읽을 줄 알면
남들이 심기 전에 의사결정할 수 있습니다.

→ {LINK}

#농업관측 #KREI #데이터기반"""
    },
    "wednesday": {
        "title": "투입비용 계산하기 💰",
        "text": """영농을 시작하려면 얼마가 필요할까?

초기 투입비용을 제대로 계산하는 게 성공의 첫 걸음입니다.

우리 계산기로:
✓ 품목별 표준 투입비 자동 계산
✓ 자기자본 vs 정부지원금 vs 대출 분석
✓ 손익분기점 예측
✓ 자금 조달 방식 제안

벼 1,000평? 포도 500평?
어떤 규모든 정확한 비용이 나옵니다.

→ {LINK}

#사업계획 #투입비용 #영농자금"""
    },
    "thursday": {
        "title": "수익 예측하기 📈",
        "text": """이 작물, 연간 얼마나 벌 수 있을까?

KAMIS 실시간 가격 + 최근 3년 데이터로
월별·연간 수익을 정확하게 예측합니다.

우리 시뮬레이션으로 확인할 수 있는 것:
✓ 월별 현금흐름 (누가 돈이 들어올지)
✓ 손익분기점 (언제부터 이익이 나는지)
✓ 시나리오별 수익성 비교
✓ 위험도 평가

"1년에 얼마를 벌까?"
정확한 데이터로 판단하세요.

→ {LINK}

#수익예측 #현금흐름 #재무계획"""
    },
    "friday": {
        "title": "사업계획서 자동생성 📄",
        "text": """금융기관 제출용 사업계획서, 직접 만들 필요 없습니다.

위의 진단·계산·시뮬레이션 데이터를 모두 종합해서
자동으로 사업계획서를 생성합니다.

생성되는 문서:
✓ 사업개요 (작물, 규모, 전략)
✓ 재정계획 (투입비, 수익, 손익분기점)
✓ 위험관리 계획
✓ 연간 목표

농협 대출 신청? 정부 지원금 신청?
이 사업계획서 하나면 충분합니다.

→ {LINK}

#사업계획서 #금융기관 #농협대출"""
    },
    "saturday": {
        "title": "정부 지원금 안내 🏛️",
        "text": """청년농업인, 얼마를 받을 수 있나요?

정부가 주는 지원금을 정리했습니다:

✓ 청년농업인 영농정착금: 월 100만원 × 5년
✓ 선도농인 경영비: 연 최대 3,000만원
✓ 한농대 졸업생 특화: 최대 1,500만원
✓ 저금리 정책금융 대출: 연 2~3%

지원금을 받으려면 언제 신청해야 할까?
• 제대 1개월 전 미리 준비 시작
• 각 시·군 농업기술센터에서 상담
• 영농계획서 + 기술교육 수료증 필요

자세한 신청 방법 → {LINK}

#정부지원금 #청년농업 #농협"""
    ),
    "sunday": {
        "title": "위험 관리 체크리스트 ⚠️",
        "text": """6년 의무영농, 예상 위험을 미리 대비하세요.

• 가격 폭락: KREI·KAMIS로 미리 파악
• 천재지변: 농작물 보험 필수
• 병해충: 조기 발견과 예방
• 현금흐름: 월별 정산으로 관리
• 기술 부족: 기술센터 교육 이수

우리 체크리스트로:
✓ 29개 항목 확인
✓ 준비도 자동 평가 (70% 이상 권장)
✓ 단계별 위험 대응 전략

완벽한 준비는 불가능하지만,
70% 이상은 꼭 확인하고 시작하세요.

→ {LINK}

#위험관리 #사전대비 #영농안전"""
    )
}


# ========== 유틸리티 ==========

def load_json(name, default=None):
    p = STATE / name
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return default or {}


def save_json(name, obj):
    (STATE / name).write_text(
        json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def get_daily_content():
    """요일별 콘텐츠 가져오기"""
    day = datetime.now().strftime("%A").lower()
    day_map = {
        "monday": "monday",
        "tuesday": "tuesday",
        "wednesday": "wednesday",
        "thursday": "thursday",
        "friday": "friday",
        "saturday": "saturday",
        "sunday": "sunday"
    }
    return CONTENT_TEMPLATES.get(day_map.get(day, "monday"))


# ========== Threads 통합 (기존 시스템과 동일) ==========

def post_to_threads(text, image_url=None):
    """Threads에 포스팅"""
    if not THREADS_USER_ID or not THREADS_TOKEN:
        print("❌ Threads: 인증 정보 없음")
        return None

    # threads_bot.py의 post 함수 재사용
    sys.path.insert(0, str(ROOT))
    from threads_bot import post
    try:
        media_id = post(text, image_url=image_url)
        print(f"✅ Threads: 포스팅 완료 (ID: {media_id})")
        return media_id
    except Exception as e:
        print(f"❌ Threads: {e}")
        return None


# ========== 명령어 ==========

def cmd_post(platform="all"):
    """SNS에 포스팅"""
    content = get_daily_content()
    if not content:
        print("❌ 오늘 콘텐츠 없음")
        return

    text = content["text"].replace("{LINK}", PLATFORM_LINK)
    title = content["title"]

    print(f"\n{'='*50}")
    print(f"📝 {title}")
    print(f"{'='*50}")
    print(text[:100] + "...")
    print(f"{'='*50}\n")

    if platform in ["all", "threads"]:
        post_to_threads(text)

    # 향후 다른 플랫폼 추가
    if platform in ["all", "instagram"]:
        print("⏳ Instagram: 준비중")
    if platform in ["all", "twitter"]:
        print("⏳ Twitter/X: 준비중")
    if platform in ["all", "telegram"]:
        print("⏳ Telegram: 준비중")


def cmd_reply(platform="threads"):
    """SNS 댓글에 자동 응답"""
    if platform == "threads":
        sys.path.insert(0, str(ROOT))
        from threads_bot import cmd_reply as threads_reply
        threads_reply()
    else:
        print(f"⏳ {platform.upper()}: 준비중")


def cmd_schedule():
    """예약 상태 확인"""
    config = json.loads((ROOT / "sns-automation" / "config.json").read_text(encoding="utf-8"))

    print("\n📅 SNS 포스팅 일정\n")
    for platform, info in config["platforms"].items():
        status = "✅ 활성화" if info["enabled"] else "⏳ 준비중"
        print(f"{platform.upper()}: {status}")
        print(f"  일정: {info['schedule']}")
        print(f"  설명: {info['description']}")
        print()


def cmd_analytics():
    """분석 리포트"""
    analytics = load_json("analytics.json")

    print("\n📊 SNS 분석 리포트\n")
    if analytics:
        print(f"총 포스팅: {analytics.get('total_posts', 0)}")
        print(f"총 조회: {analytics.get('total_views', 0):,}")
        print(f"총 상호작용: {analytics.get('total_engagement', 0)}")
        print(f"클릭률: {analytics.get('ctr', 0):.1f}%")
    else:
        print("아직 데이터가 없습니다.")
    print()


def cmd_help():
    """도움말"""
    print("""
영농사업화 SNS 자동화 봇
================================

사용법:
  python sns_bot.py post [platform]     # 포스팅 (기본: all)
  python sns_bot.py reply [platform]    # 댓글 응답 (기본: threads)
  python sns_bot.py schedule             # 일정 확인
  python sns_bot.py analytics            # 분석 리포트

플랫폼:
  - threads (활성화)
  - instagram, twitter, telegram (준비중)

예:
  python sns_bot.py post threads         # Threads만 포스팅
  python sns_bot.py reply threads        # Threads 댓글 응답
  python sns_bot.py schedule             # 전체 일정 보기
""")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "post"
    arg = sys.argv[2] if len(sys.argv) > 2 else None

    handlers = {
        "post": lambda: cmd_post(arg or "all"),
        "reply": lambda: cmd_reply(arg or "threads"),
        "schedule": cmd_schedule,
        "analytics": cmd_analytics,
        "help": cmd_help,
    }

    if cmd in handlers:
        handlers[cmd]()
    else:
        print(f"❌ 알 수 없는 명령어: {cmd}\n")
        cmd_help()
