from champsimextract.core import *
from champsimextract.misc.MetricAggr import MetricAggregator

def geometric_mean(values):
    """Calculates the geometric mean of a list of values."""
    product = 1.0
    n = len(values)
    for v in values:
        product *= v
    return product ** (1.0 / n)
def flat_split_list(parts:list,sep):
    """Splits a list of strings by a separator and flattens the result into a single list."""
    result = []
    for part in parts:
        result.extend(part.split(sep))
    return result

def flat_split_multi_sep(inp_str:str,sep:list[str]):
    """Splits a list of strings by a separator and flattens the result into a single list. 
    Splits based on list of seperators"""
    result = inp_str.split(sep[0])
    for s in sep[1:]:
        result = flat_split_list(result,s)
    return result
if __name__ == "__main__":
    ipc = BaseMetric(
        name="IPC",
        regex_pattern=r"CPU \d+ cumulative IPC:\s+([0-9]*\.[0-9]+).*"
    )
    speedup = BaselinedMetric(
        name="Speedup",
        base_metric=ipc,
        baseline_config=Configuration(
            name="4096",
            logdir="../data/LLC-Size/4096",
            get_workload_name_from_log_filename=lambda path: path.name.split('_')[2],
            get_simpoint_from_log_filename=lambda path: path.name.split('_')[0]
        )
    )
    exp = Experiment(
        name="Sample Experiment",
        configurations={
            "8MB": "../data/LLC-Size/8192",
            "16MB": "../data/LLC-Size/16384",
            "32MB": "../data/LLC-Size/32768",
        },
        get_workload_name_from_log_filename=lambda path: flat_split_multi_sep(path.name,sep=['.','-','_'])[2],
        get_simpoint_from_log_filename=lambda path: flat_split_multi_sep(path.name,sep=['.','-','_'])[3]
    )
    for config in exp.configurations:
        print(f"Configuration: {config.name}, Number of Logs: {len(config.logCollection.logs)}")
    agg = MetricAggregator(name="geomean",reducer=geometric_mean)
    print(exp.plot(speedup, agg, plot_type="line", ylabel="Speedup",base_color="orange" ,round_to=1,delta_round=0.01, delta_factor=1))
    print(exp.print_table(speedup, agg,latex=True))
    
