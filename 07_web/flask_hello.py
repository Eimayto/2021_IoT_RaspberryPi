from flask import Flask

# Flask 객체 생성
app = Flask(__name__) # __name__ = 자기 파일 명


css = '''
    p, a{
        font-size:50px;
        text-decoration : none;
        color:black;
    }
'''


# 0.0.0.0:5000/
@app.route("/") # 연결되면 hello()에 연결해라
def hello():
    return '''
    <style>''' + css +'''</style>
    <p>Hello, Flask!!</p>
    <a href="/first">Go First</a>  
    <a href="/second">Go Second</a>
    '''

@app.route("/first")
def first():
    return '''
        <style>''' + css +'''</style>
        <p>First Page</p>
        <a href="/">Go Home</a>
    '''

@app.route("/second")
def second():
    return '''
        <style>''' + css +'''</style>
        <p>Second Page</p>
        <a href="/">Go Home</a>
    '''

# 터미널에서 직접 실행시킨 경우
if __name__ == "__main__":
    app.run(host="0.0.0.0") # 0.0.0.0 = 127.0.0.1 = localhost