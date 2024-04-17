from factory_map import *

factory_map = FactoryMap()

factory_map.updateFactoryMap()
factory_map.visualizeFactoryMap()
factory_map.visualizePointMap()
# factory_map.visualizeGraphFactoryMap()
# folder = "RDS/data/100x50"
# np.savetxt(folder + "/map.txt", np.array([factory_map.factory_center_x, factory_map.factory_center_y, 
#                                         factory_map.factory_length, factory_map.factory_width]), fmt="%.2f")
# factory_map.save_line_data(folder)
# factory_map.save_zone_data(folder)
# factory_map.save_point_data(folder)
plt.show()