# Phoney


## Setup 
1. virtual environment 를 설정합니다.  
```
$ source bin/activate && cd phone
```

1.1 혹은 기존 설정값을 불러옵니다.
```
$ pip install -r requirements.txt && cd phone
```

2. API KEY와 API Secret key를 입력해주세요.
phone > accounts > key.py
key.py안에 넣어주시면됩니다. 

3. 앱을 실행합니다. 
```
$ python manage.py runserver
```

4. 브라우저에서 localhost:8000를 엽니다. 

### Super User Information
* id: admin
* pw: admin123
