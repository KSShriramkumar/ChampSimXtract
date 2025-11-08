from dataclasses import dataclass
from ChampsimLog import ChampsimLogCollection
from metrics import Metric,BaseMetric
@dataclass
class Configuration:
    name: str
    logCollection: ChampsimLogCollection

    def __init__(self, name: str, logdir: str,get_workload_name_from_path, get_simpoint_from_path):
        self.name = name
        self.logCollection = ChampsimLogCollection(log_dir=logdir)
        self.get_workload_name_from_path = get_workload_name_from_path
        self.get_simpoint_from_path = get_simpoint_from_path
    def get_data_dict(self, metric: Metric) -> dict:
        data = {}
        for log in self.logCollection.logs:
            if self.name not in data:
                data[self.name] = {}
            if self.get_workload_name_from_path(log.path) not in data[self.name]:
                data[self.name][self.get_workload_name_from_path(log.path)] = {}
            if self.get_simpoint_from_path(log.path) not in data[self.name]:
                data[self.name][self.get_workload_name_from_path(log.path)][self.get_simpoint_from_path(log.path)] = None
            data[self.name][self.get_workload_name_from_path(log.path)][self.get_simpoint_from_path(log.path)] = metric.get_val(log)
        return data
@dataclass
class Experiment:
    name: str
    configurations: list[Configuration]

    def __init__(self, name: str, configurations: dict[str, str],get_workload_name_from_path, get_simpoint_from_path):
        self.name = name
        self.configurations = []
        for config_name, logdir in configurations.items():
            config = Configuration(name=config_name, logdir=logdir, get_workload_name_from_path=get_workload_name_from_path, get_simpoint_from_path=get_simpoint_from_path)
            self.configurations.append(config)
    
    def get_data_dict(self,metric:Metric) -> dict:
        data = {}
        for config in self.configurations:
            data[config.name] = config.get_data_dict(metric)
        return data
    def __str__(self) -> str:
        return f"Experiment(name={self.name}, num_configurations={len(self.configurations)})"

if __name__ == "__main__":
    ipc = BaseMetric(
        name="IPC",
        regex_pattern=r"CPU \d+ cumulative IPC:\s+([0-9]*\.[0-9]+).*"
    )
    exp = Experiment(
        name="Sample Experiment",
        configurations={
            "ConfigA": "/mnt/d/CODE/RnD/results/LLC-Size/8192",
            "ConfigB": "/mnt/d/CODE/RnD/results/LLC-Size/4096"
        },
        get_workload_name_from_path=lambda path: path.name.split('_')[2],
        get_simpoint_from_path=lambda path: path.name.split('_')[3]
    )
    for config in exp.configurations:
        print(f"Configuration: {config.name}, Number of Logs: {len(config.logCollection.logs)}")
    print(exp.get_data_dict(ipc))