from .step import Step


class Preflight(Step):
    def process(self, data, inputs, utils):
        print('In Preflight')
        utils.create_dirs()
