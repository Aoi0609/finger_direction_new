# Finger Direction

指の方向を取得するジェネレーター関数

## 環境構築

```shell
pip install git+https://github.com/rionehome/finger_direction
```


```python
from hand_detect import finger_direction

# args : camera_id (default: 0)
# yield : direction ("R" | "L" | None)
# ESC to exit
for direction in finger_direction():
    print(direction)
```
