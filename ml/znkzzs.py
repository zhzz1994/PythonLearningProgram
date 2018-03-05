import tkinter as tk
import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt

height = 6
weight = 6
UNIT = 40

class enviroment(tk.Tk):
    def __init__(self):
        super(enviroment, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('game')
        self.geometry('{0}x{1}'.format(height * UNIT, weight * UNIT))
        self.buildenv()

    def buildenv(self):
        self.canvas = tk.Canvas(self, bg='white',
                                height=height * UNIT,
                                width=weight * UNIT)

        for c in range(0,weight * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, height * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, height * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, weight * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        origin = np.array([UNIT*0.5, UNIT*0.5])

        hell1_center = origin + np.array([UNIT * 4, UNIT*4])
        self.hell1 = self.canvas.create_rectangle(
            hell1_center[0] - 15, hell1_center[1] - 15,
            hell1_center[0] + 15, hell1_center[1] + 15,
            fill='black')

        hell2_center = origin + np.array([UNIT * 1, UNIT * 2])
        self.hell2 = self.canvas.create_rectangle(
            hell2_center[0] - 15, hell2_center[1] - 15,
            hell2_center[0] + 15, hell2_center[1] + 15,
            fill='black')

        hell3_center = origin + np.array([UNIT * 2, UNIT*3])
        self.hell3 = self.canvas.create_rectangle(
            hell3_center[0] - 15, hell3_center[1] - 15,
            hell3_center[0] + 15, hell3_center[1] + 15,
            fill='black')

        hell4_center = origin + np.array([UNIT * 5, UNIT*3])
        self.hell4 = self.canvas.create_rectangle(
            hell4_center[0] - 15, hell4_center[1] - 15,
            hell4_center[0] + 15, hell4_center[1] + 15,
            fill='black')

        # trans1_center = origin + np.array([UNIT * 2, UNIT * 1])
        # self.trans1 = self.canvas.create_rectangle(
        #     trans1_center[0] - 15, trans1_center[1] - 15,
        #     trans1_center[0] + 15, trans1_center[1] + 15,
        #     fill='blue')

        # trans2_center = origin + np.array([UNIT * 2, UNIT * 2])
        # self.trans2 = self.canvas.create_rectangle(
        #     trans2_center[0] - 15, trans2_center[1] - 15,
        #     trans2_center[0] + 15, trans2_center[1] + 15,
        #     fill='blue')

        end_center = origin + np.array([UNIT * 5, UNIT * 4])
        self.end = self.canvas.create_oval(
            end_center[0] - 15, end_center[1] - 15,
            end_center[0] + 15, end_center[1] + 15,
            fill='yellow')

        self.actor = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        self.canvas.pack()

    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.actor)
        origin = np.array([UNIT*0.5, UNIT*0.5])
        self.actor = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        return self.canvas.coords(self.actor)

    def step(self,action):
        s = self.canvas.coords(self.actor)
        base_action = np.array([0, 0])
        if action == 0:  # up
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:  # down
            if s[1] < (height - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:  # right
            if s[0] < (weight - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:  # left
            if s[0] > UNIT:
                base_action[0] -= UNIT
        self.canvas.move(self.actor, base_action[0], base_action[1])
        spoint = self.canvas.coords(self.actor)
        if spoint == self.canvas.coords(self.end):
            reward = 50
            done = True
        elif spoint in [self.canvas.coords(self.hell1),self.canvas.coords(self.hell2),
                        self.canvas.coords(self.hell3),self.canvas.coords(self.hell4)]:
            reward = -20
            done = True
        # # elif spoint in [self.canvas.coords(self.trans1)]:
        # #     reward = 1
        # #     done = False
        # #     rand1 = np.random.randint(2,3)
        # #     rand2 = np.random.randint(4,5)
        #     self.canvas.move(self.actor, rand1*UNIT,  rand2*UNIT)
        #     #print(rand1,rand2)
        #     spoint = self.canvas.coords(self.actor)
        else:
            reward = -1
            done = False
        return spoint, reward, done

    def render(self):
        self.update()

class SarsaLambdaTable():
    def __init__(self, actions, learning_rate=0.15, reward_decay=0.9,  trace_decay=0.9):
        self.actions = actions  # a list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.q_table = pd.DataFrame(columns=self.actions)
        self.lambda_ = trace_decay
        self.eligibility_trace = self.q_table.copy()

    def choose_action(self, observation, e_greedy):
        self.check_state_exist(observation)
        if np.random.rand() < e_greedy:
            state_action = self.q_table.ix[observation, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))
            action = state_action.argmax()
        else:
            action = np.random.choice(self.actions)
        return action

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            to_be_append = pd.Series(
                    [0] * len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            self.q_table = self.q_table.append(to_be_append)
            self.eligibility_trace = self.eligibility_trace.append(to_be_append)

    def learn(self, s, a, r, s_, a_):
        self.check_state_exist(s_)
        q_predict = self.q_table.ix[s, a]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.q_table.ix[s_, a_]  # next state is not terminal
        else:
            q_target = r
        error = q_target - q_predict

        self.eligibility_trace.ix[s, a] += 1
        self.q_table += self.lr * error * self.eligibility_trace
        self.eligibility_trace *= self.gamma*self.lambda_

def update():
    egreedy = 0.5
    step = 0
    for episode in range(100):
        allreward = 0
        observation = env.reset()
        action = RL.choose_action(str(observation),egreedy)
        RL.eligibility_trace *= 0
        while True:
            env.render()
            print(episode)
            observation_, reward, done = env.step(action)
            allreward += reward
            print(egreedy)
            action_ = RL.choose_action(str(observation_),egreedy)
            RL.learn(str(observation), action, reward, str(observation_), action_)
            observation = observation_
            action = action_
            step += 1
            egreedy = 1 - 1/(step**0.5)
            if done:
                rewardlist.append(allreward)
                break
    env.destroy()

if __name__ == "__main__":
    env = enviroment()
    RL = SarsaLambdaTable(actions=list(range(env.n_actions)))
    rewardlist = []
    env.after(100, update)
    env.mainloop()
    plt.plot(rewardlist, '.')
    plt.show()