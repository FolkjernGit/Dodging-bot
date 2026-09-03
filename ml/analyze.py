import os
import pickle


best_reward = float("-inf")
best_file = None
best_episode = None


data_folder = "data"


for filename in os.listdir(data_folder):
    
    if not filename.endswith(".pkl"):
        continue

    path = os.path.join(data_folder, filename)

    try:
        with open(path, "rb") as f:
            data = pickle.load(f)

    except Exception:
        continue


    # Handle reward lists
    if isinstance(data, list):

        for episode, reward in enumerate(data):

            # handle generations saved as lists
            if isinstance(reward, list):

                for sub_episode, sub_reward in enumerate(reward):

                    if sub_reward > best_reward:
                        best_reward = sub_reward
                        best_file = filename
                        best_episode = (
                            f"generation data {episode}, "
                            f"episode {sub_episode}"
                        )

            else:

                if reward > best_reward:
                    best_reward = reward
                    best_file = filename
                    best_episode = episode



print("========== BEST REWARD FOUND ==========")

print(
    f"Reward: {best_reward:.2f}"
)

print(
    f"File: {best_file}"
)

print(
    f"Episode: {best_episode}"
)