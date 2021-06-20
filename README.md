# [선릉맥주](https://youtu.be/iNovavF_PoI)

# 프로젝트 소개

## 프로젝트 요약
- **제주맥주**를 모티브로 하여 '선릉맥주'라는 가상의 브랜드, 가상의 상품 기획을 더해 cloning.
- **진행 기간**: 2021.06.04 ~ 06.18
- **기획 포인트**
1. '선릉맥주' 라는 가상의 브랜드 아래, 선릉과 어울리는 각종 술과 음식,굿즈를 판매하는 커머스 서비스
2. '선릉맥주'란?
여행, 휴식과는 거리가 먼 서울, 그 중에서도 가장 치열하고 바쁜 도심 선릉.
그러나 도심 속 지친 직장인들에게도 여행이, 그리고 '당장의' 여행이 필요하다.
언제든지 잠시의 여행을 즐길 수 있게 도와주는 상품들이 있다면?
선릉에서 개발 공부에 지쳐가는 우리에게 여행지의 맥주, 일상을 잊게 하는 굿즈, 맛있는 음식이 있다면 얼마나 좋을까?
이런 소원에서 출발하여, 지금 우리가 갖고 싶은 상품들을 판매하는 가상의 커머스 사이트를 제작하였습니다.

## 팀원 소개
Front - 김건우, 백진수
Back - 김경천,김정연,황복실

## 메인 서비스
1. 상품을 카테고리별로 골라 볼 수 있습니다.
2. 상품을 장바구니에 담을 수 있습니다.
3. 장바구니에서 담은 상품을 조회하고, 수량을 변경하고, 삭제할 수 있습니다.
3. 상품을 바로 주문하거나, 장바구니에 담은 상품을 주문할 수 있습니다.

# 적용 기술 및 구현 기능
## 기술 스택
- Front-End : 
- Back-End : Python, Django, My SQL
- Communication Tool : Trello, Git, GitHub, Slack
## 구현 기능 상세
### 데이터 모델링(김경천,김정연,황복실)
- (데이터 모델링 간단하게 시각화여 추가할 예정)
### 회원가입 페이지 (황복실)
1. 이메일 중복 체크 및 정규식 사용하여 형식 체크
2. 전화번호 중복 체크 및 정규식 사용하여 형식 체크
3. 비밀번호 bcrypt 사용하여 암호화
### 로그인 페이지 (황복실)
1. 인증 방식으로 JWT 방식을 선택, 로그인 성공 시 토큰 발행
### 인증 (황복실)
1. 인증이 필요할 경우, 로그인 시 발행한 JWT를 통한 인증 진행
### 상품리스트 페이지 (김정연)
1. 통신의 효율성을 위해 페이지 내 데이터를 구분하여 각각 통신하도록 구현(상단 카테고리/하단 상품리스트)
2. 필터링 및 페이지네이션
### 상품 상세 페이지 (김경천)
1. 상품 상세 데이터 조회
### 장바구니 페이지 (황복실,김경천)
1. 장바구니 등록
2. 장바구니 조회
3. 장바구니 수량 변경
4. 장바구니 삭제
### 결제 페이지 (김정연)
1. 상품 상세에서 바로 결제
2. 장바구니에서 결제
3. 결제 과정에 트랜잭션 처리

# Reference
1. 이 프로젝트는 [제주맥주]https://jejubeer.co.kr/를 참조하여 학습 목적으로 만들었습니다.
2. !!개발 클론이 아닌 '기획 클론'
선릉맥주 프로젝트는 제주맥주 클론 프로젝트이지만, 백지 상태에서 구현되었습니다.
개발자의 역할은 기획이 아닌, 기획 의도를 현실로 바꾸는, 기획의 ‘구현’이라 생각합니다.
따라서, 기획 과정을 건너 뛰고 구현에 집중하기 위해 제주맥주라는 서비스를 참고한 것일 뿐,
프로젝트의 모든 기능은, 실제 서비스 개발과정과 마찬가지로, 백지 상태에서 구현되었음을 밝힙니다.
3. 프로젝트에 사용한 모든 이미지와 영상은 저작권에 문제가 없는 컨텐츠를 사용하여 만들었습니다.
4. 실무 수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.