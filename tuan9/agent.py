from utility import * 
class Agent:
    def __init__(self, id:int, init_pose:np.ndarray, visual:Axes, robot_radius:float=0.2):
        self.id = id
        self.global_pose: np.ndarray = init_pose.copy()
        self.radius = robot_radius

        self.agent_visual: Circle = Circle((self.global_pose[0], self.global_pose[1]), radius= self.radius, color='blue')
        visual.add_patch(self.agent_visual)

        self.agent_text: Text = visual.text(self.global_pose[0], self.global_pose[1], str(self.id), c='black', size=5.0)

        self.vel:np.ndarray = np.zeros(2)

    