import pathlib
from dataclasses import dataclass
from traces import TraceCollection
from ChampsimLog import ChampsimLogCollection

@dataclass
class Configuration:
    name: str
    logs: ChampsimLogCollection

    def __init__(self, name: str, logdir: str):
        self.name = name
        self.logs = ChampsimLogCollection(log_dir=logdir)

@dataclass
class Experiment:
    name: str
    configurations: list[Configuration]

    def __init__(self, name: str, configurations: dict[str, str]):
        self.name = name
        self.configurations = []
        for config_name, logdir in configurations.items():
            config = Configuration(name=config_name, logdir=logdir)
            self.configurations.append(config)
    

if __name__ == "__main__":
    exp = Experiment(
        name="Sample Experiment",
        configurations={
            "ConfigA": "/mnt/d/CODE/RnD/results/LLC-Size/8192",
            "ConfigB": "/mnt/d/CODE/RnD/results/LLC-Size/4096"
        }
    )
    for config in exp.configurations:
        print(f"Configuration: {config.name}, Number of Logs: {len(config.logs.logs)}")