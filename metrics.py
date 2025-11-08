import re
from ChampsimLog import ChampsimLog

class Metric:
    def get_val(self,log:ChampsimLog):
        raise NotImplementedError("Subclasses must implement get_val method")
class BaseMetric(Metric):
    '''A base metric defined by a regex pattern to extract a value from a Champsim log.'''
    def __init__(self,name:str,regex_pattern:str) -> None:
        self.pattern = re.compile(regex_pattern)
        self.name = name
    def get_val(self,log:ChampsimLog):
        match = self.pattern.search(log.get_log_text())
        if not match:
            raise ValueError(f"Metric pattern {self.name} did not match log {log.path}")
        elif len(match.groups()) > 1:
            raise ValueError(f"Metric pattern {self.name} has more than one capturing group in log {log.path}")
        elif len(match.groups()) == 1:
            return match.groups()[0]
        return None

class CustomMetric(Metric):
    '''A metric defined by multiple base metrics and a processing function.
    The processing function takes as input the raw values extracted by each base metric
    and returns the final value of the custom metric. The order of metrics in the list and processing
    function arguments must match.'''
    def __init__(self,metrics:list[BaseMetric],process_func) -> None:
        self.metrics = metrics
        self.process_func = process_func
    def get_val(self,log:ChampsimLog):
        raw_values = [metric.get_val(log) for metric in self.metrics]
        return self.process_func(*raw_values)