from stable_baselines3 import PPO
from hex_chess_env import HexChessEnv  # Импорт среды

def test_model():
    model = PPO.load("hex_chess_model")
    env = HexChessEnv()
    obs = env.reset()
    for _ in range(100):
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, dones, info = env.step(action)
        env.render()
        if dones:
            break