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


### Enviroments

```
Python: 3.10.12
Ubuntu 


```
<br>
<br>


## 시연 영상

### 외력 줘서 제조 실행
![Image](https://github.com/user-attachments/assets/749bb68f-a878-47de-ae37-26e699a643c2)


### 컵세팅  
![cobot1_2](https://github.com/user-attachments/assets/b16fb909-83eb-4091-9f9d-b74611c4489b)


### 우유 넣기 
![cobot1_3](https://github.com/user-attachments/assets/d15126ff-1199-4e43-97b3-116de6d06439)


### 얼음 넣기
![cobot1_4](https://github.com/user-attachments/assets/090dc174-5001-44aa-9ab0-dab6b842aacf)


### 흔들어서 음료 섞기
![cobot1_5](https://github.com/user-attachments/assets/b8fad3ca-cf89-4b3a-9c78-5bd236d19f4d)


### 서빙
![cobot1_6](https://github.com/user-attachments/assets/ac6b6979-3ec4-4949-b66b-fcb1c9f06382)


### 적재 (스택 포인터 조정)
![cobot1_7](https://github.com/user-attachments/assets/6cfa213b-e84f-45b1-a486-d38e3a06219e)


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
