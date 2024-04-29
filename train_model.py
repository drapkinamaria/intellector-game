from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from hex_chess_env import HexChessEnv  # Импорт среды

def train_model():
    env = make_vec_env(lambda: HexChessEnv(), n_envs=4)
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=5000)
    model.save("hex_chess_model")
    print("ready")
    return model