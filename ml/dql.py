import numpy as np
import pandas as pd
import tensorflow as tf

np.random.seed(1)
tf.set_random_seed(1)

import numpy as np
import tkinter as tk
import time


height = 4
weight = 4
UNIT = 80

class Maze(tk.Tk):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.n_features = 4
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

        # hell1_center = origin + np.array([UNIT * 3, UNIT*3])
        # self.hell1 = self.canvas.create_rectangle(
        #     hell1_center[0] - 15, hell1_center[1] - 15,
        #     hell1_center[0] + 15, hell1_center[1] + 15,
        #     fill='green')

        # hell3_center = origin + np.array([UNIT * 1, UNIT*1])
        # self.hell3 = self.canvas.create_rectangle(
        #     hell3_center[0] - 15, hell3_center[1] - 15,
        #     hell3_center[0] + 15, hell3_center[1] + 15,
        #     fill='green')
        #
        # hell4_center = origin + np.array([UNIT * 2, UNIT*4])
        # self.hell4 = self.canvas.create_rectangle(
        #     hell4_center[0] - 15, hell4_center[1] - 15,
        #     hell4_center[0] + 15, hell4_center[1] + 15,
        #     fill='green')

        # trans1_center = origin + np.array([UNIT * 2, UNIT * 3])
        # self.trans1 = self.canvas.create_rectangle(
        #     trans1_center[0] - 15, trans1_center[1] - 15,
        #     trans1_center[0] + 15, trans1_center[1] + 15,
        #     fill='blue')

        # trans2_center = origin + np.array([UNIT * 2, UNIT * 2])
        # self.trans2 = self.canvas.create_rectangle(
        #     trans2_center[0] - 15, trans2_center[1] - 15,
        #     trans2_center[0] + 15, trans2_center[1] + 15,
        #     fill='blue')

        end_center = origin + np.array([UNIT * 2, UNIT * 2])
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
        time.sleep(0.1)
        self.canvas.delete(self.actor)
        self.canvas.delete(self.end)
        origin = np.array([UNIT*0.5, UNIT*0.5])
        self.actor = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        end_center = origin + np.array([UNIT * 2, UNIT * 2])
        self.end = self.canvas.create_oval(
            end_center[0] - 15, end_center[1] - 15,
            end_center[0] + 15, end_center[1] + 15,
            fill='yellow')
        a = np.array(self.canvas.coords(self.actor)[:2])
        b = np.array(self.canvas.coords(self.end)[:2])
        featl = [a[0],a[1],b[0],b[1]]
        feat = np.array(featl)
        return feat

    def stepactor(self,action):
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
            reward = 120
            done = True
        # elif spoint in [self.canvas.coords(self.hell1),self.canvas.coords(self.hell4),
        #                 self.canvas.coords(self.hell3)]:
        #     reward = -10
        #     done = True
        # elif spoint in [self.canvas.coords(self.trans1)]:
        #     reward = 1
        #     done = False
        #     rand1 = np.random.randint(2,3)
        #     rand2 = np.random.randint(4,5)
        #     self.canvas.move(self.actor, rand1*UNIT,  rand2*UNIT)
        #     #print(rand1,rand2)
        #     spoint = self.canvas.coords(self.actor)
        else:
            reward = -1
            done = False
        a = np.array(self.canvas.coords(self.actor)[:2])
        b = np.array(self.canvas.coords(self.end)[:2])
        featl = [a[0], a[1], b[0], b[1]]
        feat = np.array(featl)
        return feat, reward, done

    def stepactor2(self, action):
        s = self.canvas.coords(self.end)
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
        self.canvas.move(self.end, base_action[0], base_action[1])
        spoint = self.canvas.coords(self.end)
        if spoint == self.canvas.coords(self.actor):
            reward = -120
            done = True
        # elif spoint in [self.canvas.coords(self.hell3), self.canvas.coords(self.hell4),
        #                 self.canvas.coords(self.hell3)]:
        #     reward = 5
        #     done = False
        # elif spoint in [self.canvas.coords(self.trans1)]:
        #     reward = 1
        #     done = False
        #     rand1 = np.random.randint(2,3)
        #     rand2 = np.random.randint(4,5)
        #     self.canvas.move(self.actor, rand1*UNIT,  rand2*UNIT)
        #     #print(rand1,rand2)
        #     spoint = self.canvas.coords(self.actor)
        else:
            reward = 1
            done = False
        a = np.array(self.canvas.coords(self.actor)[:2])
        b = np.array(self.canvas.coords(self.end)[:2])
        featl = [a[0], a[1], b[0], b[1]]
        feat = np.array(featl)
        return feat, reward, done

    def render(self):
        #time.sleep(0.1)
        self.update()

