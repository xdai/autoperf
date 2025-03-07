import string

from .interface import AbstractAnalysis
from ..utils import config


class Analysis(AbstractAnalysis):
    '''
    This analysis top-level class relies on TAU's Jython analysis interface to
    the PerfExplorer Java analysis framework.
    '''

    def __init__(self, experiment):
        self.name = "metrics"
        self.longname = "Analyses.%s.%s" % (self.name, experiment.name)
        self.experiment = experiment

        self.longmetrics = config.get("%s.metrics" % self.longname, "").split()
        self.metrics = [m.partition('@')[0] for m in self.longmetrics]

        self.derived_metrics = dict()
        try:
            for name in config.get("%s.derived_metrics" % self.longname).split():
                self.derived_metrics[name] = config.get("%s.%s" % (self.longname, name))
                metrics = self.derived_metrics[name].translate(string.maketrans("()+-*/^", "       ")).split()
                for m in metrics:
                    try:
                        float(m)
                    except ValueError:
                        if m not in self.metrics:
                            self.metrics.append(m)
        except Exception:
            pass

    def run(self):
        # return # comment this line to run script below
        self.run_script("%s.py" % self.name,
                        TAULIB="%s/lib" % self.experiment.tauroot,
                        ppk="%s/data.ppk" % self.experiment.insname,
                        derived_metrics=repr(self.derived_metrics)
                        )
