from Dev.DTOs import TemplateDTO
from Dev.DataAccessLayer.DAOs import TemplateDAO
from Dev.FingerprintGenerator import generator
from Dev.LogicLayer.LogicObjects.Asset import Asset


class Template(Asset):
    def __init__(self, path):
        super().__init__(path)

    def convert_to_image(self, minutiae_map_path: str, output_path: str):
        generator.generate()

    def to_dto(self) -> TemplateDTO:
        raise NotImplementedError

    def to_dao(self) -> TemplateDAO:
        raise NotImplementedError

    def __eq__(self, other):
        f1_min_content = []
        f1_xyt_content = []
        f2_min_content = []
        f2_xyt_content = []

        with open(self.path.join('.min')) as f:
            f1_min_content = f.readlines()

        with open(self.path.join('.xyt')) as f:
            f1_xyt_content = f.readlines()

        with open(other.__path.join('.min')) as f:
            f2_min_content = f.readlines()

        with open(other.__path.join('.xyt')) as f:
            f2_xyt_content = f.readlines()

        return (f1_min_content.sort() == f2_min_content.sort()) and (f1_xyt_content.sort() == f2_xyt_content.sort())
