import os

from Dev.Enums import OperationType
from Dev.LogicLayer.Controllers.ExperimentController import ExperimentController
from Dev.LogicLayer.LogicObjects.Image import Image
from Dev.LogicLayer.LogicObjects.PrintingObject import PrintingObject
from Dev.LogicLayer.LogicObjects.Template import Template
from Dev.Utils import Singleton
from Dev.FingerprintGenerator.generator import generate
from Dev.LogicLayer.LogicObjects.Operation import Operation
from Dev.Playground import PLAYGROUND


class ConvertorController(metaclass=Singleton):

    def __init__(self):
        self.__experiment_controller = ExperimentController()  # this behavior indicates high coupling and low cohesion (we should reconsider it).
        self._playground = PLAYGROUND()
        self.__min_maps_cache: dict[str, str] = dict()

    def convert_template_to_min_map_image(self, template: Template):
        min_map_image_path = ''
        if template.path in self.__min_maps_cache:
            min_map_image_path = self.__min_maps_cache.get(template.path)
        else:
            min_map_image_path = template.convert_to_min_map_image()
            self.__min_maps_cache[template.path] = min_map_image_path
        min_map_image = Image(min_map_image_path, is_dir=False)
        return min_map_image

    def convert_template_to_image(self, template: Template, experiment_name: str, operation_id: str) -> Image:
        generated_image_path = template.convert_to_image(experiment_name, operation_id)
        generated_image = Image(generated_image_path, template.is_dir)
        return generated_image

    def convert_image_to_template(self, image: Image, experiment_name: str, operation_id: str) -> Template:
        template_path = image.convert_to_template(experiment_name, operation_id)
        extracted_template = Template(template_path, image.is_dir)
        return extracted_template

    def convert_image_to_printing_object(self, image: Image) -> PrintingObject:

        printing_object = image.convert_to_printing_object()
        return printing_object