class DeepQNetwork:
    def __init__(
            self,
            n_actions,
            n_features,
            learning_rate=0.01,
            reward_decay=0.9,
            e_greedy=0.9,
            replace_target_iter=300,
            memory_size=500,
            batch_size=32,
            e_greedy_increment=None,
            output_graph=False,
    ):
        self.n_actions = n_actions
        self.n_features = n_features
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon_max = e_greedy
        self.replace_target_iter = replace_target_iter
        self.memory_size = memory_size
        self.batch_size = batch_size
        self.epsilon_increment = e_greedy_increment
        self.epsilon = 0 if e_greedy_increment is not None else self.epsilon_max

        # total learning step
        self.learn_step_counter = 0

        # initialize zero memory [s, a, r, s_]
        self.memory = np.zeros((self.memory_size, n_features * 2 + 2))

        # consist of [target_net, evaluate_net]
        self._build_net()

        self.sess = tf.Session()

        if output_graph:
            # $ tensorboard --logdir=logs
            # tf.train.SummaryWriter soon be deprecated, use following
            tf.summary.FileWriter("logs/", self.sess.graph)

        self.sess.run(tf.global_variables_initializer())
        self.cost_his = []

    def _build_net(self):
        # ------------------ build evaluate_net ------------------
        self.s = tf.placeholder(tf.float32, [None, self.n_features], name='s')  # input
        self.q_target = tf.placeholder(tf.float32, [None, self.n_actions], name='Q_target')  # for calculating loss
        with tf.variable_scope('eval_net'):
            # c_names(collections_names) are the collections to store variables
            c_names, n_l1, w_initializer, b_initializer = \
                ['eval_net_params', tf.GraphKeys.GLOBAL_VARIABLES], 50, \
                tf.random_normal_initializer(0., 0.3), tf.constant_initializer(0.1)  # config of layers

            # first layer. collections is used later when assign to target net
            with tf.variable_scope('l1'):
                w1 = tf.get_variable('w1', [self.n_features, n_l1], initializer=w_initializer, collections=c_names)
                b1 = tf.get_variable('b1', [1, n_l1], initializer=b_initializer, collections=c_names)
                l1 = tf.nn.relu(tf.matmul(self.s, w1) + b1)

            # second layer. collections is used later when assign to target net
            with tf.variable_scope('l2'):
                w2 = tf.get_variable('w2', [n_l1, self.n_actions], initializer=w_initializer, collections=c_names)
                b2 = tf.get_variable('b2', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                self.q_eval = tf.matmul(l1, w2) + b2

        with tf.variable_scope('loss'):
            self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval))
        with tf.variable_scope('train'):
            self._train_op = tf.train.RMSPropOptimizer(self.lr).minimize(self.loss)

        # ------------------ build target_net ------------------
        self.s_ = tf.placeholder(tf.float32, [None, self.n_features], name='s_')    # input
        with tf.variable_scope('target_net'):
            # c_names(collections_names) are the collections to store variables
            c_names = ['target_net_params', tf.GraphKeys.GLOBAL_VARIABLES]

            # first layer. collections is used later when assign to target net
            with tf.variable_scope('l1'):
                w1 = tf.get_variable('w1', [self.n_features, n_l1], initializer=w_initializer, collections=c_names)
                b1 = tf.get_variable('b1', [1, n_l1], initializer=b_initializer, collections=c_names)
                l1 = tf.nn.relu(tf.matmul(self.s_, w1) + b1)

            # second layer. collections is used later when assign to target net
            with tf.variable_scope('l2'):
                w2 = tf.get_variable('w2', [n_l1, self.n_actions], initializer=w_initializer, collections=c_names)
                b2 = tf.get_variable('b2', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                self.q_next = tf.matmul(l1, w2) + b2

    def store_transition(self, s, a, r, s_):
        if not hasattr(self, 'memory_counter'):
            self.memory_counter = 0

        transition = np.hstack((s, [a, r], s_))

        # replace the old memory with new memory
        index = self.memory_counter % self.memory_size
        self.memory[index, :] = transition

        self.memory_counter += 1

    def choose_action(self, observation):
        # to have batch dimension when feed into tf placeholder
        observation = observation[np.newaxis, :]

        if np.random.uniform() < self.epsilon:
            # forward feed the observation and get q value for every actions
            actions_value = self.sess.run(self.q_eval, feed_dict={self.s: observation})
            action = np.argmax(actions_value)
        else:
            action = np.random.randint(0, self.n_actions)
        return action

    def _replace_target_params(self):
        t_params = tf.get_collection('target_net_params')
        e_params = tf.get_collection('eval_net_params')
        self.sess.run([tf.assign(t, e) for t, e in zip(t_params, e_params)])

    def learn(self):
        # check to replace target parameters
        if self.learn_step_counter % self.replace_target_iter == 0:
            self._replace_target_params()
            print('\ntarget_params_replaced\n')

        # sample batch memory from all memory
        if self.memory_counter > self.memory_size:
            sample_index = np.random.choice(self.memory_size, size=self.batch_size)
        else:
            sample_index = np.random.choice(self.memory_counter, size=self.batch_size)
        batch_memory = self.memory[sample_index, :]

        q_next, q_eval = self.sess.run(
            [self.q_next, self.q_eval],
            feed_dict={
                self.s_: batch_memory[:, -self.n_features:],  # fixed params
                self.s: batch_memory[:, :self.n_features],  # newest params
            })

        # change q_target w.r.t q_eval's action
        q_target = q_eval.copy()

        batch_index = np.arange(self.batch_size, dtype=np.int32)
        eval_act_index = batch_memory[:, self.n_features].astype(int)
        reward = batch_memory[:, self.n_features + 1]

        q_target[batch_index, eval_act_index] = reward + self.gamma * np.max(q_next, axis=1)

        """
        For example in this batch I have 2 samples and 3 actions:
        q_eval =
        [[1, 2, 3],
         [4, 5, 6]]
        q_target = q_eval =
        [[1, 2, 3],
         [4, 5, 6]]
        Then change q_target with the real q_target value w.r.t the q_eval's action.
        For example in:
            sample 0, I took action 0, and the max q_target value is -1;
            sample 1, I took action 2, and the max q_target value is -2:
        q_target =
        [[-1, 2, 3],
         [4, 5, -2]]
        So the (q_target - q_eval) becomes:
        [[(-1)-(1), 0, 0],
         [0, 0, (-2)-(6)]]
        We then backpropagate this error w.r.t the corresponding action to network,
        leave other action as error=0 cause we didn't choose it.
        """

        # train eval network
        _, self.cost = self.sess.run([self._train_op, self.loss],
                                     feed_dict={self.s: batch_memory[:, :self.n_features],
                                                self.q_target: q_target})
        self.cost_his.append(self.cost)

        # increasing epsilon
        self.epsilon = self.epsilon + self.epsilon_increment if self.epsilon < self.epsilon_max else self.epsilon_max
        self.learn_step_counter += 1

    def plot_cost(self):
        import matplotlib.pyplot as plt
        plt.plot(np.arange(len(self.cost_his)), self.cost_his)
        plt.ylabel('Cost')
        plt.xlabel('training steps')
        plt.show()

class DeepQNetwork2:
    def __init__(
            self,
            n_actions,
            n_features,
            learning_rate=0.01,
            reward_decay=0.9,
            e_greedy=0.9,
            replace_target_iter=300,
            memory_size=500,
            batch_size=32,
            e_greedy_increment=None,
            output_graph=False,
    ):
        self.n_actions = n_actions
        self.n_features = n_features
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon_max = e_greedy
        self.replace_target_iter = replace_target_iter
        self.memory_size = memory_size
        self.batch_size = batch_size
        self.epsilon_increment = e_greedy_increment
        self.epsilon = 0 if e_greedy_increment is not None else self.epsilon_max

        # total learning step
        self.learn_step_counter = 0

        # initialize zero memory [s, a, r, s_]
        self.memory = np.zeros((self.memory_size, n_features * 2 + 2))

        # consist of [target_net, evaluate_net]
        self._build_net()

        self.sess = tf.Session()

        if output_graph:
            # $ tensorboard --logdir=logs
            # tf.train.SummaryWriter soon be deprecated, use following
            tf.summary.FileWriter("logs/", self.sess.graph)

        self.sess.run(tf.global_variables_initializer())
        self.cost_his = []

    def _build_net(self):
        # ------------------ build evaluate_net ------------------
        self.s = tf.placeholder(tf.float32, [None, self.n_features], name='s')  # input
        self.q_target = tf.placeholder(tf.float32, [None, self.n_actions], name='Q_target')  # for calculating loss
        with tf.variable_scope('eval_net2'):
            # c_names(collections_names) are the collections to store variables
            c_names, n_l1, w_initializer, b_initializer = \
                ['eval_net_params2', tf.GraphKeys.GLOBAL_VARIABLES], 50, \
                tf.random_normal_initializer(0., 0.3), tf.constant_initializer(0.1)  # config of layers

            # first layer. collections is used later when assign to target net
            with tf.variable_scope('l12'):
                w1 = tf.get_variable('w11', [self.n_features, n_l1], initializer=w_initializer, collections=c_names)
                b1 = tf.get_variable('b11', [1, n_l1], initializer=b_initializer, collections=c_names)
                l1 = tf.nn.relu(tf.matmul(self.s, w1) + b1)

            # second layer. collections is used later when assign to target net
            with tf.variable_scope('l22'):
                w2 = tf.get_variable('w212', [n_l1, self.n_actions], initializer=w_initializer, collections=c_names)
                b2 = tf.get_variable('b212', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                self.q_eval = tf.matmul(l1, w2) + b2

        with tf.variable_scope('loss2'):
            self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval))
        with tf.variable_scope('train2'):
            self._train_op = tf.train.RMSPropOptimizer(self.lr).minimize(self.loss)

        # ------------------ build target_net ------------------
        self.s_ = tf.placeholder(tf.float32, [None, self.n_features], name='s_')    # input
        with tf.variable_scope('target_net2'):
            # c_names(collections_names) are the collections to store variables
            c_names = ['target_net_params2', tf.GraphKeys.GLOBAL_VARIABLES]

            # first layer. collections is used later when assign to target net
            with tf.variable_scope('l12'):
                w1 = tf.get_variable('w112', [self.n_features, n_l1], initializer=w_initializer, collections=c_names)
                b1 = tf.get_variable('b112', [1, n_l1], initializer=b_initializer, collections=c_names)
                l1 = tf.nn.relu(tf.matmul(self.s_, w1) + b1)

            # second layer. collections is used later when assign to target net
            with tf.variable_scope('l22'):
                w2 = tf.get_variable('w212', [n_l1, self.n_actions], initializer=w_initializer, collections=c_names)
                b2 = tf.get_variable('b212', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                self.q_next = tf.matmul(l1, w2) + b2

    def store_transition(self, s, a, r, s_):
        if not hasattr(self, 'memory_counter2'):
            self.memory_counter = 0

        transition = np.hstack((s, [a, r], s_))

        # replace the old memory with new memory
        index = self.memory_counter % self.memory_size
        self.memory[index, :] = transition

        self.memory_counter += 1

    def choose_action(self, observation):
        # to have batch dimension when feed into tf placeholder
        observation = observation[np.newaxis, :]

        if np.random.uniform() < self.epsilon:
            # forward feed the observation and get q value for every actions
            actions_value = self.sess.run(self.q_eval, feed_dict={self.s: observation})
            action = np.argmax(actions_value)
        else:
            action = np.random.randint(0, self.n_actions)
        return action

    def _replace_target_params(self):
        t_params = tf.get_collection('target_net_params2')
        e_params = tf.get_collection('eval_net_params2')
        self.sess.run([tf.assign(t, e) for t, e in zip(t_params, e_params)])

    def learn(self):
        # check to replace target parameters
        if self.learn_step_counter % self.replace_target_iter == 0:
            self._replace_target_params()
            print('\ntarget_params_replaced2\n')

        # sample batch memory from all memory
        if self.memory_counter > self.memory_size:
            sample_index = np.random.choice(self.memory_size, size=self.batch_size)
        else:
            sample_index = np.random.choice(self.memory_counter, size=self.batch_size)
        batch_memory = self.memory[sample_index, :]

        q_next, q_eval = self.sess.run(
            [self.q_next, self.q_eval],
            feed_dict={
                self.s_: batch_memory[:, -self.n_features:],  # fixed params
                self.s: batch_memory[:, :self.n_features],  # newest params
            })

        # change q_target w.r.t q_eval's action
        q_target = q_eval.copy()

        batch_index = np.arange(self.batch_size, dtype=np.int32)
        eval_act_index = batch_memory[:, self.n_features].astype(int)
        reward = batch_memory[:, self.n_features + 1]

        q_target[batch_index, eval_act_index] = reward + self.gamma * np.max(q_next, axis=1)

        """
        For example in this batch I have 2 samples and 3 actions:
        q_eval =
        [[1, 2, 3],
         [4, 5, 6]]
        q_target = q_eval =
        [[1, 2, 3],
         [4, 5, 6]]
        Then change q_target with the real q_target value w.r.t the q_eval's action.
        For example in:
            sample 0, I took action 0, and the max q_target value is -1;
            sample 1, I took action 2, and the max q_target value is -2:
        q_target =
        [[-1, 2, 3],
         [4, 5, -2]]
        So the (q_target - q_eval) becomes:
        [[(-1)-(1), 0, 0],
         [0, 0, (-2)-(6)]]
        We then backpropagate this error w.r.t the corresponding action to network,
        leave other action as error=0 cause we didn't choose it.
        """

        # train eval network
        _, self.cost = self.sess.run([self._train_op, self.loss],
                                     feed_dict={self.s: batch_memory[:, :self.n_features],
                                                self.q_target: q_target})
        self.cost_his.append(self.cost)

        # increasing epsilon
        self.epsilon = self.epsilon + self.epsilon_increment if self.epsilon < self.epsilon_max else self.epsilon_max
        self.learn_step_counter += 1

    def plot_cost(self):
        import matplotlib.pyplot as plt
        plt.plot(np.arange(len(self.cost_his)), self.cost_his)
        plt.ylabel('Cost2')
        plt.xlabel('training steps2')
        plt.show()

def run_maze():
    step = 0
    count = 0
    for episode in range(3000):
        observation = env.reset()
        while True:
            env.render()
            action = RLactor.choose_action(observation)
            observation_, reward, done = env.stepactor(action)
            RLactor.store_transition(observation, action, reward, observation_)
            if (step > 10) and (step % 5 == 0):
                RLactor.learn()
            observation = observation_
            action2 = RLactor2.choose_action(observation)
            observation_, reward2, done2 = env.stepactor2(action2)
            RLactor2.store_transition(observation, action2, reward2, observation_)
            if (step > 10) and (step % 5 == 0):
                RLactor2.learn()
            observation = observation_
            time.sleep(0.05)
            step += 1
            count += 1
            print(count)
            over = done+done2
            if over:
                print(over)
                break
    print('game over')
    env.destroy()

if __name__ == "__main__":
    # maze game
    env = Maze()
    RLactor = DeepQNetwork(env.n_actions, env.n_features,
                      learning_rate=0.1,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=20,
                      memory_size=5000,
                      # output_graph=True
                      )
    RLactor2 = DeepQNetwork2(env.n_actions, env.n_features,
                           learning_rate=0.1,
                           reward_decay=0.9,
                           e_greedy=0.9,
                           replace_target_iter=20,
                           memory_size=5000,
                           # output_graph=True
                           )
    env.after(100, run_maze)
    env.mainloop()
    RLactor.plot_cost()
    RLactor2.plot_cost()