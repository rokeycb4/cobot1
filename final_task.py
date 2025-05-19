

def set_va(jvel, jacc,xvel, xacc):
    """속도 가속도 초기화"""
    set_velj(jvel)
    set_accj(jacc)
    set_velx(xvel)
    set_accx(xacc)

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
    wait(1)

def grab_ice():
    set_digital_output(1,1)
    set_digital_output(2,1)
    wait(1)

def release():
    set_digital_output(2,0)
    set_digital_output(1,1)
    
def movelz(z):
    """z축 상대좌표 이동"""
    movel([0,0,z,  0,0,0], 60, 60, mod=1)     

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
    
    movel(cord3)
    grab_cup()
    movelz(50)
    
    #p1 = posx(457.67, 16.53, 167.47, 13.12, -176.54, 2.42)
    #movel(p1,60,60)
    
    #tp_log('{}'.format(home))
    movel(home)
    
    amove_periodic([0,0,0,30,0,90],3.0 ,0.02 ,3,DR_TOOL)
    wait(10)
    amove_periodic([0,0,30,0,0,0],1.0 ,0.02 ,2,DR_TOOL)
    wait(3)
    
    # 6축 회전(다른 모션으로 수정 필요)
    #movel([0,0,0,  0,0,60], vv, aa, mod=1)
    #movel([0,0,0,  0,0,-60], vv, aa, mod=1)
    #wait(0.5)
    
def serve():
    """서빙 위치로 이동후 놓기"""
    tp_log("serve() called")
    
    movel(cord_final)
    
    k_d = [3000,3000,3000,200,200,200]
    task_compliance_ctrl(k_d)
    while True:
        tk = get_tool_force()
        #tp_popup("{}".format(tk))
        if tk[2] < -1 :
            release()
            movel(home, 30, 30)
            #set_digital_output(2,0)
       

################################################ code start

set_va(100, 100, 100, 100)  # 속도 가속도 초기화
    
home_j = posj(0,0,90, 0,90,0)             # 초기위치
home = posx(367.3, 7.07, 204.32, 89.42, 179.98, 89.33)



cord1 = posx(300, 100, 57, 128.1, -178, 140.41)                          #컵 놓는 위치
cord2 = trans(cord1, [0,0,50, 0,0,0], DR_BASE, DR_BASE)             #얼음 놓는 위치
cord3 = posx(300, 100, 62, 128.1, -178, 140.41)   #shake할 때 컵 다시 잡는 위치
cord_final = posx(306.45, -378.25, 131.33, 112.06, -179.99, 113.06)#최종 위치

cup11 = posx(544.3, -286.47, 62.61, 148.1, 180, 147.59)
cup23 = posx(659.79, -91.69, 61.32, 96.38, -178.13, 95.67)

ice11 = posx(557.67, 79.51, 15, 90.21, -179.41, 90.86)
ice23 = posx(696.42, 260.37, 15, 75.4, 177.23, 75.09)

def main():
    tp_log("main called")

    movej(home_j)
    release()
    grab_place(cup11, cord1, 50, 50, "cup")
    grab_place(ice11, cord2, 100,20, "ice")
    grab_shake()
    serve()
    
    #movej(home_j, vv, aa)

    
#if __name__ == "__main__":
main()
