"""Example script to compute and plot WQ_ROW_HITS for different LLC sizes.
This is a custom metric example which is not predefined in champsimextract.common.metrics.
Uses the GEOMEAN aggregator to compute the geometric mean WQ_ROW_HITS across workloads.
Plots the WQ_ROW_HITS as a bar chart and prints a LaTeX table of"""
from champsimextract.core import *
from champsimextract.common.aggregators import GEOMEAN
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
    speedup = BaseMetric(
        name="WQ_ROW_HITS",
        regex_pattern=r"\s+WQ\s+ROW_BUFFER_HIT:\s+(\d+)\s+ROW_BUFFER_MISS:\s+\d+\s+FULL:\s+\d+"
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
        
    exp.plot(speedup, GEOMEAN,savepath="temp.pdf",plot_type="bar", ylabel="WQ buffer hits",round_to=10000,ytick_rounding=0,delta_round=0.01, delta_factor=4*10000/32273.2)
    exp.print_table(speedup, GEOMEAN,latex=True)
    
