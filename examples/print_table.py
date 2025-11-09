"""
Example script to print a table of IPC for different LLC sizes.
Uses the AVERAGE aggregator to compute the average IPC across workloads.
Prints the table in LaTeX format.
"""
from champsimextract.core import *
from champsimextract.common.aggregators import AVERAGE

ipc = BaseMetric(
    name="IPC",
    regex_pattern=r"CPU \d+ cumulative IPC:\s+([0-9]*\.[0-9]+).*"
)

exp = Experiment(
    name="Table Example",
    configurations={
        "8MB": "../data/LLC-Size/8192",
        "16MB": "../data/LLC-Size/16384",
        "32MB": "../data/LLC-Size/32768",
    },
    get_workload_name_from_log_filename=lambda path: path.name.split('_')[2],
    get_simpoint_from_log_filename=lambda path: path.name.split('_')[0]
)


# Print table
print(exp.print_table(ipc, AVERAGE, latex=True))
