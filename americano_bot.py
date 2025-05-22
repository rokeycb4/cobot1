


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
        super().__init__(cnt, first, interval, row=2, col=1)

    def get_cup_cord(self):
        return self.get_last_cord()
        

class MilkShelf(Shelf):
    def __init__(self, cnt=0, first=posx(0, 0, 0, 0, 0, 0), interval=0):
        super().__init__(cnt, first, interval, row=1, col=3)

    def get_milk_cord(self):
        return self.get_last_cord()


class IceShelf(Shelf):
    def __init__(self, cnt=0, first=posx(0, 0, 0, 0, 0, 0), interval=0):
        super().__init__(cnt, first, interval, row=2, col=3)
        self.upper_stack = []
        self.build_upper_stack()

    def build_stack(self):
        """IceShelf 방향: x 감소, y 감소"""
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

############################################################# 로봇 동작 함수

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

def pour():
    """우유 잡아서 붓기"""
    src = milk_shelf.get_milk_cord()
    
    movel(src)
    grab()
    wait(0.5)
    
    amovel(pos_mmilk, vel=170, acc=170)
    wait(1)
    movelz(40, 50, 50)
    movel(pos_mmilk2)

    movel(pos_pour)
    
def milk_return():
    movelz(50) # 낮출수 있는지
    
    #movel(pos_mmilk)

    
    des = milk_shelf.get_milk_cord()
    movel(des)
    release()
    
    movel(pos_mmilk)
    
    movej(home_j)
    

    
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
            
            
def load_cup():
    """cup_load에서 컵 집어서 선반 다음 위치에 놓기"""
    cup_shelf.push()
    des = cup_shelf.get_cup_cord()
    
    movel(cup_load)
    grab_cup()
    wait(1)
    
    movej(cup_upper2)
    movel(des)
    release()
    
    
    
def load_milk():
    """src에서 우유 집어서 선반 다음 위치에 놓기"""
    milk_shelf.push()
    des = milk_shelf.get_cup_cord()
    grab_place(src, des)


    
## 결합된 레고 넣고 빼기
legoh = 19.5 #레고 들어간거 확인
    
# 레고 + 힘제어 버전
def load_ice(il):
    release()
    
    # 얼음 잡기
    movel(il)
    grab_ice()
    wait(0.5)
    
    # 레고판 다음 얼음 위치 위(upper) 이동
    ice_shelf.push()
    des = ice_shelf.get_upper_cord()
    movel(des)
    
    force_control_on(-30)
    
    # 레고 들어갈떄까지 대기
    while True:
        curr_z = get_current_posx()[0][2]
        if curr_z < legoh+1:  # 
            release()
            force_control_off()
            break
            
        
        wait(0.3)
        
    movelz(15)

    
def place_cup():
    # place cup
    movej(cup_upper)  # 중간 좌표
    
    # 다음 컵 집기
    next_cup = cup_shelf.get_cup_cord()
    cup_shelf.pop()
    movel(next_cup)
    grab_cup()
    
    # 컵위치에 놓기
    movej(cup_upper2) # cup_place가는 중간 좌표
    movej(cup_place_upper_j)
    movel(cup_place)

    release()
    wait(0.3)
    movelz(50)

    
def place_ice():
    """레고판에서 얼음 떼서 컵에 놓기"""
    src = ice_shelf.get_ice_cord()
    ice_shelf.pop()
    
    # 레고판 위로 이동
    movel(src)
    
    # 얼음 잡고 뽑기
    grab("ice")
    wait(1)
    force_control_on(15)
    movel([0,0,0,  0,3,0], 1,1, mod=1)
    wait(0.5)    
    force_control_off()
    movel([0,0,0,  0,-3,0], 1,1, mod=1)
    
    movelz(100)
    
    movej(ice_place)

    release()
    wait(0.5)

def make_latte():
    tp_log("make_latte called")
    
    if cup_shelf.cnt == 0:
        tp_log("에러: 컵이 부족합니다.")
        movel(home)
        return
    if milk_shelf.cnt == 0:
        tp_log("에러: 우유가 부족합니다.")
        movel(home)
        return
    if ice_shelf.cnt == 0:
        tp_log("에러: 얼음이 부족합니다.")
        movel(home)
        return

    movej(posj(0, 0, 90, 0, 90, 0))  # 홈 이동
    release()

    try:
        place_cup()
        pour()
        milk_return()
        place_ice()
        grab_shake()
        serve()
    except Exception as e:
        tp_log("make_latte 에러: {}".format(e))
        movel(home)


