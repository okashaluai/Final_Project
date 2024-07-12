import os

from Dev.LogicLayer.LogicObjects.Asset import Asset
from Dev.LogicLayer.LogicObjects.Experiment import Experiment
from Dev.LogicLayer.LogicObjects.Operation import Operation
from Dev.Utils import Singleton
from Dev.DataAccessLayer.FILESYSTEM import FILESYSTEM
from datetime import datetime


class ExperimentController(metaclass=Singleton):

    def __init__(self):
        self.current_experiment_name = None
        self.experiments: dict[str, Experiment] = dict()  # <Key: experiment_name, Value: Experiment>
        self.__filesystem: FILESYSTEM = FILESYSTEM()
        self.load_experiments()

    def add_operation(self, operation: Operation):
        if self.current_experiment_name is None:
            raise Exception('No current experiment is defined!')
        self.__filesystem.register_operation_metadata(self.current_experiment_name, operation.to_dto())
        return self.experiments[self.current_experiment_name].add_convert_operation(operation)

    def get_experiments(self):
        return self.experiments.values()

    def delete_experiment(self, experiment_name: str):
        if experiment_name in self.experiments:
            del self.experiments[experiment_name]
            self.__filesystem.delete_experiment_dir(experiment_name)
        else:
            raise Exception(f'Experiment with name {experiment_name} does not exist!')

    def get_sorted_experiments_by_date(self):
        return sorted(self.experiments.values(), key=lambda experiment: experiment.experiment_date)

    def export_experiment(self, experiment_name: str, export_path: str):
        raise NotImplementedError

    def revert_operation(self, operation_id: str):
        self.__filesystem.delete_operation_dir(self.current_experiment_name, operation_id)

    def load_experiments(self):
        experiment_dtos = self.__filesystem.load_experiments()
        for experiment_dto in experiment_dtos:
            operations: dict[str: Operation] = dict()
            for operation_dto in experiment_dto.operations:
                input_asset = Asset(path=operation_dto.operation_input.path,
                                    is_dir=operation_dto.operation_input.is_dir)
                output_asset = Asset(path=operation_dto.operation_output.path,
                                     is_dir=operation_dto.operation_output.is_dir)
                operation = Operation(operation_id=operation_dto.operation_id,
                                      operation_type=operation_dto.operation_type,
                                      operation_datetime=operation_dto.operation_datetime,
                                      operation_input=input_asset,
                                      operation_output=output_asset)
                operations[operation.operation_id] = operation
            experiment = Experiment(experiment_name=experiment_dto.experiment_name,
                                    experiment_datetime=experiment_dto.experiment_datetime,
                                    operations=operations)
            self.experiments[experiment_dto.experiment_name] = experiment

    def rename_experiment(self, experiment_name: str, new_experiment_name: str):
        if experiment_name in self.experiments:
            self.experiments[experiment_name].rename_experiment(new_experiment_name)
            return self.experiments[experiment_name]
        else:
            raise Exception(f'Experiment with name {experiment_name} does not exist!')

    def create_experiment(self, experiment_name: str):

        if experiment_name in self.experiments:
            raise Exception(f'Experiment with name {experiment_name} already exists!')

        self.__filesystem.create_experiment_dir(experiment_name=experiment_name)

        new_experiment = Experiment(experiment_name, datetime.now())
        self.experiments[experiment_name] = new_experiment

        return self.experiments[experiment_name]

    def set_current_experiment(self, current_experiment_name: str) -> Experiment:
        if current_experiment_name in self.experiments:
            self.current_experiment_name = current_experiment_name
            return self.experiments[self.current_experiment_name]
        else:
            raise Exception(f'Experiment with name {current_experiment_name} does not exist!')

    def import_templates(self, templates_path: str, operation_id: str):
        experiment_name = self.experiments.get(self.current_experiment_name).experiment_name

        if os.path.isfile(templates_path):
            self.__filesystem.import_template_into_dir(templates_path, experiment_name, operation_id)
        elif os.path.isdir(templates_path):
            self.__filesystem.import_templates_dir(templates_path, experiment_name, operation_id)

        else:
            raise Exception(f"{templates_path} does not exist or is not a valid path.")

    def import_images(self, images_path: str, operation_id: str):
        experiment_name = self.experiments.get(self.current_experiment_name).experiment_name
        if os.path.isfile(images_path):
            self.__filesystem.import_image_into_dir(images_path, experiment_name, operation_id)
        elif os.path.isdir(images_path):
            self.__filesystem.import_images_dir(images_path, experiment_name, operation_id)
        else:
            raise Exception(f"{images_path} does not exist or is not a valid path.")

    def get_current_experiment(self) -> Experiment:
        if self.current_experiment_name in self.experiments:
            return self.experiments[self.current_experiment_name]
        else:
            raise Exception(f'There is no current experiment!')

    def delete_operation(self, experiment_name: str, operation_id: str):
        if experiment_name not in self.experiments.keys():
            raise Exception(f'Experiment with name {self.current_experiment_name} does not exist!')
        if operation_id not in self.experiments[experiment_name].operations.keys():
            raise Exception(f'Operation with id {self.current_experiment_name} does not exist!')
        else:
            self.experiments[experiment_name].remove_operation(operation_id)
            self.__filesystem.delete_operation_dir(experiment_name, operation_id)