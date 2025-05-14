def grab():
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

    # z값 유지하고 이동
    curr = get_current_posx()[0]
    src[2] = curr[2]
    movel(src, vv, aa)
    
    # 내려서 잡고 올리기
    transz(-height)
    grab()
    wait(0.5)
    transz(height)
    
     # z값 유지하고 이동
    des[2] = curr[2]
    movel(des, vv, aa)
    wait(0.5)
    
    # 내리고 놓고 올리기
    transz(-height)
    release()
    transz(height)
    
home = posj(0,0,90, 0,90,0)
movej(home, 50, 50)

# 기본 속도, 가속도
vv, aa = 80, 80

p1 = posx(150, 20, 100, 45, 180, 45)
p2 = posx(300, 100, 100, 45, 180, 45)

func1(p1,p2)

    
    
    
    
