# -*- coding: utf-8 -*-
"""
Adafruit PCA9685 サーボコンロローラライブラリの
PCA9685 クラスを peripheriy ライブラリで書き換えたモジュール。
"""
import time
import math

try:
    from periphery import I2C
except:
    exit('This code requires periphery library.') 

# Registers/etc:
PCA9685_ADDRESS    = 0x40
MODE1              = 0x00
MODE2              = 0x01
SUBADR1            = 0x02
SUBADR2            = 0x03
SUBADR3            = 0x04
PRESCALE           = 0xFE
LED0_ON_L          = 0x06
LED0_ON_H          = 0x07
LED0_OFF_L         = 0x08
LED0_OFF_H         = 0x09
ALL_LED_ON_L       = 0xFA
ALL_LED_ON_H       = 0xFB
ALL_LED_OFF_L      = 0xFC
ALL_LED_OFF_H      = 0xFD

# Bits:
RESTART            = 0x80
SLEEP              = 0x10
ALLCALL            = 0x01
INVRT              = 0x10
OUTDRV             = 0x04

class Periphery_PCA9685(object):
    """
    peripheryライブラリをつかったPCA9685 PWM LED/servo コントローラ。
    """

    def __init__(self, address=PCA9685_ADDRESS, i2cbus=1, debug=False, **kwargs):
        """
        PCA9685を初期化する。
        引数：
            address     I2Cスレーブアドレス
            i2cbus      I2Cバス値
            debug       デバッグフラグ
        戻り値：
            なし
        """
        # Setup I2C interface for the device.
        self.i2c = I2C('/dev/i2c-' + str(i2cbus))
        self.address = address
        #self._device = i2c.get_i2c_device(address, **kwargs)
        self.set_all_pwm(0, 0)
        #self._device.write8(MODE2, OUTDRV)
        self.write8(MODE2, OUTDRV)
        #self._device.write8(MODE1, ALLCALL)
        self.write8(MODE1, ALLCALL)
        time.sleep(0.005)  # wait for oscillator
        #mode1 = self._device.readU8(MODE1)
        mode1 = self.readU8(MODE1)
        mode1 = mode1 & ~SLEEP  # wake up (reset sleep)
        #self._device.write8(MODE1, mode1)
        self.write8(MODE1, mode1)
        time.sleep(0.005)  # wait for oscillator
        self.debug = debug

    def set_pwm_freq(self, freq_hz):
        """
        PWM frequency をセットする。
        引数：
            hertz       freq値
        戻り値：
            なし
        """
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq_hz)
        prescaleval -= 1.0
        if self.debug:
            print('Setting PWM frequency to {0} Hz'.format(freq_hz))
            print('Estimated pre-scale: {0}'.format(prescaleval))
        prescale = int(math.floor(prescaleval + 0.5))
        if self.debug:
            print('Final pre-scale: {0}'.format(prescale))
        #oldmode = self._device.readU8(MODE1)
        oldmode = self.readU8(MODE1)
        newmode = (oldmode & 0x7F) | 0x10    # sleep
        #self._device.write8(MODE1, newmode)  # go to sleep
        self.write8(MODE1, newmode)  # go to sleep
        #self._device.write8(PRESCALE, prescale)
        self.write8(PRESCALE, prescale)
        #self._device.write8(MODE1, oldmode)
        self.write8(MODE1, oldmode)
        time.sleep(0.005)
        #self._device.write8(MODE1, oldmode | 0x80)
        self.write8(MODE1, oldmode | 0x80)

    def set_pwm(self, channel, on, off):
        """Sets a single PWM channel."""
        #self._device.write8(LED0_ON_L+4*channel, on & 0xFF)
        self.write8(LED0_ON_L+4*channel, on & 0xFF)
        #self._device.write8(LED0_ON_H+4*channel, on >> 8)
        self.write8(LED0_ON_H+4*channel, on >> 8)
        #self._device.write8(LED0_OFF_L+4*channel, off & 0xFF)
        self.write8(LED0_OFF_L+4*channel, off & 0xFF)
        #self._device.write8(LED0_OFF_H+4*channel, off >> 8)
        self.write8(LED0_OFF_H+4*channel, off >> 8)

    def set_all_pwm(self, on, off):
        """Sets all PWM channels."""
        #self._device.write8(ALL_LED_ON_L, on & 0xFF)
        self.write8(ALL_LED_ON_L, on & 0xFF)
        #self._device.write8(ALL_LED_ON_H, on >> 8)
        self.write8(ALL_LED_ON_H, on >> 8)
        #self._device.write8(ALL_LED_OFF_L, off & 0xFF)
        self.write8(ALL_LED_OFF_L, off & 0xFF)
        #self._device.write8(ALL_LED_OFF_H, off >> 8)
        self.write8(ALL_LED_OFF_H, off >> 8)

    def software_reset(self, i2cbus=1, **kwargs):
        """Sends a software reset (SWRST) command to all servo drivers on the bus."""
        # Setup I2C interface for device 0x00 to talk to all of them.
        if self.i2c is None:
            self.i2c = I2C('/dev/i2c-' + str(i2cbus))

        #self._device = i2c.get_i2c_device(0x00, **kwargs)
        #self._device.writeRaw8(0x06)  # SWRST
        self.writeRaw8(0x06)

    def writeRaw8(self, value):
        self.i2c.transfer(self.address, [I2C.Message([value & 0xFF])])
    
    def write8(self, register, value):
        self.i2c.transfer(
            self.address, 
            [
                I2C.Message([register, value & 0xFF]), 
                I2C.Message([0], read=False)
                ])

    def readU8(self, register):
        msgs = [
                I2C.Message([register]), 
                I2C.Message([0], read=True)]
        self.i2c.transfer(self.address, msgs)
        return msgs[1].data[0] & 0xFF
        