import math

# A 위치 (입력 좌표)
A = [AX, AY, AZ, ARX, ARY, ARZ]  # <- 여기에 실제 좌표 넣으세요
# B 위치 (분류 대상 좌표)
B = [BX, BY, BZ, BRX, BRY, BRZ]  # <- 여기에 실제 좌표 넣으세요

# 간격 (m 단위로 51mm)
spacing = 0.051

# 침하량 기준 (단위: m)
dz1 = 0.01
dz2 = 0.02

# 그리퍼 제어 함수
def gripper_close():
    set_digital_output(1, OFF)
    set_digital_output(2, ON)

def gripper_open():
    set_digital_output(1, ON)
    set_digital_output(2, OFF)

# 안전 상승 높이
def safe_z(z): return z + 0.1

# 3x3 A 파레트 순회
for row in range(3):
    for col in range(3):
        # 현재 물건 위치 (A 파레트)
        item_pos = [
            A[0] + spacing * col,
            A[1] + spacing * row,
            A[2],
            A[3], A[4], A[5]
        ]

        # 1. 접근: 상단으로 이동
        approach_pos = [item_pos[0], item_pos[1], safe_z(item_pos[2]), item_pos[3], item_pos[4], item_pos[5]]
        movel(approach_pos, vel=50)

        # 2. 순응 제어 모드 ON (Z축만)
        set_compliance_mode(mode=ON, dof=[0, 0, 1, 0, 0, 0])
        sync()

        # 3. 천천히 하강 (최대 100 스텝)
        start_z = approach_pos[2]
        end_z = start_z
        for i in range(100):
            z = start_z - (i * 0.001)
            movel([item_pos[0], item_pos[1], z, item_pos[3], item_pos[4], item_pos[5]], vel=2)
            force = get_tool_force()
            if force[2] > 10.0:  # 접촉 감지
                break
        # 4. 최종 위치 기록
        pose = get_current_pose()
        end_z = pose[2]
        delta_z = start_z - end_z

        # 5. 순응 제어 해제
        set_compliance_mode(mode=OFF)
        sync()

        # 6. 물체 집기
        gripper_close()
        wait(1.0)

        # 7. 상승
        movel([item_pos[0], item_pos[1], safe_z(item_pos[2]), item_pos[3], item_pos[4], item_pos[5]], vel=50)

        # 8. 분류 기준 결정
        if delta_z > dz2:
            dest_row = 2
        elif delta_z > dz1:
            dest_row = 1
        else:
            dest_row = 0

        # 9. B 파레트 위치 계산
        dest_pos = [
            B[0] + spacing * col,
            B[1] + spacing * dest_row,
            B[2],
            B[3], B[4], B[5]
        ]

        # 10. 이동 → 배치 위치 상단
        movel([dest_pos[0], dest_pos[1], safe_z(dest_pos[2]), dest_pos[3], dest_pos[4], dest_pos[5]], vel=50)
        movel(dest_pos, vel=10)

        # 11. 물체 놓기
        gripper_open()
        wait(1.0)

        # 12. 상승 → 다음 물건으로
        movel([dest_pos[0], dest_pos[1], safe_z(dest_pos[2]), dest_pos[3], dest_pos[4], dest_pos[5]], vel=50)
