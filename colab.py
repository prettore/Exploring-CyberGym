"""
colab.py — CybORG Cage 4 · Train & Evaluate on Google Colab
=============================================================

USAGE
-----
1. Open a new Google Colab notebook.
2. In the first cell, clone the repo and run this script:

    !git clone --recurse-submodules https://github.com/prettore/Exploring-CyberGym.git
    %cd Exploring-CyberGym
    %run colab.py

   OR copy-paste individual sections (marked with # %%) into separate cells.

3. After the script finishes, three files are automatically downloaded:
     graph.pkl   — network state snapshots for every evaluation step
     actions.pkl — per-step actions for every agent
     rewards.pkl — cumulative reward history per blue agent

4. On your local machine, drop those three files into:
     Exploring-CyberGym/WebGUI_dash/
   then launch the dashboard:
     cd WebGUI_dash && python index.py

CONFIGURATION — edit the values below before running.
"""

# =============================================================================
# %%  0. CONFIGURATION
# =============================================================================

TRAIN_STEPS      = 5        # Number of PPO training iterations
TRAIN_LR         = 0.0001   # Learning rate
TRAIN_BATCH_SIZE = 200      # Train batch size
EVAL_STEPS       = 50       # Number of evaluation steps (episode length)

# =============================================================================
# %%  1. INSTALL DEPENDENCIES
# =============================================================================
# This cell installs everything needed.  It will print a lot of output — that
# is normal.  If Colab asks you to restart the runtime, click "Restart" and
# then re-run from cell 2 onwards (skip this cell).

import subprocess, sys

def _pip(*args):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", *args])

print("Installing Ray RLlib …")
_pip("ray[rllib]", "torch", "--upgrade")

print("Installing CybORG cage-challenge-4 …")
subprocess.check_call(
    [sys.executable, "-m", "pip", "install", "-q", "-e",
     "Cage4/cage-challenge-4"],
    # cage-challenge-4 must be installed from its own directory
)

print("Installing remaining dashboard dependencies …")
_pip("plotly", "networkx", "numpy", "matplotlib")

print("\nAll dependencies installed.")

# =============================================================================
# %%  2. ENVIRONMENT SETUP
# =============================================================================

import os, sys, re, pickle

# Make sure CybORG and the visualiser module are importable
REPO_ROOT      = os.path.abspath(".")
CAGE4_DIR      = os.path.join(REPO_ROOT, "Cage4")
CHALLENGE_DIR  = os.path.join(CAGE4_DIR, "cage-challenge-4")
TESTING_DIR    = os.path.join(CAGE4_DIR, "Testing")
WEBGUI_DIR     = os.path.join(REPO_ROOT, "WebGUI_dash")

