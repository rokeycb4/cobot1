


############################################################# 선반스택

class Shelf:
    def __init__(self, cnt=0, first=posx(0, 0, 0, 0, 0, 0), interval=0, row=1, col=1):
        self.cnt = cnt
        self.first = first
        self.interval = interval
        self.stack = []
        self.row = row
        self.col = col
        self.build_stack()

    def build_stack(self):
        """기본 방향: x 증가, y 감소"""
        self.stack = []
        for i in range(self.row):
            for j in range(self.col):
                x = self.first[0] + i * self.interval
                y = self.first[1] - j * self.interval
                p = posx(x, y, self.first[2], self.first[3], self.first[4], self.first[5])
                self.stack.append(p)

    def get_last_cord(self):
        if self.cnt == 0:
            tp_log("경고: 아이템이 없습니다.")
            return None
        return self.stack[self.cnt - 1]

    def push(self):
        if self.cnt >= len(self.stack):
            tp_log("경고: 선반이 가득 찼습니다.")
            return
        self.cnt += 1

    def pop(self):
        if self.cnt <= 0:
            tp_log("경고: 꺼낼 아이템이 없습니다.")
            return
        self.cnt -= 1


class CupShelf(Shelf):
    def __init__(self, cnt=0, first=posx(0, 0, 0, 0, 0, 0), interval=0):
        super().__init__(cnt, first, interval, row=2, col=3)

    def get_cup_cord(self):
        return self.get_last_cord()
        

class MilkShelf(Shelf):
    def __init__(self, cnt=0, first=posx(0, 0, 0, 0, 0, 0), interval=0):
        super().__init__(cnt, first, interval, row=1, col=3)

    def get_milk_cord(self):
        return self.get_last_cord()


class IceShelf2(Shelf):
    def __init__(self, cnt=0, first=posx(0, 0, 0, 0, 0, 0), interval=0):
        super().__init__(cnt, first, interval, row=2, col=3)
        self.upper_stack = []
        self.build_upper_stack()

    def build_stack(self):
        """IceShelf2 방향: x 감소, y 감소"""
        self.stack = []
        for i in range(self.row):
            for j in range(self.col):
                x = self.first[0] - i * self.interval
                y = self.first[1] - j * self.interval
                p = posx(x, y, self.first[2], self.first[3], self.first[4], self.first[5])
                self.stack.append(p)

    def build_upper_stack(self):
        """stack과 동일한 평면 배치 + z값만 40 증가"""
        self.upper_stack = []
        for i in range(self.row):
            for j in range(self.col):
                x = self.first[0] - i * self.interval
                y = self.first[1] - j * self.interval
                z = self.first[2] + 40
                p = posx(x, y, z, self.first[3], self.first[4], self.first[5])
                self.upper_stack.append(p)

    def get_ice_cord(self):
        return self.get_last_cord()

    def get_upper_cord(self):
        if self.cnt == 0:
            tp_log("경고: upper_stack에 아이템이 없습니다.")
            return None
        return self.upper_stack[self.cnt - 1]

############################################################# 로봇스택

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
        tp_log("wrong object")

    
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
    
def movelz(z, vel_=100, acc_=100):
    """z축 상대좌표 이동"""
    movel([0,0,z,  0,0,0], vel=vel_, acc=acc_ ,mod=1)     

def force_control_on(force_z):
    """ z방향 힘제어"""
    k_d = [500.0,500.0,500.0,  200.0,200.0,200.0]
    task_compliance_ctrl(k_d)
    f_d = [0,0,force_z,0.0,0.0,0.0]
    f_dir = [0,0,1,0,0,0]
    set_desired_force(f_d,f_dir)

def force_control_off():
    """순응제어 해제, 힘제어 해제"""
    release_force()
    release_compliance_ctrl()
    
    
