# 팀 생성 후 해야 할일
필수가 아닌 것도 있습니다. Notion 등을 사용하셔도 좋습니다.

0. 팀편성
1. 친해지기
2. 팀장 뽑기
3. 오거나이제이션 만들기
    * (권장) organization > New organization > free
    * (권장) 오거나이제이션 동료 초대: People > invite member
    * 레포 만들기: create a new repo
    * 레포에서 동료 초대: settings > collaborators and teams > add people
4. (필수는 아닙니다. 팀 취향입니다.) 이슈, 프로젝트, 위키, 액션스 세팅, 깃 브랜치 전략
    * GitHub Project
        * 레포가 삭제되도 살아있습니다.
        * 다른 레포에 이슈도 등록할 수 있어요. 한 레포에 종속된 것이 아닙니다. 일반적으로는 한 레포에만 사용합니다.
        * Table, Board, Roadmap 하나 선택해도 view에서 여러개를 만들 수 있습니다.
        * TODO에 여러 task 반영
        * Table에서 역활 분담
        * (팀에서 논의 후 반영) Table에서 시작일(날짜), 종료일(날짜), 우선순위(숫자) 반영
        * roadmap에서 Date fields > start date과 target date 설정
        * 프로젝트 진행하면서 우선순위대로 정렬해보고 아직 진행하지 못한 것이 있으면 다같이 진행합니다.
        * (필수 아닙니다.) Set limit을 통해 todo에 너무 많은 항목이 올라가지 않도록 조절합니다.
        * (필수 아닙니다.) chart로 통계치도 확인할 수 있습니다.
        * (필수 아닙니다.) item을 클릭하여 아카이브 할 수 있습니다. 프로젝트에 아카이브 아이템스를 클릭하면 아카이브된 목록들을 볼 수 있습니다.
            * 아카이브를 사용하는 경우 1: 예를 들어 Done이 수백개 쌓였을 경우
            * 만약 하나의 project에 아카이브가 너무 많을 경우 버전을 올리고 새로운 project를 만든 후 project 자체를 아카이브(close) 합니다.
    * GitHub issues
        * 어떠한 이슈가 생겼을 때에만 사용하는 것은 아닙니다!
        * 과업을 설정하거나
        * Code 단위에 해결 마일 스톤을 만들 수 있습니다.
        * Code를 연결할 수 있습니다.
        * 이슈 생성 후 프로젝트에 할당해서 프로젝트 보드에서 보는 것도 가능합니다.
        * 프로젝트에 할당해서 연결된 것도 확인해보세요.
    * GitHub Wiki
        * 처음 페이지 설계를 잘 하셔야 합니다.
        * sidebar는 작성하지 않으셔도 됩니다.
        * wiki만 따로 clone도 가능합니다.
    * GitHub Actions(권장 X)
        * CI/CD를 위한 툴입니다.
        * 자동 크롤링 / 자동 배포 등을 할 수 있습니다.


# GitHub 고급 명령어
## 기본 명령어(이전에 학습)
    * git init 또는 git clone
    * git pull: 소스 코드 받아오는 것
    * 소스코드 수정
    * git add: 내 소스코드 추가
    * git commit: 버전 생성
    * git push: GitHub에 추가

## 1. GUI SW
    * 소스트리 (권고)
    * 깃크라켄
    * 깃허브 데스크탑 (비사용 권고)
    * https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens
    * VSC Extension, gitlens: https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens
        - 무료판, 기능이 적음.
        - 2개 같이 사용하는 분도 많으십니다.
    * VSC Extension, git graph:https://marketplace.visualstudio.com/items?itemName=mhutchie.git-graph
        - 시각화가 잘 되어 있습니다.
        - 2개 같이 사용하는 분도 많으십니다.
    * 깃모지: https://gitmoji.dev/ (실무에서 많이 사용하고 commit에서 메시지로만 주셔도 됩니다. -m ':bug: 버그 고침', VSC 익스텐션으로 많이 사용하고 $ npm i -g gitmogi-cli로 인스톨하여 cli에서 사용할 수도 있습니다.)
    * 팀 프로젝트 할 때 라이브 쉐어와 같은 VSC 익스텐션을 사용하시면 좋습니다. https://visualstudio.microsoft.com/ko/services/live-share/

