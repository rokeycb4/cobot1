def set_va(vel, acc):
    """속도 가속도 초기화"""
    set_velj(vel)
    set_accj(acc)
    set_velx(vel)
    set_accx(acc)
    
def grab():
    set_digital_output(1,0)
    set_digital_output(2,1)
    wait(1)

def release():
    set_digital_output(2,0)
    set_digital_output(1,1)
    
    
def force_control_on():
    k_d = [500.0,500.0,500.0,  200.0,200.0,200.0]
    task_compliance_ctrl(k_d)
    f_d = [0,0,-20,0.0,0.0,0.0]
    f_dir = [0,0,1,0,0,0]
    set_desired_force(f_d,f_dir)

def force_control_off():
    release_force()
    release_compliance_ctrl()
    
# src에서 잡아서 des에 놓기
def grab_place(src, des):

    upheight = 100

    height = get_current_posx()[0][2] - src[2]

    src[2] = get_current_posx()[0][2]
    movel(src, vv, aa)
    
    # 내려서 잡고 올리기
    movel([0,0,-height, 0,0,0], mod=1)
    grab(obj)
    wait(0.5)
    movel([0,0,upheight, 0,0,0], mod=1)
    
    #내려갈값 구하기
    height = get_current_posx()[0][2] - des[2]
    
     # z값 유지하면서 이동
    des[2] = get_current_posx()[0][2]
    movel(des)
    wait(0.5)
    
    # 내리고 놓고 올리기
    movelz(-height)
    
    
###################################################### code start
set_va(80,80)



home = posj(0,0,90, 0,90,0)
movej(home)

grab_place(p1,p2)


















