from flask import Flask, render_template

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
    return render_template(
        'hello.html',
        title="Hello, Flask!!!!"
       )

@app.route("/first")
def first():
    return render_template(
        'first.html',
        title="First Page"
        )

@app.route("/second")
def second():
    return render_template(
        'second.html',
        title="Second Page"
        )

# 터미널에서 직접 실행시킨 경우
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True) # 0.0.0.0 = 127.0.0.1 = localhost