def make_americano():
    tp_log("make_americano called")

    if cup_shelf.cnt == 0:
        tp_log("에러: 컵이 부족합니다.")
        movel(home)
        return
    if ice_shelf.cnt == 0:
        tp_log("에러: 얼음이 부족합니다.")
        movel(home)
        return

    movej(posj(0, 0, 90, 0, 90, 0))  # 홈 이동
    release()

    try:
        place_cup()
        place_ice()
        grab_shake()
        serve()
    except Exception as e:
        tp_log("make_americano 에러: {}".format(e))
        movel(home)



################################################ code start


set_va(100, 100, 140, 140)  # 속도 가속도 초기화

home_j = posj(0,0,90, 0,90,0)
home = posx(367.31, 7.07, 204.32, 88.13, 179.98, 88.03)

cup_place = posx(418.21, -81, 68.18, 154.1, 180, 64.92)
cup_place_j = posj(-11.9, 11.47, 98.88, -0.04, 69.65, -100.97)

# 바군거
cup_place = posx(424.4, -76.95, 58.32, 10.81, -179.95, -79.65)
cup_place_j = posj(-11.19, 12.71, 98.97, -0.06, 68.36, -101.54)
       
cup_place_upper = posx(418.21, -81, 75, 154.1, 180, 64.92)   # cup_place 보다다 살짝 위
cup_place_upper_j = posj(-11.9, 11.14, 98.15, -0.04, 70.71, -100.97)     
               
                                                     #컵 놓는 위치
#ice_place = trans(cup_place, [0,0,75, 0,0,0], DR_BASE, DR_BASE)    #얼음 놓는 위치(컵 위치보다 살짝 위)
ice_place = posj(-11.64, 9.1, 91.78, -0.04, 79.12, -100.72)

#ice_place = posx([i for i in cup_place])
shake_place = posx(300, 100, 62, 128.1, -178, 140.41)                       #shake할 때 컵 다시 잡는 위치
cord_final = posx(306.45, -378.25, 131.33, 112.06, -179.99, 113.06)      #최종 위치(서빙 위치)
cup_upper = posj(35.59, 2.74, 74.23, -0.79, 103.82, 88.03)  #바꾼거
cup_upper2 = posj(51.64, 20.86, 41.77, -0.93, 116.2, -123.24)



# 선반 좌표 (클래스 기반)
cup_first = posx(309.16, 481.47, 250.6, 67.32, -178.93, -112.44)
cup_first = posx(239.49, 474.69, 240.93, 79.66, 180, 88.03) #바꾼거
ice_first = posx(683.57, 76.19, 19.5, 129.77, 178.08, 41.15)
ice_first = posx(681, 75, 19.5, 129.77, 178.08, 41.15)


milk_first = posx(324.85, 529.94, 47.7, 95.53, 105.88, -87.2)

# 우유 따르는 중간포즈, 포즈
pos_mmilk = posx(361.72, 297.42, 175.46, 81.12, 102.16, -90.42)
pos_mmilk_j = posj(-7.14, 11.96, 129.86, 83.84, 79.28, 128.5)



pos_mmilk2 = posx(462.24, -144.77, 176.01, 32, 95.81, -86.05)
pos_pour = posx(455.1, -99.27, 142.4, 40.23, 102.38, 159.51)


# 선반 객체 생성
cup_shelf = CupShelf(cnt = 2, first=cup_first, interval=120)
ice_shelf = IceShelf(cnt = 4, first=ice_first, interval=80)
milk_shelf = MilkShelf(cnt = 1, first=milk_first, interval=80)


 # (적재할때) 잡는 위치
cup_load = posx(275.37, -82, 58.32, 85.22, -174.48, -6.79)
ice_load = posx(274.88, -77.32, 16.27, 13.79, -180, 14.63)
ice_load_j = posj(-17.09, -4.3, 124.83, 0.01, 59.47, -16.15)
ice_load2 = posx(274.88, -112.32, 16.27, 13.79, -180, 14.63)

milk_load = home


def main():
    tp_log("main called")
    movej(posj(0,0,90, 0,90,0)) # 홈 이동
    release()
          
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
