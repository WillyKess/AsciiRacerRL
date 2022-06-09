from collections import OrderedDict, namedtuple
import gym
import pprint
from queue import Queue
import threading
from time import sleep
from asciiracer.game import run
from gym import spaces
import numpy as np
Sprite = namedtuple('Sprite', ['attrs', 'current_coords'])
teststate = {'car': Sprite(attrs=None, current_coords=((31, 35), (48, 71))),
 'car_speed_tuple': None,
 'car_steer_tuple': None,
 'car_x': 0,
 'money': [Sprite(attrs=((['╲___╱', ' ╲G╱ ', '  ╿   ', '  ┴  '], 5), 18, 50, 1.8333333333333317, 1), current_coords=((18, 21), (50, 55)))],
 'score': -20,
 'speed': 5,
 'frames': 118,}
def _getobs(state):
    if state['car_speed_tuple'] is None:
        state['car_speed_tuple'] = (0, 0)
    if state['car_steer_tuple'] is None:
        state['car_steer_tuple'] = (0, 0)
    drinkvals = {
        10: 0,
        1: 1,
        5: 2,
        -20: 2
    }
    speedvals = {
        0: 0,
        -1: 1,
        1: 2
    }
    moneyval = drinkvals.get(state['money'][0].attrs[0][1])
    obs = {
        'car_coords': (np.array(state['car'].current_coords[0]), np.array(state['car'].current_coords[1]).astype(np.int32)),
        'car_speed_tuple': (np.array([state['car_speed_tuple'][0]]).astype(np.float32), speedvals.get(state['car_speed_tuple'][1])),
        'car_steer_tuple': (np.array([state['car_steer_tuple'][0]]).astype(np.float32), speedvals.get(state['car_steer_tuple'][1])),
        'car_x': np.array([state['car_x']]).astype(np.int32),
        'money': (moneyval, np.array(state['money'][0].current_coords[0]), np.array(state['money'][0].current_coords[1]).astype(np.int32)),
        'score': np.array([state['score']]).astype(np.float32),
        'speed': np.array([state['speed']]).astype(np.int32),
    }
    # obs = {
    #     'score': np.array(state['score']).astype(np.int32),
    #     'car_coords': (np.array(state['car'].current_coords[0]).astype(np.int32), np.array(state['car'].current_coords[1]).astype(np.int32)),
    #     'car_x': np.array(state['car_x']).astype(np.int32),
    #     'speed': np.array(state['speed']).astype(np.int32),
    #     'money': (state['money'][0].attrs[0][1], np.array(state['money'][0].current_coords[0]).astype(np.int32), np.array(state['money'][0].current_coords[1]).astype(np.int32)),
    #     'car_steer_tuple': (np.array(state['car_steer_tuple'][0]).astype(np.float32), np.array(state['car_steer_tuple'][1]).astype(np.int32)),
    #     'car_speed_tuple': (np.array(state['car_speed_tuple'][0]).astype(np.float32), np.array(state['car_speed_tuple'][1]).astype(np.int32)),
    # }
    # print(pprint.pformat(obs))
    return OrderedDict(obs)
class RacerEnv(gym.Env):
    def __init__(self):
        self.lastscore = 0
        self.action_space = spaces.Discrete(4)
        self.action_to_key = {0: ord('a'), 1: ord('d'), 2: ord('w'), 3: ord('s')}
        self.observation_space = spaces.Dict({
            'car_coords': spaces.Tuple((spaces.Box(low=0, high=500, shape=(2,), dtype=int), spaces.Box(low=0, high=500, shape=(2,), dtype=np.int32))),
            'car_speed_tuple': spaces.Tuple((spaces.Box(low=0, high=np.inf, shape=(1,), dtype=np.float32), spaces.Discrete(3))),
            'car_steer_tuple': spaces.Tuple((spaces.Box(low=0, high=np.inf, shape=(1,), dtype=np.float32), spaces.Discrete(3))),
            'car_x': spaces.Box(low=-500, high=500, shape=(1,), dtype=np.int32),
            'money': spaces.Tuple((spaces.Discrete(4), spaces.Box(low=0, high=500, shape=(2,), dtype=int), spaces.Box(low=0, high=500, shape=(2,), dtype=np.int32))),
            'score': spaces.Box(low=np.NINF, high=np.inf, shape=(1,), dtype=np.float32),
            'speed': spaces.Box(low=0, high=100, shape=(1,), dtype=np.int32),
        })
        self.statequeue: Queue[dict] = Queue()
        self.keyqueue: Queue[int] = Queue()
        # thread = threading.Thread(target=lambda: run(squeue=self.statequeue, kqueue=self.keyqueue), daemon=False)
        # thread.start()
    def step(self, action):
        self.keyqueue.put(self.action_to_key[action])  # type: ignore
        lastscore: int = self.lastscore
        # state = teststate
        state = self.statequeue.get()
        self.lastscore=state['score']
        return _getobs(state), state['score']-lastscore, (state['frames'] > 1200), {}
    def reset(self):
        try:
            self.keyqueue.put(ord('q'))
        except:
            pass
        self.keyqueue = Queue()
        thread = threading.Thread(target=lambda: run(squeue=self.statequeue, kqueue=self.keyqueue), daemon=False)
        thread.start()
        state = self.statequeue.get()
        # state = teststate
        return _getobs(state)
    def close(self):
        try:
            self.keyqueue.put(ord('q'))
        except:
            pass

# from stable_baselines3.common.env_checker import check_env
# env =  RacerEnv()
# check_env(env)
# sleep(5)
# env.close()