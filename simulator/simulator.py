import time
from datetime import datetime

import gymnasium
from gymnasium.envs.registration import register
from kafka_client import send, stop_producer

register(
    id="simglucose/adolescent2-v0",
    entry_point="simglucose.envs:T1DSimGymnaisumEnv",
    max_episode_steps=480,  # Increase this value to cover more time in one episode
    kwargs={"patient_name": "adolescent#002"},
)

env = gymnasium.make("simglucose/adolescent2-v0", render_mode="human")

# Loop to simulate a full day (or multiple episodes if needed)
hours_per_episode = 24  # Number of hours to simulate in each episode
minutes_per_step = 3  # Time increment per step, as in the logs

# Number of steps per episode to cover `hours_per_episode` hours
steps_per_episode = (hours_per_episode * 60) // minutes_per_step

# Set max_episode_steps based on desired length of episode
env.spec.max_episode_steps = steps_per_episode

episode = 1
while True:
    observation, info = env.reset()
    t = 0
    while True:
        # env.render()
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"[{current_time}] Episode {episode} - Step {t}: observation {observation}, reward {reward}, terminated {terminated}, truncated {truncated}, info {info}"
        )
        send(observation[0], ts=info["time"].timestamp())

        t += 1
        time.sleep(2)
        # If the episode is finished, either due to 'terminated' or 'truncated'
        if terminated or truncated:
            print(f"[{current_time}] Episode {episode} finished after {t} timesteps")
            break

    # Move to the next episode to simulate more data along the day
    episode += 1

    # Add a break condition if needed (e.g., stop after a full day or a set number of episodes)
    # Simulate data for 7 consecutive episodes (representing a week, for example)
    if episode > 7:
        break

stop_producer()
