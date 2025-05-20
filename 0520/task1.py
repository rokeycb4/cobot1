##블럭 정렬
def grab():
    set_digital_output(1,1)
    set_digital_output(2,1)
    wait(1)

def release():
    set_digital_output(2,0)
    set_digital_output(1,1)
    
    
def force_control_on():
    k_d = [3000.0,3000.0,3000.0,  200.0,200.0,200.0]
    task_compliance_ctrl(k_d)
    force_desired = 20.0
    f_d = [0,0,-force_desired,0.0,0.0,0.0]
    f_dir = [0,0,1,0,0,0]
    set_desired_force(f_d,f_dir)

def force_control_off():
    release_force()
    release_compliance_ctrl()
    
    
# src에서 잡아서 des에 놓기
def grab_place(src, des, upheight, upheightd, obj='cup'):


    #내려갈값 구하기
    height = get_current_posx()[0][2] - src[2]

    # z값 유지하면서 이동
    src_ = trans(src,[0,0,0, 0,0,0], DR_BASE, DR_BASE)
    src_[2] = get_current_posx()[0][2]
    movel(src_)
    
    # 내려서 잡고 올리기
    movel([0,0,-height, 0,0,0], mod=1)
    grab(obj)
    wait(0.5)
    movel([0,0,upheight, 0,0,0], mod=1)
    
    #내려갈값 구하기
    height = get_current_posx()[0][2] - des[2]
    
     # z값 유지하면서 이동
    des_ = trans(des,[0,0,0, 0,0,0], DR_BASE, DR_BASE)
    des_[2] = get_current_posx()[0][2]
    movel(des_)
    
    # 내리고 놓고 올리기
    movelz(-height)
    release()
    movelz(upheightd)
    
    
def get_height(pos):
    """ 높이 구하기"""
    grab()
    
    movel(pos)
    force_control_on()
    
    
    while True:
        t = get_tool_force()
        if t[2] > 20:
            current_height = get_current_posx()[0][2]
            force_control_off()
            return current_height
            

        
def get_next_des(h):
 """높이에 맞는 다음 도착지 구하기"""


    global high_idx, mid_idx, low_idx

    if h > middle+5:
        idx = high_idx
        high_idx += 1
    elif h > short+5:
        idx = mid_idx
        mid_idx += 1
    else:
        idx = low_idx
        low_idx += 1

    return des_cord[idx]
            
    
    
####################################################  좌표 구하기


a11 = posx(100, 200, 300, 0, 180, 0)  # 예시값 (x=100, y=200, z=300 등)

# 블록 간 간격
interval = 51

# src_cord
src_cord = []

for row in range(3):  # 행
    for col in range(3):  # 열
        x = a11[0] + row * interval
        y = a11[1] + col * interval
        z, a, b, c = a11[2], a11[3], a11[4], a11[5]
        src_cord.append(posx(x, y, z, a, b, c))

    
# 초기 좌표 b11
b11 = posx(400, 500, 300, 0, 180, 0)  # 예시값 (x=400, y=500, z=300 등)

# des_cord 생성
des_cord = []

for row in range(3):  # 행
    for col in range(3):  # 열
        x = b11[0] + row * interval
        y = b11[1] + col * interval
        z, a, b, c = b11[2], b11[3], b11[4], b11[5]
        des_cord.append(posx(x, y, z, a, b, c))

# 각 블록 인덱스
high_idx = 0
mid_idx = 3
low_idx = 6

# 각 블럭 높이
short = 0
middle = 0
#tall = 0

##################################################### code start


home_j = posj(0,0,90, 0,90,0)             # 초기위치
home = posx(367.3, 7.07, 204.32, 89.42, 179.98, 89.33)
movel(home)


# 정렬 시작
for src in src_cord:
    movel(home)  # 홈 포지션으로 복귀 (안정성 확보)

    # 높이 측정
    h = get_height(src)

    des = get_next_des(h)

    # 옮기기
    grab_place(src, des, upheight=50, upheightd=50)

