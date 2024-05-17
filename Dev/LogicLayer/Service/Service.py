from Dev.DTOs import OperationDTO, Response
from Dev.LogicLayer.Controllers.ConverterController import ConvertorController
from Dev.LogicLayer.Controllers.ExperimentController import ExperimentController
from Dev.LogicLayer.Controllers.MatcherController import MatcherController
from Dev.LogicLayer.Service.IService import IService


class Service(IService):

    def __init__(self):
        self.convertor_controller = ConvertorController()
        self.experiment_controller = ExperimentController()
        self.convertor_controller = MatcherController()

    def convert_template_to_image(self, template_path: str) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))
        
        
    def convert_image_to_template(self, image_path: str) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))

    def convert_image_to_3d_object(self, image_path: str) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))

    def match(self, templates_path1: tuple[str], templates_path2: tuple[str]) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))

    def get_experiments(self) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))
        
    def delete_experiment(self, experiment_id: int) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))

    def export_experiment(self, experiment_id: int) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))

    def rename_experiment(self, experiment_id: int, name: str) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))

    def create_experiment(self, name: str) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))

    def add_operation(self, experiment_id: int, operation: OperationDTO) -> Response:
        try:
            raise NotImplementedError
        except Exception as error:
            return Response(False, None, str(error))