# src에서 잡아서 des에 놓기
def grab_place(src, des, upheight, upheightd, obj='cup'):
    """upheight: 잡고 올릴 높이, upheightd: 놓고 올릴 높이 """
    
    #내려갈값 구하기
    height = get_current_posx()[0][2] - src[2]
    
    ## z값 유지하면서 이동
    #src_ = trans(src,[0,0,0, 0,0,0], DR_BASE, DR_BASE)
    #src_[2] = get_current_posx()[0][2]
    #movel(src_)
    
    # trans안되는 환경일 떄
    src_ = posx([i for i in src])
    src_[2] = get_current_posx()[0][2]
    movel(src_)
    
    # 내려서 잡고 올리기
    movel([0,0,-height, 0,0,0], mod=1)
    grab(obj)
    wait(0.5)
    movel([0,0,upheight, 0,0,0], mod=1)
    
    #내려갈값 구하기
    height = get_current_posx()[0][2] - des[2]
    
     ## z값 유지하면서 이동
    #des_ = trans(des,[0,0,0, 0,0,0], DR_BASE, DR_BASE)
    #des_[2] = get_current_posx()[0][2]
    #movel(des_)
    
    # trans안되는 환경일 떄
    des_ = posx([i for i in des])
    des_[2] = get_current_posx()[0][2]
    movel(des_)
    
    # 내리고 놓고 올리기
    movelz(-height)
    release()
    wait(0.2)
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
    movel(cup_place)
    grab_cup()
    movelz(50)
    movel(home)
    amove_periodic([0,0,0,30,0,90],3.0 ,0.02 ,1,DR_TOOL)
    wait(4.5)
    amove_periodic([0,0,30,0,0,0],1.0 ,0.02 ,2,DR_TOOL)
    wait(3)

def pour(src):
    """우유 잡아서 붓기"""
    movel(src)
    grab()
    wait(0.5)
    
    movel(pos_mmilk)
    movelz(80)
    movel(pos_mmilk2)

    movel(pos_pour)
    
def milk_return():
    movelz(80) # 낮출수 있는지
    movel(pos_mmilk)
    des = milk_shelf.get_milk_cord()
    
    movel(des)
    release()
    
    movel(pos_mmilk)
    
    movej(home_j)

def throw_away():
    """컵 쓰레기통에 버리기"""
    movel(trashcan_place)
    release()
    wait(0.5)
    
    
def serve():
    """서빙 위치로 이동후 놓기"""
    tp_log("serve() called")
    
    movel(cord_final)
    
    # 컵뽑으면 집게 열고 홈 위치로 이동
    k_d = [3000,3000,3000,200,200,200]
    task_compliance_ctrl(k_d)
    while True:
        tk = get_tool_force()
        if tk[2] < -1 :
            release()
            movel(home)
            break
            
            
def load_cup(src, cup_shelf):
    """src에서 컵 집어서 선반 다음 위치에 놓기"""
    cup_shelf.push()
    des = cup_shelf.get_cup_cord()
    grab_place(src, des)
    
    
def load_milk(src, milk_shelf):
    """src에서 우유 집어서 선반 다음 위치에 놓기"""
    milk_shelf.push()
    des = milk_shelf.get_cup_cord()
    grab_place(src, des)


    
## 결합된 레고 넣고 빼기
legoh = None #레고 들어간거 확인
    
# 레고 + 힘제어 버전
def load_ice2():
    release()
    
    # 얼음 잡기
    movel(ice_load)
    grab_ice()
    
    # 레고판 다음 얼음 위치 위(upper) 이동
    ice_shelf2.push()
    des = ice_shelf2.get_upper_cord()
    movel(des)
    
    force_control_on(-20)
    
    # 레고 들어갈떄까지 대기
    while True:
        curr_z = get_current_posx()[0][2]
        if curr_z < legoh+3:  # 
            release()
            force_control_off()
            
        
        wait(0.2)
            
