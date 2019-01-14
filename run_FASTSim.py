import FASTSim
import os
import time
print('Current Dir : ' + os.getcwd())

#os.chdir('D://UCI//Research APEP//fastsim-python-2018b//fastsim-2018//src')
os.chdir('D://UCI//Research APEP//fastsim-python-2018b//fastsim-2018b//src')
print('Current Dir : ' + os.getcwd())

cyc = FASTSim.get_standard_cycle('udds')
veh = FASTSim.get_veh(10)
print(veh['maxMotorKw'])
start = time.time()
# output_sub = FASTSim.sim_drive_sub(cyc, veh,0.7854515)
output_sub = FASTSim.sim_drive_sub(cyc, veh,0.7)
output = FASTSim.sim_drive(cyc, veh)
end = time.time()
print('TIME END : ' + str((end - start)))
for i in output_sub:
    print(i)
print('\n\n')


print(type(output_sub))

for i in output_sub:
    print (i + '\t' +  str(output_sub[i]))

print(str('OUTPUT : ' + str(output['mpgge'])))
print(str('OUTPUT SUB : ' + str(output_sub['valCombMpgge'])))
# def main():
#     print('WOW');
# if __name__ == '__main__':
#     main()
#     print('run_fastsim with DOE')
