# -*- coding: utf-8 -*-
"""

"""
import time

import donkeycar as dk

        
class PCA9685:
    ''' 
    PCA9685 をつかったPWM モータコントローラ。
    peripheryパッケージをつかったAdafruit_PCA9685互換クラスで代用している。 
    一般的なRCカー向け。
    '''
    def __init__(self, channel, address=0x40, frequency=60, busnum=None, init_delay=0.1, debug=False):

        self.default_freq = 60
        self.pwm_scale = frequency / self.default_freq

        from .adafruit import Periphery_PCA9685
        self.pwm = Periphery_PCA9685(address=address, i2cbus=busnum, debug=debug)
        self.pwm.set_pwm_freq(frequency)
        self.channel = channel
        time.sleep(init_delay) # "Tamiya TBLE-02" makes a little leap otherwise

    def set_pulse(self, pulse):
        try:
            self.pwm.set_pwm(self.channel, 0, int(pulse * self.pwm_scale))
        except:
            self.pwm.set_pwm(self.channel, 0, int(pulse * self.pwm_scale))

    def run(self, pulse):
        self.set_pulse(pulse)