import os
from pathlib import Path
import cv2 as cv
import fingerprint_enhancer
from PIL import Image as PImage
from csdt_stl_converter import image2stl
from Dev.DTOs import ImageDTO
from Dev.DataAccessLayer.DAOs import ImageDAO
from Dev.LogicLayer.LogicObjects.Asset import Asset
from Dev.LogicLayer.LogicObjects.PrintingObject import PrintingObject
from Dev.LogicLayer.LogicObjects.Template import Template
from Dev.NBIS.NBIS import detect_minutiae
from Dev.Playground import PLAYGROUND


class Image(Asset):
    def __init__(self, path, is_dir):
        super().__init__(path, is_dir)

    def to_dto(self) -> ImageDTO:
        return ImageDTO(path=self.path, date=self.date, is_dir=self.is_dir)

    def to_dao(self) -> ImageDAO:
        raise NotImplementedError

    def finalize_path(self, final_destination_path: str):
        if os.path.exists(final_destination_path) and os.path.isdir(final_destination_path):
            super().path = final_destination_path
        else:
            raise Exception(f'Final Destination was not found {final_destination_path} does not exist')

    def __is_valid_image(self, file_path) -> bool:
        try:
            with PImage.open(file_path) as img:
                img.verify()
                return True
        except (IOError, SyntaxError):
            return False

    def convert_to_template(self) -> str:
        template_name = Path(self.path).stem
        template_path = os.path.join(PLAYGROUND().PATH, template_name)

        detect_minutiae(self.path, PLAYGROUND().PATH, template_name)

        return template_path

    def convert_to_printing_object(self) -> PrintingObject:
        printing_object_name = f"{Path(self.path).stem}.stl"
        printing_object_path = os.path.join(PLAYGROUND.PATH, printing_object_name)

        image = cv.imread(self.path, cv.IMREAD_GRAYSCALE)
        _, binary_image = cv.threshold(image, 128, 255, cv.THRESH_BINARY)

        enhanced_image = fingerprint_enhancer.enhance_Fingerprint(binary_image)

        depth = 0.05
        stl = image2stl.convert_to_stl(255 - enhanced_image, printing_object_path, base=True, output_scale=depth)
        with open(printing_object_name, 'wb') as f:
            f.write(stl)

        return PrintingObject(printing_object_path)
