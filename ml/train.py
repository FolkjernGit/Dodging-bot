import pygame
import torch
import pickle
import os
import time

from enviroment import DodgeEnv
from model import DodgeModel
from agent import Agent
from replay_buffer import ReplayBuffer


# folders
os.makedirs("models", exist_ok=True)
os.makedirs("data", exist_ok=True)


pygame.init()

screen = pygame.display.set_mode((800, 600))


# environment
env = DodgeEnv(screen)


# training settings
generations = 2
episodes_per_generation = 500

batch_size = 64
render_interval = 500

memory_size = 50000


# load previous global best
try:
    with open("data/best_score.pkl", "rb") as f:
        global_best_reward = pickle.load(f)

except FileNotFoundError:
    global_best_reward = float("-inf")


# tracking
global_best_episode = 0
global_best_generation = 0

total_training_time = 0

all_rewards = []


# model
model = DodgeModel()


for generation in range(generations):

    print(
        f"\n========== Generation {generation + 1}/{generations} =========="
    )


    # continue from previous generation
    if generation > 0:

        checkpoint = (
            f"models/generation_{generation}.pth"
        )

        if os.path.exists(checkpoint):

            model.load_state_dict(
                torch.load(checkpoint)
            )

            print(
                "Loaded previous generation model"
            )


    agent = Agent(model)

    # RESET EPSILON EVERY GENERATION
    agent.epsilon = 1.0


    # new replay memory
    memory = ReplayBuffer(memory_size)


    rewards = []

    generation_best = float("-inf")
    generation_best_episode = 0


    start_time = time.time()


    for episode in range(episodes_per_generation):


        render = (
            (episode + 1) % render_interval == 0
        )


        observation = env.reset()

        total_reward = 0
        done = False



        while not done:


            action = agent.choose_action(
                observation,
                training=not render
            )


            next_observation, reward, done = env.step(action)



            if render:

                env.render()

                pygame.time.delay(15)


                for event in pygame.event.get():

                    if event.type == pygame.QUIT:

                        pygame.quit()
                        exit()



            if not render:

                memory.add(
                    observation,
                    action,
                    reward,
                    next_observation,
                    done
                )


                if len(memory) > batch_size:

                    batch = memory.sample(batch_size)

                    loss = agent.train_step(batch)



            observation = next_observation

            total_reward += reward



        # epsilon decay inside generation

        if not render:

            agent.epsilon = max(
                0.1,
                agent.epsilon * 0.999
            )



        rewards.append(total_reward)



        # generation best

        if total_reward > generation_best:

            generation_best = total_reward
            generation_best_episode = episode + 1



        # global best across all runs

        if total_reward > global_best_reward:


            global_best_reward = total_reward

            global_best_generation = generation + 1
            global_best_episode = episode + 1


            torch.save(
                model.state_dict(),
                "models/best_model.pth"
            )


            with open(
                "data/best_score.pkl",
                "wb"
            ) as f:

                pickle.dump(
                    global_best_reward,
                    f
                )


            print(
                f"NEW GLOBAL RECORD: {global_best_reward:.2f}"
            )



        print(
            f"Gen {generation + 1}/{generations} | "
            f"Episode {episode + 1}/{episodes_per_generation} | "
            f"Reward {total_reward:.2f} | "
            f"Epsilon {agent.epsilon:.3f} | "
            f"Alive {env.time_alive}"
        )



    generation_time = time.time() - start_time

    total_training_time += generation_time



    print("\nGeneration complete")

    print(
        f"Time: {generation_time:.1f}s"
    )

    print(
        f"Generation best: {generation_best:.2f} "
        f"(Episode {generation_best_episode})"
    )



    # save generation checkpoint

    torch.save(
        model.state_dict(),
        f"models/generation_{generation + 1}.pth"
    )



    with open(
        f"data/rewards_generation_{generation + 1}.pkl",
        "wb"
    ) as f:

        pickle.dump(
            rewards,
            f
        )


    all_rewards.append(rewards)



# save all rewards

with open(
    "data/all_rewards.pkl",
    "wb"
) as f:

    pickle.dump(
        all_rewards,
        f
    )



print("\n========== Training finished ==========")


print(
    f"Total time: {total_training_time/60:.1f} minutes"
)


print(
    f"Best reward: {global_best_reward:.2f}"
)


print(
    f"Found in generation {global_best_generation}, "
    f"episode {global_best_episode}"
)


print(
    "Best model saved!"
)