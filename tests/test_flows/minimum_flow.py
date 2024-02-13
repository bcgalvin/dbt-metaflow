from metaflow.decorators import step
from metaflow.flowspec import FlowSpec


class MinimumFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Flow is done!")
