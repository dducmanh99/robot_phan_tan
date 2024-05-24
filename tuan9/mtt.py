from utility import *
from agent import Agent
class MTT:
    def __init__(self,goals:np.ndarray, num_agents:int, agent_first_pos:np.ndarray, agents_in_row:int,
                 agents_dis:float, map_visual:Axes, max_vel:float=0.2):
        self.goals = goals
        self.num_agents=num_agents
        self.agent_first_pos=agent_first_pos
        self.map_visual:Axes = map_visual
        agent_in_cols: int = int(num_agents/ agents_in_row)
        self.agents_dis=agents_dis
        self.agents: List[Agent] = []
        for i in range(agents_in_row):
            for j in range(agent_in_cols):
                x = agent_first_pos[0] + (5+i*agents_dis)*math.cos(j*2*math.pi/agent_in_cols) 
                y = agent_first_pos[1] + (5+i*agents_dis)*math.sin(j*2*math.pi/agent_in_cols) 
                id = (i*agent_in_cols + j)
                self.agents.append(Agent(id=id,init_pos=np.array([x,y]),visual=self.map_visual))
        self.goal_range:float = 4.0
        self.avoidance_range:float = 0.8
        self.goal_gain: float = 0.02
        self.avoidance_gain: float = 0.3
        self.goalReach = []
        self.randvel = np.zeros(2)
        

    def run(self):
        for agent in self.agents:
            if agent.limitPos() == False:
                agent.checkState()
                if agent.state == 0:
                    # print("0")
                    if agent.flag_rad == True:
                        self.runRandom(agent)
                    else:
                        agent.randVel = np.random.uniform(-2, 2, 2)
                        agent.flag_rad = True
                    self.findGoal(agent)
                    self.runAvoidance(agent)
                elif(agent.state == 1):
                    # print("1")
                    self.gotoGoal(agent)
                    self.runAvoidance(agent)
                elif(agent.state == 2):
                    # print("2")
                    self.pubGoal(agent)
                    agent.vel = np.zeros(2)
                    agent.run()  
            else: 
                agent.vel = np.zeros(2)
                agent.run()
        # print(self.goalReach)
    # def pubGoal(self,agent:Agent):
    #     for goal in self.goals:
    #         dis = computeDistance(goal,agent.global_pos,0.0)
    #         if dis < self.goal_range:
    #             # print("1")
    #             if self.checkGoalReach(goal) == False:
    #                 for other in self.agents:
    #                     if other.global_pos[1] > 7.0 and np.random.rand(1) >= 0.4 : 
    #                         other.checkState()
    #                         if other.state == 0:
    #                             other.goalList = goal
    #                             self.goalReach.append(goal)
    #                             # print(other.id, goal)
    #                             break
    
    def pubGoal(self,agent:Agent):
        for goal in self.goals:
            dis = computeDistance(goal,agent.global_pos,0.0)
            if dis < self.goal_range:
                # print("1")
                if self.checkGoalReach(goal) == False:
                    for other in self.agents:
                        if computeDistance(other.global_pos, agent.global_pos, 0.0) < 12.0:
                            other.checkState()
                            if other.state == 0:
                                other.goalList = goal
                                self.goalReach.append(goal)
                                # print(other.id, goal)
                                break

    # def runRandom(self,agent:Agent):
    #     velRand = np.array([np.random.rand(1)*2-1 , np.random.rand(1)])
    #     agent.vel = agent.limitVelocity(vel=velRand)
    #     agent.run()
        
    def runRandom(self,agent:Agent):
        velRand = np.array([agent.randVel[0] , agent.randVel[1]])
        agent.vel = agent.limitVelocity(vel=velRand)
        agent.run()
    
    def findGoal(self, agent:Agent):
        for goal in self.goals:
            dis = computeDistance(goal,agent.global_pos,0.0)
            if dis < self.goal_range:
                if self.checkGoalReach(goal) == False:
                    self.goalReach.append(goal)
                    agent.goalList = goal

    def gotoGoal(self,agent:Agent):
        velGoal = np.zeros(2)

        velGoal = self.goal_gain*(agent.goalList-agent.global_pos)

        agent.vel = agent.limitVelocity(vel=velGoal)/0.1
        agent.run()        

    def runAvoidance(self, agent:Agent):
        velAvoid = np.zeros(2)
        for other in self.agents:
            if other.id == agent.id: continue
            dis = computeDistance(agent.global_pos,other.global_pos,0)
            if dis < self.avoidance_range:
                velAvoid += self.avoidance_gain** math.exp(-(dis - self.avoidance_range))/(dis - self.avoidance_range) * (other.global_pos - agent.global_pos)/dis

        agent.vel = agent.limitVelocity(vel=velAvoid)/0.1
        agent.run()
    
    def checkGoalReach(self,goal):
        for i in self.goalReach:
            if goal[0] == i[0] and goal[1] == i [1]:
                return True
        return False

    def visualize(self):
        for agent in self.agents:
            agent.visualize()

        