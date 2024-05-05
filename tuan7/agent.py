from utility import *
class Agent:
    def __init__(self, id: int, init_pose: np.ndarray, coverage_range: float,
                 max_velocity: float, visual: Axes, robot_radius: float = 0.2):
        self.id = id
        self.global_pose: np.ndarray = init_pose.copy()
        self.local_pose: np.ndarray = np.zeros(2)
        self.theta: float = 0.0
        self.max_vel = max_velocity
        self.visual: Axes = visual
        self.radius = robot_radius
        self.coverage_range: float = coverage_range

        self.agent_visual: Circle = Circle((self.global_pose[0], self.global_pose[1]), radius= self.radius, color= agent_color)
        visual.add_patch(self.agent_visual)
        self.agent_text: Text = visual.text(self.global_pose[0], self.global_pose[1], str(self.id), c='black', size=5.0)
        self.path_x = []
        self.path_y = []
        self.vel:np.ndarray = np.zeros(2)

    def run(self):
        self.global_pose[0] = self.global_pose[0] + self.vel[0] * 0.1
        self.global_pose[1] = self.global_pose[1] + self.vel[1] * 0.1
        self.theta = math.atan2(self.vel[1], self.vel[0])

    def visualize(self):
        self.path_x.append(self.global_pose[0])
        self.path_y.append(self.global_pose[1])
        self.agent_visual.set_center((self.global_pose[0], self.global_pose[1]))
        self.agent_text.set_x(self.global_pose[0])
        self.agent_text.set_y(self.global_pose[1])
        path_length = 20

    def limitVelocity(self, vel:np.ndarray):
        speed = math.hypot(vel[0], vel[1])
        if speed > self.max_vel:
            limited_speed = (vel / speed) * self.max_vel
            return limited_speed
        return vel