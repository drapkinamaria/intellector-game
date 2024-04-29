import sys

from hex_chess_env import HexChessEnv
from train_model import train_model

def simulate_game(env, model, num_steps=100):
    obs = env.reset()
    env.render()
    for _ in range(num_steps):
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, dones, info = env.step(action)
        print(f"Action taken: {action} | Reward received: {rewards}")
        env.render()
        if dones:
            print("Game ended")
            break

if __name__ == "__main__":
    # Step 1: Create and render the initial environment
    env = HexChessEnv()
    #env.render()

    # Step 2: Train the model
    trained_model = train_model()
    print(trained_model)

    # Step 3: Test and display results using the trained model
    simulate_game(env, trained_model)
    sys.exit()
