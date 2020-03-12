# flask 기본 구성

# 1. 모듈 가져오기
from flask import Flask, render_template, request, jsonify
# __init__.py 만들고

# entry가 run.py 이면
from service.ml import detect_lang
# 시작점이 어디냐에 따라 달라짐 <??
# 여기서 시작점은 start.py

# 20200311
from service.db import selectAreaGps, selectAreaindex
# 2. flask 객체 생성 
app = Flask(__name__)

# 3. 라우팅
@app.route('/')
def home() :
    # 기본 지역정보를 최초 화면 구성시 반영하여 처리 
    areas = selectAreaindex()    
    # 구 정보를 gus라는 키값으로 지정하여 랜더링 시 전달하겠다 
    return render_template('dom.html', gus=areas, default=2)

# 둘째날
@app.route('/getAreaGps')
def getAreaGps() :    
    #20200311 
    print(request)
    gu_id = 1 #request
    return jsonify( selectAreaGps( gu_id ) )
    # tmp = [ {'lat':37.55487682, 'Ing':126.9696652},{'lat':37.53378887, 'Ing':127.0171928}]
    ## json 으로 응답 
    ## html이 없다 => 전문통신, 미들웨어서버, API서버 
    ## 무게중심이 client에 쏠려있다 => angularjs, reactjs(페이스북,인스타그램,직방), vue 
    # return jsonify(tmp)

# 3-1. 언어감지 처리 
# GET 방식만 현재 되어 있는데, POST도 지원하겠다 
# 1개의 URL로 여러 메소드를 지원 => restful 
@app.route('/langTypeDetect', methods=['GET','POST'])
def langTypeDetect() :
    if request.method == 'POST' :
        # 1. 원문 데이터 획득 (get, post 방식으로 전달된 데이터 획득)
        # 인덱싱기법을 사용하지 않고, 함수로 값을 추출한다
        # 오류 발생시 에러가 나오지 않고, None으로 리턴되어 처리 가능 
        oriTxt = request.form.get('ori') 
        if not oriTxt :
            return {'code':0, 'lang':'', 'desc':'원문데이터 누락'}
        # 2. 언어 감지
        lang, desc = detect_lang( oriTxt )
        # 2-1. 디비에 로그처리
        # 3. 응답 
        return {'code':1, 'lang':lang, 'desc' :desc}
    else : # GET 
        return render_template('index.html')

# 4. 서버 가동-- 
# run.py를 실행하면 __name__ => 'start(파일명)
if __name__ == '__main__' :
    app.run(debug=True)

## 실제론 여기에서 싸이트 구동하면 됨 