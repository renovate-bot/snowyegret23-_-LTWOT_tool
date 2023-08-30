## LTWOT tool

Labyrinth: The War on Terror 텍스트 교체 툴

### 요구 사항

*   Python
*   UABEA

### 사용법

0\. SDF폰트 수정이 이미 되어있다는 것을 전제로 합니다.

1\. UABEA를 통해 resource.assets에서 텍스트 에셋을 추출 (UABEA - resource.assets 오픈 - 추출하고자 하는 에셋 선택 - Plugins - export .txt)  
  (총 6개 - Common\_Ingame, Common\_Strings, Lab\_Cards, Lab\_Ingame, Lab\_RulesTutorial, Lab\_Strings)  
  (파일명 예시는 다음과 같습니다: Common\_Ingame-resources.assets-289.txt)

2\. 추출한 텍스트에셋을 \[1.original\_txt\] 폴더에 위치

3\. main.py를 텍스트 에디터로 열어 제일 아랫부분에 위치한 'if \_\_name\_\_ == "\_\_main\_\_":' if문 코드를 아래와 같이 수정 후 실행  
if \_\_name\_\_ == "\_\_main\_\_":  
   main("extract", down\_csv=False)  
   # main("insert", down\_csv=True)

4\. \[2.export\_csv\] 폴더에 정상적으로 csv 파일들이 생성되었는지 확인

5\. csv 파일을 구글 드라이브에 업로드한 후, 구글 스프레드시트로 열기

6\. 구글 시트 기준 E열(dst 컬럼)을 수정  
  (수정 시 줄바꿈(Ctrl+Enter) 없이 한 문장 그대로 수정하는 것을 권장)  
  (참고용 기계번역 작업본: https://drive.google.com/drive/folders/1uaTJrtudqyS0JkEYmxlim4yUe5neeHwu?usp=sharing)

7\. 수정이 완료되었으면, main.py를 텍스트 에디터로 열어 'file\_info' 딕셔너리 내부 각 파일의 doc\_id와 sheet\_id를 수정  
  (예를 들어, 'Lab\_Strings'의 구글 스프레드시트 주소가 'https://docs.google.com/spreadsheets/d/1Bdxm6u0XjzDBDBpKJDRIUmyf7yuCx_IV9WEbhkMiU58/edit#gid=413374275'라면  
  1Bdxm6u0XjzDBDBpKJDRIUmyf7yuCx\_IV9WEbhkMiU58이 doc\_id고, 413374275가 sheet\_id가 됨.)

8\. main.py 하단부 'if \_\_name\_\_ == "\_\_main\_\_":' if문 코드를 아래와 같이 수정 후 실행  
if \_\_name\_\_ == "\_\_main\_\_":  
   # main("extract", down\_csv=False)  
   main("insert", down\_csv=True)

9\. 4.mod\_txt에 .txt 파일들이 정상적으로 생성되었는지 확인

10\. UABEA를 통해 수정한 텍스트 삽입 (UABEA - resource.assets 오픈 - 수정하고자 하는 에셋 선택 - Plugins - import .txt)