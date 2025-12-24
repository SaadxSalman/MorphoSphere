# Gemini-Game 🎮

An AI agent for video games that learns and adapts like a human player. Gemini-Game doesn't rely on scripted behavior but develops its own strategies, providing a truly dynamic and unpredictable opponent that offers a fresh challenge with every playthrough.

-----

## ✨ Features

  * **Human-like Adaptability:** Learns from gameplay experience to develop new strategies and counter-tactics.
  * **Perceptual Awareness:** A **Perception Agent** uses a **vision model** to directly interpret the game state from the screen, making it game-engine independent.
  * **Strategic Planning:** A **Strategy Agent** uses a large-scale model like **Gemma-3** for high-level strategic planning and decision-making.
  * **Reinforcement Learning:** A **Learning Agent** updates the model based on the outcomes of its actions, improving its performance over time.
  * **High-Performance Execution:** The core logic is built with **Rust** for real-time, low-latency execution, ensuring the agent can keep up with fast-paced games.
  * **Vector-Based State Representation:** Creates a specialized **embedding space** for game states and actions, facilitating efficient reinforcement learning.

-----

## ⚙️ Tech Stack

  * **Core Logic:** Rust
  * **Learning Framework:** GRPO (Generalized Policy Iteration)
  * **High-Level Strategy:** Gemma-3
  * **Vision Model:** Custom-trained vision model
  * **Embeddings:** Custom embeddings model

-----

## 🚀 Getting Started

### Prerequisites

  * Rust
  * Python 3.10+ (for training and model inference)
  * Access to the Gemma-3 model

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/saadsalmanakram/Gemini-Game.git
    cd Gemini-Game
    ```
2.  **Build the Rust core:**
    ```bash
    cargo build --release
    ```
3.  **Set up the training environment:**
    Follow the instructions in the `training/` directory to install the necessary Python libraries and configure the reinforcement learning environment.

### Configuration

Create a `.env` file to store API keys and other environment variables required for running the agent.

### Usage

Run the main executable and point it to the game's video stream to begin the real-time analysis and gameplay.

-----

