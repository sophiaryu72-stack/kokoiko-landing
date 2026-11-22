# 코코이코 일본어 랜딩페이지

정적 HTML + Vercel 서버리스 함수(`/api`) 구조. 토스페이먼츠 SDK v2 주문서형(위젯) 테스트 결제.

언어: 일본어(기본, `/`) · 영어(`/en/`) · 한국어(`/ko/`). 페이지 맨 위 언어 바에서 같은 페이지의 다른 언어로 이동. 문구는 `tools/content.py`에서 고치고 `python3 tools/build.py`로 세 언어를 한 번에 재생성.

## 파일 구조

| 파일 | 역할 |
| --- | --- |
| `index.html` | 메인 (지도 · 투어 카드 · 준비 중 체험 · 브랜드 소개) |
| `jeonju-damyang.html` `gangneung.html` `danyang.html` | 상품 상세 3개 (인플루언서 링크 도착지) |
| `compare.html` | 교통비 비교 (금액은 확인 중 표시) |
| `checkout.html` | 결제: 날짜 → 인원 → 대표자 정보 → 동의 → 금액 확정 → 토스 결제 UI |
| `success.html` / `fail.html` | 결제 완료(서버 승인) / 실패·취소 |
| `legal.html` | 特定商取引法に基づく表記 · キャンセルポリシー · プライバシーポリシー |
| `api/config.js` | 클라이언트 키만 브라우저에 전달 |
| `api/order.js` | 상품ID·인원으로 **서버가** 금액과 주문번호 생성 |
| `api/confirm.js` | 금액 검증 → 토스 승인 요청 (시크릿 키는 여기서만 사용) |
| `api/rate.js` | KRW→JPY 당일 환율 (참고 표시용) |
| `api/_lib.js` | 가격표 · 주문번호 서명 (DB 없이 금액 위조 방지) |
| `tools/content.py` | 화면 문구 (ja/en/ko) |
| `tools/build.py` | HTML 생성 스크립트 (문구 수정 후 `python3 tools/build.py`) |
| `en/` `ko/` | 영어·한국어 페이지 (생성물) |
| `tools/dev-server.js` | 로컬 확인용 서버 |

## 로컬에서 보기

```bash
TOSS_CLIENT_KEY=test_gck_docs_Ovk5rk1EwkEbP0W43n07xlzm \
TOSS_SECRET_KEY=test_gsk_docs_OaPz8L5KdmQXkzRz3y47BMw6 \
node tools/dev-server.js
# → http://localhost:3000
```
(또는 `npm i -g vercel` 후 `.env.local`에 키를 넣고 `vercel dev`)

## Vercel 배포

1. 이 폴더를 GitHub 저장소에 올리기 (GitHub Desktop 추천). `.env`, `.env.local`이 올라가지 않았는지 확인
2. vercel.com → Add New… → Project → 저장소 Import
3. Environment Variables에 두 줄 추가
   - `TOSS_CLIENT_KEY` = `test_gck_docs_Ovk5rk1EwkEbP0W43n07xlzm`
   - `TOSS_SECRET_KEY` = `test_gsk_docs_OaPz8L5KdmQXkzRz3y47BMw6`
4. Deploy → `프로젝트명.vercel.app` 주소 확인
5. (OGP) LINE·X 썸네일을 확실히 띄우려면 이미지 주소를 절대 URL로:
   `SITE_URL=https://프로젝트명.vercel.app python3 tools/build.py` 후 다시 push

환경변수를 나중에 넣었다면 Deployments → ⋯ → **Redeploy** 해야 적용됨.

## 결제 보안 설계 (가이드 7-1 STEP 4 체크)

- 시크릿 키는 `api/confirm.js`에서 환경변수로만 읽음. HTML·브라우저 JS에서 `test_gsk` 검색 0건
- `api.tosspayments.com` 호출은 `api/confirm.js` 안에서만
- 금액은 브라우저 값을 믿지 않음: `/api/order`가 가격표로 계산 → 주문번호에 상품·인원을 넣고 HMAC 서명 → `/api/confirm`이 서명 검증 후 가격표로 다시 계산해서 비교, 승인 요청에도 서버 금액 사용
- SDK v2 (`js.tosspayments.com/v2/standard`), `fail.html`은 승인 API 호출 없음
- 금액 조작 테스트: 테스트 모드에서만 `window.widgets` 노출. 결제 페이지 콘솔에서
  `widgets.setAmount({ currency: "KRW", value: 100 })` → 결제 → success에서 「お支払い金額が正しくありません」(AMOUNT_MISMATCH)이 나오면 통과

## 클라이언트 확인 전까지의 가정 (화면에 반영된 것)

- 신청 마감: 출발 4일 전까지 (출발 3일 전 催行 판단 때문)
- 공휴일 목록: `js/common.js`의 `holidays` (2027년분 확인 필요)
- 募集状況(あと◯組): 실데이터가 없어 **테스트 모드에서만 「デモ表示」**로 표시. 라이브 키에서는 숨겨짐
- 연락처·LINE 공식계정·사업자번호·여행업 등록번호·집합장소 출구: 「確定後に掲載」「準備中」
- 교통비 비교 금액: 「確認中」 (공개 운임 확인 후 기준일과 함께 기입)
- 신청자 정보(이름·전화·LINE ID)는 DB가 없어 브라우저에만 저장됨 → 실운영 시 저장·알림 연동 필요
