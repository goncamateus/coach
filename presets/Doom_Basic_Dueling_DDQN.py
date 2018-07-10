from agents.ddqn_agent import DDQNAgentParameters
from architectures.tensorflow_components.heads.dueling_q_head import DuelingQHeadParameters
from environments.environment import SelectedPhaseOnlyDumpMethod, MaxDumpMethod
from graph_managers.basic_rl_graph_manager import BasicRLGraphManager
from graph_managers.graph_manager import ScheduleParameters
from base_parameters import VisualizationParameters
from core_types import TrainingSteps, EnvironmentEpisodes, EnvironmentSteps, RunPhase
from environments.doom_environment import DoomEnvironmentParameters
from memories.memory import MemoryGranularity
from schedules import LinearSchedule


####################
# Graph Scheduling #
####################

schedule_params = ScheduleParameters()
schedule_params.improve_steps = TrainingSteps(10000000000)
schedule_params.steps_between_evaluation_periods = EnvironmentEpisodes(50)
schedule_params.evaluation_steps = EnvironmentEpisodes(3)
schedule_params.heatup_steps = EnvironmentSteps(1000)


#########
# Agent #
#########
agent_params = DDQNAgentParameters()
agent_params.memory.max_size = (MemoryGranularity.Transitions, 5000)
agent_params.network_wrappers['main'].learning_rate = 0.00025
agent_params.algorithm.num_steps_between_copying_online_weights_to_target = EnvironmentSteps(1000)
agent_params.exploration.epsilon_schedule = LinearSchedule(0.5, 0.01, 50000)
agent_params.exploration.evaluation_epsilon = 0
agent_params.algorithm.num_consecutive_playing_steps = EnvironmentSteps(1)
agent_params.network_wrappers['main'].replace_mse_with_huber_loss = False
agent_params.network_wrappers['main'].heads_parameters = [DuelingQHeadParameters()]

###############
# Environment #
###############
env_params = DoomEnvironmentParameters()
env_params.level = 'basic'

vis_params = VisualizationParameters()
vis_params.video_dump_methods = [SelectedPhaseOnlyDumpMethod(RunPhase.TEST), MaxDumpMethod()]
vis_params.dump_mp4 = False

graph_manager = BasicRLGraphManager(agent_params=agent_params, env_params=env_params,
                                    schedule_params=schedule_params, vis_params=vis_params)