def place_ice():
    """레고판에서 얼음 떼서 컵에 놓기"""
    src = ice_shelf2.get_ice_cord()
    #ice_shelf2.pop()
    
    # 레고판 위로 이동
    movel(src)
    
    # 얼음 잡고 뽑기
    grab("ice")
    wait(1)
    force_control_on(10)
    movel([0,0,0,  0,3,0], 1,1, mod=1)
    wait(0.5)    
    force_control_off()
    movel([0,0,0,  0,-3,0], 1,1, mod=1)
    
    movelz(100)
    
    movej(ice_place)

    release()
    wait(0.2)

def make_americano():
    tp_log("make_americano called")
    movej(posj(0,0,90, 0,90,0)) # 홈 이동
    release()
    
    # place cup
    next_cup = cup_shelf.get_cup_cord()
    #cup_shelf.pop()
    movel(cup_upper)
    grab_place(next_cup, cup_place, 50, 50, "cup")
    
    # place ice
    place_ice()
    #ice_shelf2.pop()
    
    # shake
    grab_shake()
    serve()    
    
    
def make_latte():
    tp_log("make_latte called")
    movej(posj(0,0,90, 0,90,0)) # 홈 이동
    release()
    
    # place cup
    next_cup = cup_shelf.get_cup_cord()
    #cup_shelf.pop()
    movel(cup_upper)
    grab_place(next_cup, cup_place, 50, 50, "cup")
    
    # place milk
    next_milk = milk_shelf.get_milk_cord()
    pour(next_milk)
    milk_return()
            
    # place ice
    place_ice()
    #ice_shelf2.pop()
    
    # shake
    grab_shake()
    serve()


################################################ code start


set_va(100, 100, 140, 140)  # 속도 가속도 초기화

home_j = posj(0,0,90, 0,90,0)
home = posx(367.31, 7.07, 204.32, 88.13, 179.98, 88.03)

cup_place = posx(418.21, -81, 68.18, 154.1, 180, 64.92)                                                       #컵 놓는 위치
#ice_place = trans(cup_place, [0,0,75, 0,0,0], DR_BASE, DR_BASE)    #얼음 놓는 위치(컵 위치보다 살짝 위)
ice_place = posj(-11.64, 9.1, 91.78, -0.04, 79.12, -100.72)

#ice_place = posx([i for i in cup_place])
shake_place = posx(300, 100, 62, 128.1, -178, 140.41)                       #shake할 때 컵 다시 잡는 위치
cord_final = posx(306.45, -378.25, 131.33, 112.06, -179.99, 113.06)      #최종 위치(서빙 위치)
cup_upper = posx(309.74, 453.92, 251.67, 56.44, -179.99, -123.17)


# 선반 좌표 (클래스 기반)
cup_first = posx(309.16, 481.47, 250.6, 67.32, -178.93, -112.44) # 수정필요
ice_first2 = posx(683.57, 76.19, 19.5, 129.77, 178.08, 41.15)
milk_first = posx(324.85, 529.94, 47.7, 95.53, 105.88, -87.2)

# 우유 따르는 중간포즈, 포즈
pos_mmilk = posx(361.72, 297.42, 175.46, 81.12, 102.16, -90.42)
pos_mmilk2 = posx(462.24, -144.77, 176.01, 32, 95.81, -86.05)
pos_pour = posx(455.1, -99.27, 142.4, 40.23, 102.38, 159.51)

# 선반 객체 생성
cup_shelf = CupShelf(cnt = 1, first=cup_first, interval=80)
ice_shelf2 = IceShelf2(cnt = 1, first=ice_first2, interval=80)  # 결합된 레고
milk_shelf = MilkShelf(cnt = 1, first=milk_first, interval=80)


 # (적재할때) 잡는 위치
cup_load = home
ice_load = home
milk_load = home


def main():
    tp_log("main called")
    movej(posj(0,0,90, 0,90,0)) # 홈 이동
    release()
    
    make_latte()
      
    force_control_on(0)
    while True:
        tk = get_tool_force()
        if tk[0] > 5:
            force_control_off()
            make_americano()
        if tk[0] < -5:
            force_control_off()
            make_latte()
            
    
#if __name__ == "__main__":
main()
