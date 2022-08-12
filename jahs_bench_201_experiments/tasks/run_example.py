from jahs_bench.api import Benchmark
from jahs_bench.lib.core.configspace import joint_config_space


if __name__ == "__main__":

    DATASET = "cifar10"
    MODEL_PATH = "."
    NEPOCHS = 200
    N_ITERATIONS = 100

    benchmark = Benchmark(
            task=DATASET,
            save_dir=MODEL_PATH,
            kind="surrogate",
            download=True
        )

    # Random Search
    configs = []
    results = []
    for it in range(N_ITERATIONS + 1):
        # Use benchmark ConfigSpace object to sample a random configuration.
        config = joint_config_space.sample_configuration().get_dictionary()
        # Alternatively, define configuration as a dictionary.
        # config = {
        #     'Activation': 'Hardswish',
        #     'LearningRate': 0.014079762616015878,
        #     'Op1': 1,
        #     'Op2': 0,
        #     'Op3': 2,
        #     'Op4': 1,
        #     'Op5': 0,
        #     'Op6': 1,
        #     'Optimizer': 'SGD',
        #     'TrivialAugment': False,
        #     'WeightDecay': 0.0004672556521680262,
        #     'N': 1,
        #     'W': 4,
        #     'Resolution': 1.0
        # }
        result = benchmark(config, nepochs=NEPOCHS)

        configs.append(config)
        results.append(100 - float(result[NEPOCHS]["valid-acc"]))

    incumbent_idx = min(range(len(results)), key=results.__getitem__)
    incumbent = configs[incumbent_idx]
    incumbent_value = results[incumbent_idx]
    print(f"Incumbent: {incumbent} \n Incumbent Value: {incumbent_value}")
