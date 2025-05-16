
def grab():
    set_digital_output(1,0)
    set_digital_output(2,1)

def grab_ice():
    set_digital_output(1,0)
    set_digital_output(2,1)

def release():
    set_digital_output(1,1)
    set_digital_output(2,0)
    
def transz(z):
    """z축 상대좌표 이동"""
    pos = get_current_posx()[0]
    res = trans(pos, [0,0,z,0,0,0], DR_BASE, DR_BASE)
    movel(res, 30, 30) 

def trans_rel(pos, x, y,z):
    """상대좌표로 이동"""
    res = trans(pos, [x,y,z,0,0,0], DR_BASE, DR_BASE)
    movel(res, 30, 30) 
    
    
# src에서 잡아서 des에 놓기
def func1(src, des):

    #잡고 얼마나 들지
    height = 100

    # z값 유지하면서 이동
    src[2] = get_current_posx()[0][2]
    movel(src, vv, aa)
    
    # 내려서 잡고 올리기
    transz(-height)
    grab()
    wait(0.5)
    transz(height)
    
     # z값 유지하면서 이동
    des[2] = get_current_posx()[0][2]
    movel(des, vv, aa)
    wait(0.5)
    
    # 내리고 놓고 올리기
    transz(-height)
    release()
    transz(height)
    
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
    
################################################ code start
    
home = posj(0,0,90, 0,90,0)
movej(home, 50, 50)

# 기본 속도, 가속도
vv, aa = 80, 80



def main():
    pass
    







if __name__ == "__main__":
    main()
    
    
