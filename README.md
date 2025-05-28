# 아메리카노 봇  
**ROS2를 이용한 로봇자동화 공정 시스템 구현**

<br>
<br>


### Contributors
|문준웅|강인우|나승원|장연호|
|----|----|----|----|
|**[???](https://github.com/)**|**[kiw331](https://github.com/kiw331)**|**[lala4768](https://github.com/lala4768)**|**[???](https://github.com/)**|

<br>

## How to use  
  
### DART-Studio (Window)  
`제어기 연결 설정` → `로봇 모델 설정`→`Request` → `Servo On` → `Automode` → 실행

<br>


### ROS2 패키지 (Ubuntu)  

```bash
cd ros2_ws/src  #ros2 작업환경
git clone https://github.com/rokeycb4/cobot1.git

cd ..
colcon build
source install/setup.bash

export PYTHONPATH=$PYTHONPATH:~/ros2_ws/install/dsr_common2/lib/dsr_common2/imp
ros2 launch ...
ros2 run cobot1 americano_bot


```

<br>


### Requirements

```
  Python >= 3.10
```
<br>
<br>


## 시연 영상

### 외력 줘서 제조 실행
<br>
![Image](https://github.com/user-attachments/assets/6ce0aa03-bf09-41a0-b35f-e6674414d1a3)

### 우유 넣기 
<br>


### 얼음 넣기
<br>


### 흔들어서 음료 섞기
<br>


### 서빙
<br>



## License
```
The MIT License (MIT)

Copyright (c) 2025 AmericanoBot

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```


<br>


## Reference
- https://github.com/ROKEY-SPARK/DoosanBootcamp
- https://manual.doosanrobotics.com/ko/programming/2.11.2/Publish/
