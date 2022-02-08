#!/usr/bin/env python
"""
This demo can be ran from the project root directory via:
```sh
python src/main.py
```
It can also be ran via p4a/buildozer.
"""
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
import requests
from cryptography.fernet import Fernet

DEMO_APP_KV_LANG = """
#:import ZBarCam kivy_garden.zbarcam.ZBarCam
#:import ZBarSymbol pyzbar.pyzbar.ZBarSymbol
BoxLayout:
    orientation: 'vertical'
    ZBarCam:
        id: zbarcam
        # optional, by default checks all types
        code_types: ZBarSymbol.QRCODE, ZBarSymbol.EAN13
    Label:
        id: qrlabel
        size_hint: None, None
        size: self.texture_size[0], 50
        text: ', '.join([str(symbol.data) for symbol in zbarcam.symbols])
        on_text: root.calc(self.text)
"""
VALID_STATUS = ['submitted', 'processing', 'complete', 'fail', 'received']
WEBSERVER_FUNC_URL = '{}/work/auth'
WEBSERVER_FUNC_KEY = b'6umrjD0wyVjbW6M8VMSS9qanW7GWu8iL38Fu7ZjToNI='

def run_command(cmd,website_url,func_key):
    cipher_suite = Fernet(func_key)
    cipher_text = cipher_suite.encrypt(cmd.encode())
    payload = {'id': cipher_text.decode('utf8')}
    res = requests.post(WEBSERVER_FUNC_URL.format(website_url), json = payload)
    text = res.text
    return text
def mark_order(order_code, status,website_url,func_key):
    assert status in VALID_STATUS
    cmd = f'func:mark_order|{order_code}|{status}'
    text = run_command(cmd,website_url,func_key)
    return text

WEBSITE= "https://primordiumlabs.com"
WEBSITE= "http://test.primordiumlabs.com:5000"


class DemoApp(App):
    def calc(instance, value):
        if(value != ""):
            decodevalue = value
            if("primordiumlabs.com" in decodevalue):
                ordercode = decodevalue.split("/")[-1][:-1]
                mark_order(ordercode,"received",WEBSITE,WEBSERVER_FUNC_KEY)
                print(f"{ordercode} marked!!")
    
    def build(self):
        x = Builder.load_string(DEMO_APP_KV_LANG)
        x.calc = self.calc
        return x


if __name__ == '__main__':
    DemoApp().run()