## 2. branch 만들기 및 merge test
* 고급 명령어 실습
    ```shell
    (main) mkdir test
    (main) cd test
    (main) git init
    (main) touch readme.md
    (main) git add .
    (main) git branch // 1번째 commit은 있어야 branch가 생성됩니다.
    (main) git branch a
    (main) git branch // a 생성된 것 확인
    (main) git checkout a
    (a) echo '# hello world a' >> 'hello_a.txt'
    (a) git status // 추적 확인
    (a) git add .
    (a) git commit -m 'a1'
    (a) git branch b // 브랜치 b 생성
    (a) git branch
    (a) git checkout main
    (main) // hello_a.txt가 없음을 확인
    (main) git checkout b
    (b) echo '# hello world b' >> 'hello_b.txt'
    (b) git status // 추적 확인
    (b) git add .
    (b) git commit -m 'b1'
    (b) git checkout main
    (main) git merge a
    (main) git merge b // 완료!
    ```

* GitHub push 실습
    ```shell
    (main) mkdir test
    (main) cd test
    (main) git clone https://github.com/paullabkorea/branch_test.git .
    (main) git branch // main은 있습니다.
    (main) git branch a
    (main) git branch // a 생성된 것 확인
    (main) git checkout a
    (a) echo '# hello world a' >> 'hello_a.txt'
    (a) git status // 추적 확인
    (a) git add .
    (a) git commit -m 'a1'
    (a) git push // error
    (a) git push --set-upstream origin a
    (a) git branch b // 브랜치 b 생성
    (a) git branch
    (a) git checkout main
    (main) // hello_a.txt가 없음을 확인
    (main) git checkout b
    (b) echo '# hello world b' >> 'hello_b.txt'
    (b) git status // 추적 확인
    (b) git add .
    (b) git commit -m 'b1'
    (b) git push --set-upstream origin b
    (b) git checkout main
    (main) git merge a
    (main) git merge b // 완료!
    ```

* 충돌 실습
    ```shell
    (main) mkdir conflict
    (main) cd conflict
    (main) git init
    (main) touch readme.md
    /// readme에 입력
    hello world
    ///
    (main) git add .
    (main) git commit -m 'first'
    (main) git log // 1번째 commit은 있어야 branch가 생성됩니다.
    (main) git branch a
    (main) git branch b
    (main) git branch // a 생성된 것 확인
    (main) git checkout a
    /// readme에 입력
    hello world a
    ///
    (a) git add .
    (a) git commit -m 'a1'
    (a) git checkout b
    /// readme에 입력
    hello world b
    ///
    (b) git add .
    (b) git commit -m 'b1'
    (b) git checkout main
    (main) git merge a
    (main) git merge b // 충돌!
    ```

* 충돌이 나면 아래와 같이 나옵니다. VSC 보시면 아래와 같이 하이라이팅 되고, 선택할 수 있습니다.
<<<<<<< HEAD
hello world a
=======
hello world b
>>>>>>> b

* 충돌 해결한 후 아래와 같이 add와 commit을 해주셔야 합니다. 그냥 머지가 안됩니다!
```
git add .
git commit -m '충돌해결'
```

* 기타 명령어
```
$ git branch -D <삭제할 브랜치명> // 브랜치 삭제
$ git reflog // 브랜치 복구
```

## 3. Fork
1. (담당자) 오거나이제이션에서 레포하나를 readme파일이 있는 상태로 퍼블릭 만들어주세요.
2. (여러분) 오른쪽 상단에 Fork 버튼을 클릭하여 내 repo로 해당 repo를 가져옵니다.
3. (여러분) 파일을 수정합니다.
4. (여러분) contribute라는 버튼이 코드위에 활성화 되어 있습니다. 이걸 클릭해주세요. 그러면 Open a pull request버튼이 나오고 이걸 클릭하면 title과 content를 입력할 수 있는 form이 나옵니다. 입력 후 하단에 create pull request를 클릭해주세요.
5. (담당자) 풀리퀘스트를 오거나이제이션에서 확인하고 리뷰나 머지를 할 수 있습니다. filechage와 같은 곳에서 코드 단위로 리뷰가 가능합니다.


## 4. 그 외 실무에서 간혹 쓰이는 명령어(amend, stash, reset, revert, cherry-pick)

```shell
$ git add amend.txt
$ git commit --amend

//////////

$ touch test.txt
$ git stash
$ git status
$ git stash pop

//////////

$ git log
$ git reset --hard 025cd1d98da39af2a819c43e17b3d5f2d553649d
$ git push -f origin main

//////////

$ git revert <직전커밋 id>

//////////

$ git branch cherry
$ git checkout cherry
$ 파일 수정 -> commit
$ 파일 생성 -> commit
$ git push
$ git log
$ git switch main
$ git cherry-pick logid

```
