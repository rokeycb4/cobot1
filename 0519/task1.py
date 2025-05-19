def set_va(vel, acc):
    """속도 가속도 초기화"""
    set_velj(vel)
    set_accj(acc)
    set_velx(vel)
    set_accx(acc)
    
def grab():
    set_digital_output(1,1)
    set_digital_output(2,1)
    wait(1)
    
def release():
    set_digital_output(2,0)
    set_digital_output(1,1)


def force_control_on(force_z):
    k_d = [500.0,500.0,500.0,  200.0,200.0,200.0]
    task_compliance_ctrl(k_d)
    f_d = [0,0,force_z,0.0,0.0,0.0]
    f_dir = [0,0,1,0,0,0]
    set_desired_force(f_d,f_dir)

def force_control_off():
    release_force()
    release_compliance_ctrl()
    
def movelz(z):
    """z축 상대좌표 이동"""
    movel([0,0,z,  0,0,0], 30, 30, mod=1)  
    
def grab_place(src, des):

    
    upheight = 100

    height = get_current_posx()[0][2] - src[2]

    src_ = trans(src,[0,0,0, 0,0,0], DR_BASE, DR_BASE)
    src_[2] = get_current_posx()[0][2]
    movel(src_)
    
    # 내려서 잡고 올리기
    movel([0,0,-height, 0,0,0], mod=1)
    grab()
    wait(0.5)
    movel([0,0,upheight, 0,0,0], mod=1)
    
    #내려갈값 구하기
    height = get_current_posx()[0][2] - des[2]
    
     # z값 유지하면서 이동
    des_ = trans(des,[0,0,0, 0,0,0], DR_BASE, DR_BASE)
    des_[2] = get_current_posx()[0][2]
    movel(des_)
    wait(0.5)
    
    # 내리고 놓고 올리기
    movelz(-height)

def pulloff():
    """레고 뽑아서 들기"""
    grab()
    wait(1)
    force_control_on(10)
    
    movel([0,0,0,  0,8,0], 1,1, mod=1)
    wait(1)
    
    force_control_off()
    movel([0,0,0,  0,-8,0], 1,1, mod=1)

    

def pullin(pos1, pos2, h):
    """레고 끼우기"""
    grab_place(pos1,pos2)
    
    force_control_on(-20)
    while True:
        t = get_tool_force()
        if t[2] > 20:
            z = get_current_posx()[0][2]
            if z < h:
                force_control_off()
                break
    release()            
    #movelz(30)
    wait(1)
               

    
    
#################################################




set_va(80,80)

p = posj(0,0,90,0,90,0)
movej(p,30,30)
wait(0.5)

release()

p1 = posx(422.71, -228.1, 11.43, 152.36, 180, 151.34)   #시작 위치
p2 = posx(518.75, 21.5, 16.87, 0.65, -179.96, -0.51)     #레고1 (힘제어 시작위치니까 살짝 위에 있어야됨)
p3 = posx(518.75, 21.5, 50, 0.65, -179.96, -0.51)            #레고2



pullin(p1, p2, 15)
pullin(p1, p3, 33)
pulloff()

    
