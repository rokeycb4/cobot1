

def grab(obj='cup'):
    if obj == 'cup':
        grab_cup()
    elif obj == 'ice':
        grab_ice()
    else:
        print("wrong object")

    
def grab_cup():
    set_digital_output(1,0)
    set_digital_output(2,1)
    wait(0.2)

def grab_ice():
    set_digital_output(1,1)
    set_digital_output(2,1)
    wait(0.2)

def release():
    set_digital_output(2,0)
    set_digital_output(1,1)
    
def movelz(z):
    """z축 상대좌표 이동"""
    movel([0,0,z,  0,0,0], 30, 30, mod=1)     

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
def grab_place(src, des, obj='CUP'):

    upheight = 100

    #내려갈값 구하기
    height = get_current_posx()[0][2] - src[2]

    # z값 유지하면서 이동
    src[2] = get_current_posx()[0][2]
    movel(src, vv, aa)
    
    # 내려서 잡고 올리기
    movel([0,0,-height, 0,0,0], vv, aa, mod=1)
    grab()
    wait(0.5)
    movel([0,0,upheight, 0,0,0], vv, aa, mod=1)
    
    #내려갈값 구하기
    height = get_current_posx()[0][2] - des[2]
    
     # z값 유지하면서 이동
    des[2] = get_current_posx()[0][2]
    movel(des, vv, aa)
    wait(0.5)
    
    # 내리고 놓고 올리기
    movelz(-height)
    release()
    movelz(upheight)
    

def get_cup_cord():
    """다음 컵 위치 반환"""
    res = posx(573.4, -225.6, 68.39, 128.1, -178, 140.41)      # 임시값
    return  res
    
    
def get_ice_cord():
    """다음 얼음 위치 반환"""
    res = posx(574.28, 220.44, 25.62, 94.08, 177.04, 96.26)      # 임시값
    return  res
    
def grab_shake():
    """컵 집어서 흔들기"""
    tp_log("grab_shake() called")
    
    movel(cord1, vv, aa)
    grab_cup()
    movelz(10)
    
    # 6축 회전(다른 모션으로 수정 필요)
    movel([0,0,0,  0,0,60], vv, aa, mod=1)
    movel([0,0,0,  0,0,-60], vv, aa, mod=1)
    wait(0.5)
    
def serve():
    """서빙 위치로 이동후 놓기"""
    tp_log("serve() called")
    
    movel(cord_final, vv, aa)
    release()
    movelz(50)
    

################################################ code start
    
home_j = posj(0,0,90, 0,90,0)             # 초기위치
home = posx(368, 6.25, 425, 19.57, 180, 19.57)


cord1 = posx(300, 100, 68.39, 128.1, -178, 140.41)                          #컵 놓는 위치
cord2 = trans(cord1, [0,0,20, 0,0,0], DR_BASE, DR_BASE)             #얼음 놓는 위치
cord_final = trans(cord1, [0,-50,0, 0,0,0], DR_BASE, DR_BASE)      #최종 위치

#cord1 = posx(200, 30, 505,  0, 0, 0)   # 처음 컵 놓는 위치
#cord2 = posx(600, 30, 505,  0, 0, 0)   # 처음 컵 놓는 위치


# 기본 속도, 가속도
vv, aa = 120, 120

def main():
    tp_log("main called")

    movej(home_j, vv, aa)
    release()
    grab_place(get_cup_cord(), cord1)
    grab_place(get_ice_cord(), cord2)
    grab_shake()
    serve()
    
    movej(home_j, vv, aa)

    
#if __name__ == "__main__":
if True:
    main()
