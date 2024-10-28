import random
import time
from datetime import datetime, timedelta

import gymnasium
from gymnasium.envs.registration import register

from vita.simulator.blood_glucose_producer import BloodGlucoseProducer

# Loop to simulate a full day (or multiple episodes if needed)
hours_per_episode = 24  # Number of hours to simulate in each episode
minutes_per_step = 3  # Time increment per step, as in the logs

# Number of steps per episode to cover `hours_per_episode` hours
steps_per_episode = (hours_per_episode * 60) // minutes_per_step

# Set max_episode_steps based on desired length of episode
bg_producer = BloodGlucoseProducer()

reference_time = datetime.now()

episode = 1

all_names_list = [
    'adolescent#001', 'adolescent#002', 'adolescent#003', 'adolescent#004',
    'adolescent#005', 'adolescent#006', 'adolescent#007', 'adolescent#008',
    'adolescent#009', 'adolescent#010', 'adult#001', 'adult#002', 'adult#003',
    'adult#004', 'adult#005', 'adult#006', 'adult#007', 'adult#008',
    'adult#009', 'adult#010', 'child#001', 'child#002', 'child#003',
    'child#004', 'child#005', 'child#006', 'child#007', 'child#008',
    'child#009', 'child#010'
]

while True:
    chosen_string = random.choice(all_names_list)
    experiment_id = "simglucose/adolescent2-v0"
    register(
        id=experiment_id,
        entry_point="simglucose.envs:T1DSimGymnaisumEnv",
        max_episode_steps=80,  # Increase this value to cover more time in one episode
        kwargs={"patient_name": chosen_string},
    )

    env = gymnasium.make(experiment_id, render_mode="human")
    env.spec.max_episode_steps = steps_per_episode

    observation, info = env.reset()
    t = 0
    while True:
        env.render()
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        blood_time = reference_time + timedelta(minutes=minutes_per_step)
        data = {
            "bg": float(observation[0]),
            "ts": blood_time.timestamp(),
        }
        bg_producer.send_blood_glucose(data)

        t += 1
        time.sleep(2)
        # If the episode is finished, either due to 'terminated' or 'truncated'
        if terminated or truncated:
            print(f"[{current_time}] Episode {episode} finished after {t} timesteps")
            env.render()
            break
        minutes_per_step += 3

    # Move to the next episode to simulate more data along the day
    episode += 1