for path in [CHALLENGE_DIR, TESTING_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

os.makedirs(WEBGUI_DIR, exist_ok=True)

print(f"REPO_ROOT   : {REPO_ROOT}")
print(f"CHALLENGE   : {CHALLENGE_DIR}")
print(f"TESTING     : {TESTING_DIR}")
print(f"OUTPUT DIR  : {WEBGUI_DIR}")

# =============================================================================
# %%  3. TRAINING
# =============================================================================

from CybORG import CybORG
from CybORG.Simulator.Scenarios import EnterpriseScenarioGenerator
from CybORG.Agents.Wrappers import EnterpriseMAE
from CybORG.Agents import SleepAgent, EnterpriseGreenAgent, FiniteStateRedAgent

from ray.tune import register_env
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.policy.policy import PolicySpec
import ray

# Initialize Ray with local mode to prevent autoscaler warnings
ray.init(
    ignore_reinit_error=True,
    log_to_driver=False,
    _temp_dir="/tmp/ray",
    runtime_env={"env_vars": {"PYTHONWARNINGS": "ignore::DeprecationWarning"}}
)

NUM_AGENTS = 5
POLICY_MAP  = {f"blue_agent_{i}": f"Agent{i}" for i in range(NUM_AGENTS)}

def env_creator(env_config: dict):
    sg  = EnterpriseScenarioGenerator(
        blue_agent_class=SleepAgent,
        green_agent_class=EnterpriseGreenAgent,
        red_agent_class=FiniteStateRedAgent,
        steps=EVAL_STEPS,
    )
    cyborg = CybORG(scenario_generator=sg)
    return EnterpriseMAE(env=cyborg, agent_name="blue_agent")

register_env("CC4", lambda cfg: env_creator(cfg))
env = env_creator({})

def policy_mapper(agent_id, episode, worker, **kwargs):
    return POLICY_MAP[agent_id]

algo_config = (
    PPOConfig()
    .environment(env="CC4")
    .training(
        lr=TRAIN_LR,
        train_batch_size=TRAIN_BATCH_SIZE,
    )
    .multi_agent(
        policies={
            ray_agent: PolicySpec(
                policy_class=None,
                observation_space=env.observation_space(cyborg_agent),
                action_space=env.action_space(cyborg_agent),
                config={"gamma": 0.85},
            )
            for cyborg_agent, ray_agent in POLICY_MAP.items()
        },
        policy_mapping_fn=policy_mapper,
    )
    .env_runners(
        num_env_runners=0,  # Set to 0 to use local mode (no parallel workers)
        rollout_fragment_length=EVAL_STEPS,
    )
    .resources(
        num_cpus_per_worker=0,  # Disable CPU allocation for workers
        num_gpus_per_worker=0,  # Disable GPU allocation
    )
)

print(f"\nTraining for {TRAIN_STEPS} iteration(s) …")
algo = algo_config.build()
reward_log = []

for step in range(TRAIN_STEPS):
    results = algo.train()

    mean_reward = results.get("episode_reward_mean")
    if mean_reward is None and "env_runners" in results:
        mean_reward = results["env_runners"].get("episode_reward_mean", 0)
    if mean_reward is None:
        mean_reward = 0

    reward_log.append(mean_reward)
    print(f"  step {step + 1}/{TRAIN_STEPS}  |  mean_reward = {mean_reward:.4f}")

# Save checkpoint
results_dir  = os.path.join(REPO_ROOT, "results", "Cage4")
os.makedirs(results_dir, exist_ok=True)

existing = [f.name for f in os.scandir(results_dir) if f.is_dir()]
nums = [int(m.group(1)) for d in existing for m in [re.search(r"(\d+)$", d)] if m]
next_num = max(nums) + 1 if nums else 1
checkpoint_path = os.path.join(results_dir, f"training{next_num}")

algo.save(checkpoint_path)
print(f"\nCheckpoint saved → {checkpoint_path}")

# =============================================================================
# %%  4. EVALUATION
# =============================================================================

from ray.rllib.algorithms.algorithm import Algorithm
from VisualiseRedExpansionMod import VisualiseRedExpansionMod

print(f"\nEvaluating for {EVAL_STEPS} step(s) …")

# Re-register env with the correct step count (may already be registered)
try:
    register_env("CC4", lambda cfg: env_creator(cfg))
except Exception:
    pass

mae = env_creator({})
obs, _ = mae.reset()

algo_eval = Algorithm.from_checkpoint(checkpoint_path)

total          = {}
reward_history = {agent_id: [] for agent_id in POLICY_MAP}
visualise      = VisualiseRedExpansionMod(mae.env, EVAL_STEPS)

for i in range(EVAL_STEPS):
    actions = {
        agent_id: algo_eval.compute_single_action(
            agent_obs,
            policy_id=POLICY_MAP[agent_id],
            explore=False,
        )
        for agent_id, agent_obs in obs.items()
    }

    obs, rewards, dones, truncs, infos = mae.step(actions)

    for agent_id, reward in rewards.items():
        total[agent_id] = total.get(agent_id, 0) + reward

    for agent_id in POLICY_MAP:
        reward_history[agent_id].append(total.get(agent_id, 0))

    visualise.modified_run(mae.env)

    if (i + 1) % 10 == 0:
        print(f"  step {i + 1}/{EVAL_STEPS}")

collected_figures = visualise.get_figures()
all_actions       = visualise.all_actions

print("Evaluation complete.")

# =============================================================================
# %%  5. SAVE OUTPUT FILES
# =============================================================================

graph_path   = os.path.join(WEBGUI_DIR, "graph.pkl")
actions_path = os.path.join(WEBGUI_DIR, "actions.pkl")
rewards_path = os.path.join(WEBGUI_DIR, "rewards.pkl")

with open(graph_path,   "wb") as f: pickle.dump(collected_figures, f)
with open(actions_path, "wb") as f: pickle.dump(all_actions,       f)
with open(rewards_path, "wb") as f: pickle.dump(reward_history,    f)

print(f"\nOutput files written:")
print(f"    {graph_path}")
print(f"    {actions_path}")
print(f"    {rewards_path}")

# =============================================================================
# %%  6. DOWNLOAD FILES  (Colab only)
# =============================================================================
# This section uses the Colab file-download API.
# If you are running locally, the files are already in WebGUI_dash/ — skip this.

try:
    from google.colab import files as colab_files

    print("\nDownloading result files …")
    colab_files.download(graph_path)
    colab_files.download(actions_path)
    colab_files.download(rewards_path)
    print(
        "\n  Done!  Move the three downloaded .pkl files into your local\n"
        "    Exploring-CyberGym/WebGUI_dash/ directory, then run:\n\n"
        "        cd WebGUI_dash && python index.py\n\n"
        "    Select Cage4, choose the agent, and click Evaluate."
    )

except ImportError:
    print(
        "\nNot running in Google Colab — files are already saved to\n"
        f"   {WEBGUI_DIR}"
    )
