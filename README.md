# 오늘의 커피

스타벅스 메뉴 중 사람들이 가장 좋아하는 커피를 보여드립니다!

![demo](https://user-images.githubusercontent.com/58046372/109933483-ce5abf80-7d0e-11eb-9b54-3ffc4c5f596c.gif)

### 주요 기능
- 사람들이 많이 찾는 커피 메뉴를 위에 먼저 보여드려요.
- 메뉴 검색을 통해 원하는 커피를 찾을 수 있어요.
- 로그인을 하면 '좋아요' 버튼과 '싫어요'버튼을 이용할 수 있어요.
- 좋아하는 커피에 '좋아요'를 눌러 화면의 위로 올릴 수 있습니다. 반대로 '싫어요'로 화면에서 밑으로 내리는 것도 가능해요.
- 커피에 다른 사람이 남긴 댓글을 확인할 수 있으며 로그인을 하면 댓글을 달 수 있어요.

### 데모 영상
https://youtu.be/FVRb_ukFViM

### 사용 기술
Python, Flask, MongoDB, JWT, JS


### 기능(API 목록)

| 기능 | Method | URL | request | response |
| :- | - | :-: | -: | -: |
| 홈 | GET | / |  | DB에 있는 커피 목록 출력 |
| 로그인 | GET | /login | | 로그인 화면 출력 |
|  | POST | /api/sign_in | ID, PW 전달 | 검증 후 JWT 토큰 생성, 홈으로 이동 |
| 회원가입 | POST | /api/check_nick | 닉네임이 DB에 존재하는지 요청 | 중복 결과 반환(True, False) |
|  | POST | /api/check_dup | ID가 DB에 존재하는지 요청 | 중복 결과 반환(True, False) |
|  | POST | /api/sign_up | 사용자가 입력한 ID, PW, 닉네임 전달 | 유효성 검사 후 DB에 저장 |
| 상세 페이지 | GET | /detail/<number> |  | 해당 메뉴의 이름, 이미지, 좋아요, 싫어요, 댓글 데이터 전달 |
|  | POST | /api/write | 댓글 내용, 작성자, 제품id를 전달 | 토큰(로그인) 확인 후 DB에 저장 |
|  | POST | /api/like | '좋아요'를 누른 커피id 서버에 전달 | 토큰(로그인) 확인 후 '좋아요' +1 |
|  | POST | /api/dislike | '싫어요'를 누른 커피id 서버에 전달 | 토큰(로그인) 확인 후 '싫어요' +1 |
