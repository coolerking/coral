# Coral Dev Board をつかった Donkey Car アプリケーション

Raspberry Pi のかわりに Coral Dev Board JP Version をつかったDonkey Carアプリケーションを提供します。

## Coral Dev Board の結線

| **ピン番号** | **PCA9685側ピン** |
|:--|:--|
| 3 (I2C2:SDA) | SDA |
| 4 (5V) | VCC |
| 5 (I2C2:SCL) | SCL |
| 6 (GND) | GND |

* USBケーブルはmicro-BからUSB-Cに変更する必要あり

## インストール

このリポジトリをCoral Dev Board上に展開し、`myconfig.py`を編集後、`python manage.py drive..`を実行する。
