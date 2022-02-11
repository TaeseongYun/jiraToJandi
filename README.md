# JIRA Automation 

이슈 관리와 릴리즈 노트 업로드 등 개발 이외의 작업을 편하게 하고자 매크로를 개발하였습니다. 

## 기능 (추후 기능추가예정)

### - 테스트 앱 배포 릴리즈 노트 자동생성 및 잔디 전송기능

해당 기능은 배포에 반영된 JIRA QA 이슈를 필터링하여 QA 이슈키를 릴리즈 노트에 반영시키는 스크립트입니다. 
QA 이슈 필터링 기준은 JIRA 이슈의 해결 버전 필드와 argument로 받은 버전 정보가 일치하는 이슈를 가져옵니다.

```shell
./releaseNoteForTestApp.sh <<수정된 버전>> <<수정번호>>
```

------

## 사용 방법

### 1. 공통 준비 작업

JIRA Automation 스크립트를 사용하기 위해서는 몇가지 제반 작업이 필요합니다

JIRA Automation 스크립트는 Python3 기반으로 수행됩니다. macOS에는 Python3가 기본적으로 설치되어있지만 Python3가 없는경우 먼저 설치 후 다음 준비작업을 진행해주세요

파이썬 JIRA 모듈을 설치해야합니다.

```shell
sudo pip3 install jira
```

JIRA 서버에 접근하기 위해 auth.csv 파일에 로그인 정보를 입력해야합니다.
auth.csv 첫줄에는 접근하려는 서버 도메인, 두번째 줄에는 이메일, 세번째 줄에는 토큰 정보 마지막줄에는 잔디 윕훅 URL을 입력합니다.

> 토큰은 https://id.atlassian.com/manage-profile/security 링크에서 발급할 수 있습니다. 

### 2. 스크립트 수행

- **테스트 앱 배포 릴리즈 노트 자동생성 및 잔디 전송기능**

  1. **스크립트 퍼미션 설정**

     스크립트를 처음 수행하기전에 퍼미션을 변경해야합니다.

     ```shell
     chmod 755 releaseNoteForTestApp.sh
     ```

     

  2. **릴리즈 노트 템플릿 수정하기**

     템플릿은 scripts/jira-automation/template/testApp-release-template.md 파일을 수정하면 됩니다.

     

     **템플릿에 사용 가능한 키워드 집합**

  | Key        | Discpriotion                                                 |
  | ---------- | ------------------------------------------------------------ |
  | %(VERSION) | 해결 버전을 나타내는 키워드입니다. 스크립트에서 매개변수로 받은 버전정보를 뜻합니다. |
  | %(ISSUES)  | JIRA QA 이슈 중 해결 버전이 %(VERSION)과 일치하는 모든 이슈 키 집합입니다. |

  

  3. **스크립트 실행하기**

     ```shell
     ./releaseNoteForTestApp.sh <<수정된 버전>> <<수정번호>>
     ```

     해당 스크립트를 수행하면 수정된 버전에 따른 릴리즈노트를 자동적으로 생성하고 잔디 메시지 송신을 수행합니다.
