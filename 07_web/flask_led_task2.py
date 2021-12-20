from flask import Flask, render_template
import RPi.GPIO as GPIO

RED_PIN = 2
BLUE_PIN = 3
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN,GPIO.OUT)
GPIO.setup(BLUE_PIN,GPIO.OUT)

# Flask 객체 생성
app = Flask(__name__) # __name__ = 자기 파일 명



# 0.0.0.0:5000/
@app.route("/") # 연결되면 hello()에 연결해라
def hello():
    return render_template("led2.html")

@app.route("/led/<color>/<op>") # 동적 라우팅
def led_op(color, op):
    if color == 'red':
        LED = RED_PIN
    else:
        LED = BLUE_PIN
    if op == "on":
        GPIO.output(LED, GPIO.HIGH)
        return color.upper()+" LED ON"
    elif op == "off":
        GPIO.output(LED, GPIO.LOW)
        return color.upper()+" LED OFF"



# 터미널에서 직접 실행시킨 경우
if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", debug=True) # 0.0.0.0 = 127.0.0.1 = localhost
    finally:
        GPIO.cleanup()