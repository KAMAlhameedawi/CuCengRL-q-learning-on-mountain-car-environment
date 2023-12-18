import gym
import numpy as np
import matplotlib.pyplot as plt

class QLearningAgent:
    def __init__(self, state_space_size, action_space_size, learning_rate, discount_factor, exploration_rate):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.state_space_size = state_space_size
        self.action_space_size = action_space_size
        self.q_table = np.zeros((state_space_size, action_space_size))

    def discretize_state(self, state):
        # Convert the continuous state to a discrete state representation
        # Modify this according to the specifics of your state space
        discrete_state = tuple(state)
        return discrete_state

    def select_action(self, state):
        # Choose the action using epsilon-greedy strategy
        if np.random.rand() < self.exploration_rate:
            return np.random.randint(self.action_space_size)
        else:
            return np.argmax(self.q_table[state, :])

    def update_q_value(self, state, action, reward, next_state):
        # Update the Q-value using the Q-learning update rule
        best_next_action = np.argmax(self.q_table[next_state, :])
        self.q_table[state, action] += self.learning_rate * (
            reward + self.discount_factor * self.q_table[next_state, best_next_action] - self.q_table[state, action]
        )

def run_experiment(agent, env, num_episodes):
    episode_rewards = []

    for episode in range(num_episodes):
        state = agent.discretize_state(env.reset())
        total_reward = 0
        done = False

        while not done:
            action = agent.select_action(state)

            # Take action in the environment
            next_state, reward, done, _ = env.step(action)
            next_state = agent.discretize_state(next_state)

            # Ensure the action is within the valid range
            assert env.action_space.contains(action), f"Invalid action: {action}"

            # Update Q-value
            agent.update_q_value(state, action, reward, next_state)

            state = next_state
            total_reward += reward

        episode_rewards.append(total_reward)

    env.close()
    return episode_rewards

def plot_learning_curve(episode_rewards, lr, df, er):
    plt.plot(episode_rewards, label=f'LR={lr}, DF={df}, ER={er}')
    plt.xlabel('Episodes')
    plt.ylabel('Total Episode Reward')
    plt.title('Q-learning on Mountain Car Benchmark')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    state_space_size = 2  # Update this based on your state space
    action_space_size = 3  # Update this based on your action space

    learning_rates = [0.1, 0.5, 0.9]
    discount_factors = [0.1, 0.5, 0.9]
    exploration_rates = [0.1, 0.5, 0.9]

    for lr in learning_rates:
        for df in discount_factors:
            for er in exploration_rates:
                print(f"Running experiment with Learning Rate={lr}, Discount Factor={df}, Exploration Rate={er}")
                agent = QLearningAgent(state_space_size, action_space_size, lr, df, er)
                episode_rewards = run_experiment(agent, gym.make('MountainCar-v0'), num_episodes=1000)
                plot_learning_curve(episode_rewards, lr, df, er)
