from flask import Flask
import RPi.GPIO as GPIO

LED_PIN = 2
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN,GPIO.OUT)

# Flask 객체 생성
app = Flask(__name__) # __name__ = 자기 파일 명


css = '''
body{
    background-color:black;
    font-size:100px;
    color:white;
}
a{
    color:powderblue;
    text-decoration : none;
}
'''


# 0.0.0.0:5000/
@app.route("/") # 연결되면 hello()에 연결해라
def hello():
    return '''
    <style>''' + css +'''</style>
    <p>Hello, Flask!!</p>
    <a href="/led/on" style="padding-right:20px;">LED ON</a> 
    <a href="/led/off">LED OFF</a>
    '''

@app.route("/led/<op>") # 동적 라우팅
def led_op(op):
    re = '<style>' + css + '</style>'
    if op == "on":
        GPIO.output(LED_PIN, GPIO.HIGH)
        return re + '''
        <p>LED ON</p>
        <a href="/">Go Home</a>
        '''
    elif op == "off":
        GPIO.output(LED_PIN, GPIO.LOW)
        return re + '''
        <p>LED OFF</p>
        <a href="/">Go Home</a>
        '''


# 터미널에서 직접 실행시킨 경우
if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", debug=True) # 0.0.0.0 = 127.0.0.1 = localhost
    finally:
        GPIO.cleanup()