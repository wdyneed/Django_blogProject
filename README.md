# 장고를 사용한 개인 블로그 프로젝트

[![Django Version](https://img.shields.io/badge/django-4.2.5-brightgreen)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)

## 개요

이번 블로그 프로젝트는 파이썬과 장고, postgresql로만 간단하게 작성한 프로젝트입니다.  
개인 일기장 같은 느낌으로, 남들이 글을 작성하는 것이 아닌 블로그 주인만 글을 작성할 수 있으며, 남들은 글을 보는 것만 가능합니다.

## 사용한 기술

- [Django](https://www.djangoproject.com/): A high-level Python web framework
- [Python](https://www.python.org/): The programming language used for development
- [Postgresql](https://www.postgresql.org/): The database engine for the project


## 기능 설명 및 화면 설명

- 로그인 기능    

![로그인](https://github.com/wdyneed/django_blog_MadeInDojo/assets/88184651/da5d8bd8-0aba-4c9e-b14e-f88ebdabbfa0)  
블로그를 소유한 사람은 발급받은 자신의 id로 로그인이 가능합니다.


- 글 작성 기능

![글작성화면](https://github.com/wdyneed/django_blog_MadeInDojo/assets/88184651/5f194a60-e284-40b1-837c-d23c7b7ae13f)

제목과 아래 내용을 작성한 후, TOPIC을 골라서 업로드 할 수 있으며, 임시저장도 가능합니다. 제목에 원하는 내용을 작성해서 AI 글 자동 완성 버튼을 클릭하면 작성한 것에 맞게 자동완성이 됩니다.

- 임시저장 리스트

![임시저장리스트](https://github.com/wdyneed/django_blog_MadeInDojo/assets/88184651/6b4fe137-f709-43f2-8eda-a93fd153ddfd)

임시저장을 하면 이런 식으로 창이 뜨면서 원하는 글을 선택하거나 삭제할 수 있습니다.  

- 글 작성 후 페이지

![글 작성후](https://github.com/wdyneed/django_blog_MadeInDojo/assets/88184651/64150cf0-4aa3-42a7-80a1-0806022f75ad)

제목 위에는 작성한 시간과 조회수가 나오게 되고, 제목 아래에는 작성자의 닉네임이 나오게 됩니다.

이미지를 올리지 않으면 오른쪽처럼 NO IMAGE로 나오게 되며, 작성한 사람은 수정과 삭제가 가능합니다. 삭제하기를 누르면 별도의 확인없이 게시글이 삭제가 됩니다.

다음글과 이전글로 이동이 가능하며, 페이지를 공유하는 공유하기 버튼도 존재합니다.


- 글 수정 기능

![게시글 수정화면](https://github.com/wdyneed/django_blog_MadeInDojo/assets/88184651/3cdef6b5-4510-4cad-94e5-8c8d3c77140d)

수정버튼을 누르면 해당 화면이 나오게 되며, 공개여부는 글을 최초로 작성할 때와는 다르게 공개로 되어있습니다.  
내용과 제목을 수정할 수 있으며, TOPIC을 재선택할 수 있습니다.

- 일반 사용자 화면

![일반 사용자화면](https://github.com/wdyneed/django_blog_MadeInDojo/assets/88184651/1ee00c98-276d-4f01-97c1-ccf1ea33a3e0)

일반 사용자의 경우는 수정과 삭제버튼이 없어지며, 위에 Just Write 버튼도 없어진 것을 볼 수 있습니다. 

- 추천 게시글  

![추천 게시글](https://github.com/wdyneed/django_blog_MadeInDojo/assets/88184651/cb850b8a-807b-43d5-8870-46e1761449a0)

글 오른쪽에 존재하는 추천 게시글은 같은 TOPIC에서 가장 최신 게시글들을 보여줍니다.


- 글이 존재하지 않는 메인 페이지

![메인화면](https://github.com/wdyneed/django_blog_MadeInDojo/assets/88184651/328c9b43-c268-4654-895a-f76d46969311)

글을 작성하지 않은 상태면 이렇게 페이지가 나오며, 만약 요리 탭에 게시글을 작성하고 영화 탭에는 작성하지 않았을 때도 마찬가지로 글이 존재하지 않는다고 나오게 됩니다.

- 글이 존재하는 메인 페이지

![글있는 메인화면](https://github.com/wdyneed/django_blog_MadeInDojo/assets/88184651/5a41939d-0314-4010-99d7-37d400fb6873)

글이 존재하는 페이지는 글을 선택할 수 있으며, 최신순과 인기순을 선택하여 정렬할 수 있으며, 글이 6개가 넘어가면 페이지가 추가되어 페이지 이동도 가능합니다.


## 폴더구조

📦blogproject  
 ┣ 📂blogapp  
 ┃ ┣ 📂migrations  
 ┃ ┣ 📂static  
 ┃ ┃ ┣ 📂css  
 ┃ ┃ ┃ ┣ 📜index.css  
 ┃ ┃ ┃ ┣ 📜login.css  
 ┃ ┃ ┃ ┣ 📜navfooter.css  
 ┃ ┃ ┃ ┣ 📜navfooter2.css  
 ┃ ┃ ┃ ┣ 📜post.css  
 ┃ ┃ ┃ ┗ 📜write.css  
 ┃ ┃ ┗ 📂img  
 ┃ ┣ 📂templates  
 ┃ ┃ ┣ 📜edit_post.html  
 ┃ ┃ ┣ 📜index.html  
 ┃ ┃ ┣ 📜login.html  
 ┃ ┃ ┣ 📜popup.html  
 ┃ ┃ ┣ 📜post.html  
 ┃ ┃ ┣ 📜register.html  
 ┃ ┃ ┗ 📜write.html  
 ┃ ┣ 📂templatetags  
 ┃ ┃ ┣ 📜extract_first_image_url.py  
 ┃ ┃ ┣ 📜timetemplates.py  
 ┃ ┃ ┗ 📜__init__.py  
 ┃ ┣ 📜admin.py  
 ┃ ┣ 📜apps.py  
 ┃ ┣ 📜forms.py  
 ┃ ┣ 📜models.py  
 ┃ ┣ 📜serializers.py  
 ┃ ┣ 📜tests.py  
 ┃ ┣ 📜urls.py  
 ┃ ┣ 📜views.py  
 ┃ ┗ 📜__init__.py  
 ┣ 📂blogproject  
 ┃ ┣ 📜asgi.py  
 ┃ ┣ 📜settings.py  
 ┃ ┣ 📜urls.py  
 ┃ ┣ 📜wsgi.py  
 ┃ ┗ 📜__init__.py  
 ┣ 📂media  
 ┃ ┗ 📂images  
 ┣ 📜manage.py  
 ┣ 📜requirements.txt  
 ┗ 📜secrets.json  

