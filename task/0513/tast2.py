
set_digital_output(2,OFF)
set_digital_output(1,OFF)

set_digital_output(2,OFF)
set_digital_output(1,ON)
a= Global_a
movel(a)
wait(3)
set_digital_output(2,ON)
set_digital_output(1,OFF)


k_d = [300.0 , 300.0, 300.0, 200.0, 200.0, 200.0]
task_compliance_ctrl(k_d)

force_desired = 20.0
f_d = [0.0 , 0.0 , -force_desired,0.0,0.0,0.0]
f_dir = [0, 0, 1, 0, 0, 0]
set_desired_force(f_d,f_dir)

while True:
	trq_ext = get_external_torque()
	#tp_popup("{}".format(trq_ext))
	
	if trq_ext[2] < -5:
		d = get_current_posx()[0]
		z = d[2]
		if z > 45 : 
			dele = [0,10,0,0,0,0]
			x2 = trans(d,dele,DR_BASE,DR_BASE)
			movel(x2,30,30)
		elif z < 45:
			release_force()
			release_compliance_ctrl()
			set_digital_output(2,OFF)
			set_digital_output(1,ON)
			break
aa= get_current_posx()[0]
aa[2] = aa[2] + 100
movel(aa, 60 , 60)

#set_digital_output(2,ON)
#set_digital_output(1,OFF)
#wait(1)
