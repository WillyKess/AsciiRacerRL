from time import sleep
from gym.wrappers import FlattenObservation
import racerenv
from stable_baselines3 import A2C
from stable_baselines3.common.evaluation import evaluate_policy
env = racerenv.RacerEnv()
# print(env.observation_space)
env = FlattenObservation(env)
# print(env.observation_space)
model = A2C('MlpPolicy', env)
model.learn(total_timesteps=10000)
env.close()
sleep(2)
print("Done training!")
# model.save('a2c_racer')
# model = A2C.load('a2c_racer', env=env)
# mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)  # type: ignore
# obs = env.reset()
# for i in range(1000):
#     action, _states = model.predict(obs, deterministic=True)  # type: ignore
#     obs, rewards, dones, info = env.step(action)