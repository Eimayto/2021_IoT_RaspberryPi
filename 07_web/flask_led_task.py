from flask import Flask
import RPi.GPIO as GPIO

BLUE_PIN = 2
RED_PIN = 3
GPIO.setmode(GPIO.BCM)
GPIO.setup(BLUE_PIN,GPIO.OUT)
GPIO.setup(RED_PIN, GPIO.OUT)

# Flask 객체 생성
app = Flask(__name__) # __name__ = 자기 파일 명


css = '''
body{
    background-color:black;
    font-size:100px;
    color:white;
}
a{
    color:#39FFB9;
    text-decoration:none;
}
.red a{
    color:#FF5C39;
}
.blue a{
    color:powderblue;
}
'''


# 0.0.0.0:5000/
@app.route("/") # 연결되면 hello()에 연결해라
def hello():
    return '''
    <style>''' + css +'''</style>
    <p>Hello, Flask!!</p>
    <div class='red'>
        <a href="/led/red/on" style="padding-right:20px;">RED LED ON</a> 
        <a href="/led/red/off" style="padding-left:20px;">RED LED OFF</a>
    </div>
    <div class='blue'>
        <a href="/led/blue/on" style="padding-right:20px;">BLUE LED ON</a> 
        <a href="/led/blue/off" style="padding-left:20px;"><blue> LED OFF</a>
    </div>
    '''

@app.route("/led/<color>/<op>") # 동적 라우팅
def led_op(color, op):
    re = '<style>' + css + '</style>'
    if color == 'blue':
        LED_PIN = BLUE_PIN
    if color == 'red':
        LED_PIN = RED_PIN

    if op == "on":
        GPIO.output(LED_PIN, GPIO.HIGH)
        return re + '''
        <p>''' + color.upper() + ''' LED ON</p>
        <a href="/">Go Home</a>
        '''
    elif op == "off":
        GPIO.output(LED_PIN, GPIO.LOW)
        return re + '''
        <p>''' + color.upper() + ''' LED OFF</p>
        <a href="/">Go Home</a>
        '''


# 터미널에서 직접 실행시킨 경우
if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", debug=True) # 0.0.0.0 = 127.0.0.1 = localhost
    finally:
        GPIO.cleanup()