import spidev
import time
import RPi.GPIO as GPIO



LED = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)

# SPI 인스턴스 생성
spi = spidev.SpiDev()

# SPI 통신 시작 ( spi.start() 아님! )
spi.open(0,0)    # bus:0, dev:0 (CE0, CE1)

# SPI 통신 최대 속도 설정
spi.max_speed_hz = 1000000

# 0~7까지 채널에서 SPI 데이터 읽기 ( 안 내용 이해하려 하지 마라! )


def analog_read(channel):
    # [byte_1, byte_2, byte_3]
    # byte_1 : 1
    # byte_2 : channel(0) + 8 -> 0000 1000 << 4 -> 1000 0000
    # byte_3 : 0
    ret = spi.xfer2([1, (channel + 8) << 4, 0])
    adc_out = ((ret[1] & 3) << 8) + ret[2]
    return adc_out


try:
    while True:
        ldr_value = analog_read(0)    # 0 ~ 1023
        if(ldr_value >= 512):
            GPIO.output(LED, GPIO.LOW)
        else:
            GPIO.output(LED, GPIO.HIGH)
finally:
    spi.close()
    GPIO.cleanup()