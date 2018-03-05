import tkinter as tk
import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt

height = 6
weight = 6
UNIT = 80

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

        hell1_center = origin + np.array([UNIT * 5, UNIT*4])
        self.hell1 = self.canvas.create_rectangle(
            hell1_center[0] - 15, hell1_center[1] - 15,
            hell1_center[0] + 15, hell1_center[1] + 15,
            fill='black')

        # hell2_center = origin + np.array([UNIT * 4, UNIT * 4])
        # self.hell2 = self.canvas.create_rectangle(
        #     hell2_center[0] - 15, hell2_center[1] - 15,
        #     hell2_center[0] + 15, hell2_center[1] + 15,
        #     fill='black')

        hell3_center = origin + np.array([UNIT * 3, UNIT*4])
        self.hell3 = self.canvas.create_rectangle(
            hell3_center[0] - 15, hell3_center[1] - 15,
            hell3_center[0] + 15, hell3_center[1] + 15,
            fill='black')

        # hell4_center = origin + np.array([UNIT * 3, UNIT*4])
        # self.hell4 = self.canvas.create_rectangle(
        #     hell4_center[0] - 15, hell4_center[1] - 15,
        #     hell4_center[0] + 15, hell4_center[1] + 15,
        #     fill='black')

        trans1_center = origin + np.array([UNIT * 2, UNIT * 1])
        self.trans1 = self.canvas.create_rectangle(
            trans1_center[0] - 15, trans1_center[1] - 15,
            trans1_center[0] + 15, trans1_center[1] + 15,
            fill='blue')

        # trans2_center = origin + np.array([UNIT * 2, UNIT * 2])
        # self.trans2 = self.canvas.create_rectangle(
        #     trans2_center[0] - 15, trans2_center[1] - 15,
        #     trans2_center[0] + 15, trans2_center[1] + 15,
        #     fill='blue')

        end_center = origin + np.array([UNIT * 4, UNIT * 5])
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
            reward = 20
            done = True
        elif spoint in [self.canvas.coords(self.hell1),
                        self.canvas.coords(self.hell3)]:
            reward = -10
            done = True
        elif spoint in [self.canvas.coords(self.trans1)]:
            reward = 1
            done = False
            rand1 = np.random.randint(2,3)
            rand2 = np.random.randint(4,5)
            self.canvas.move(self.actor, rand1*UNIT,  rand2*UNIT)
            #print(rand1,rand2)
            spoint = self.canvas.coords(self.actor)
        else:
            reward = -1
            done = False
        return spoint, reward, done

    def render(self):
        #time.sleep(0.1)
        self.update()

def tableshow():
    window = tk.Tk()
    window.title('my window')
    window.geometry('{0}x{1}'.format(height * UNIT, weight * UNIT))
    canvas = tk.Canvas(window, bg='white',
                       height=height * UNIT,
                       width=weight * UNIT)
    for c in range(0, weight * UNIT, UNIT):
        x0, y0, x1, y1 = c, 0, c, height * UNIT
        canvas.create_line(x0, y0, x1, y1)
    for r in range(0, height * UNIT, UNIT):
        x0, y0, x1, y1 = 0, r, weight * UNIT, r
        canvas.create_line(x0, y0, x1, y1)
    canvas.pack()
    window.mainloop()

class RL(object):
    def __init__(self, action_space, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        self.actions = action_space  # a list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy

        self.q_table = pd.DataFrame(columns=self.actions)

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )

    def choose_action(self, observation):
        self.check_state_exist(observation)
        # action selection
        if np.random.rand() < self.epsilon:
            # choose best action
            state_action = self.q_table.ix[observation, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))     # some actions have same value
            action = state_action.argmax()
        else:
            # choose random action
            action = np.random.choice(self.actions)
        return action

    def learn(self, *args):
        pass


# backward eligibility traces
class SarsaLambdaTable(RL):
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9, trace_decay=0.9):
        super(SarsaLambdaTable, self).__init__(actions, learning_rate, reward_decay, e_greedy)

        # backward view, eligibility trace.
        self.lambda_ = trace_decay
        self.eligibility_trace = self.q_table.copy()

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            to_be_append = pd.Series(
                    [0] * len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            self.q_table = self.q_table.append(to_be_append)

            # also update eligibility trace
            self.eligibility_trace = self.eligibility_trace.append(to_be_append)

    def learn(self, s, a, r, s_, a_):
        self.check_state_exist(s_)
        q_predict = self.q_table.ix[s, a]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.q_table.ix[s_, a_]  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        error = q_target - q_predict

        # increase trace amount for visited state-action pair

        # Method 1:
        # self.eligibility_trace.ix[s, a] += 1

        # Method 2:
        self.eligibility_trace.ix[s, :] *= 0
        self.eligibility_trace.ix[s, a] = 1

        # Q update
        self.q_table += self.lr * error * self.eligibility_trace

        # decay eligibility trace after update
        self.eligibility_trace *= self.gamma*self.lambda_

    def showtablevalue(self):
        tablevalue = self.q_table
        return tablevalue

class QLearningTable:
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        self.actions = actions
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.q_table = pd.DataFrame(columns=self.actions)

    def showtablevalue(self):
        tablevalue = self.q_table
        return tablevalue

    def choose_action(self, observation):
        self.check_state_exist(observation)
        if np.random.uniform() < self.epsilon:
            state_action = self.q_table.ix[observation, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))     # some actions have same value
            action = state_action.argmax()
        else:
            action = np.random.choice(self.actions)
        return action

    def learn(self, s, a, r, s_):
        self.check_state_exist(s_)
        q_predict = self.q_table.ix[s, a]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.q_table.ix[s_, :].max()
        else:
            q_target = r
        self.q_table.ix[s, a] += self.lr * (q_target - q_predict)

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )

# def update():
#     for episode in range(2000):
#         observation = enviroment.reset()
#         allreward = 0
#         while True:
#             enviroment.render()
#             action = RL.choose_action(str(observation))
#             observationnext, reward, done = enviroment.step(action)
#             allreward += reward
#             RL.learn(str(observation), action, reward, str(observationnext))
#             observation = observationnext
#             if done:
#                 tb = RL.showtablevalue()
#                 print(allreward)
#                 rewardlist.append(allreward)
#                 #print(tb)
#                 break
#     print('game over')
#     enviroment.destroy()

def update():
    for episode in range(5):
        observation = env.reset()
        allreward = 0
        action = RL.choose_action(str(observation))
        RL.eligibility_trace *= 0
        while True:
            env.render()
            tb = RL.showtablevalue()
            # print(tb)
            # time.sleep(0.5)
            observation_, reward, done = env.step(action)
            allreward += reward
            action_ = RL.choose_action(str(observation_))
            RL.learn(str(observation), action, reward, str(observation_), action_)
            observation = observation_
            action = action_
            if done:
                print(allreward)
                rewardlist.append(allreward)
                print(tb)
                break
    print('game over')
    env.destroy()

def showvalue():
    plt.plot(rewardlist,'.')
    plt.show()


if __name__ == "__main__":
    env = enviroment()
    RL = SarsaLambdaTable(actions=list(range(env.n_actions)))
    rewardlist = []
    env.after(100, update)
    env.mainloop()
    showvalue()