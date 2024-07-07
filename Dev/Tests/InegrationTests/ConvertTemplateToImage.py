import datetime
import os
import unittest

from Dev.DTOs import ImageDTO, TemplateDTO
from Dev.LogicLayer.Service.Service import Service
from TestUtils import images_path, templates_path


class ConvertImageToTemplate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = Service()
        # Create experiment
        cls.experiment_name = "IT_Experiment"
        create_experiment_response = cls.service.create_experiment(cls.experiment_name)
        if create_experiment_response.success:
            pass
        else:
            raise create_experiment_response.error

        # Set current experiment
        set_current_experiment_response = cls.service.set_current_experiment(cls.experiment_name)
        if set_current_experiment_response.success:
            pass
        else:
            raise set_current_experiment_response.error

    def test_convert_valid_image_to_template(self):
        valid_image = ImageDTO(
            path=os.path.join(images_path, '109_1_8bit.png'),
            date=datetime.datetime.now(),
            is_dir=False
        )

        response = self.service.convert_image_to_template(valid_image)
        assert response.success
        assert response.data is not None
        generated_template: TemplateDTO = response.data

        assert generated_template.path != ""

        xyt_template_file = os.path.join(generated_template.path, f"{os.path.basename(generated_template.path)}.xyt")
        min_template_file = os.path.join(generated_template.path, f"{os.path.basename(generated_template.path)}.xyt")

        assert os.path.exists(xyt_template_file) and os.path.exists(min_template_file)

        expected_template = TemplateDTO(path=os.path.join(templates_path, '109_1_8bit_template'),
                                        date=datetime.datetime.now(), is_dir=False)

        # assert generated_template == expected_template

    def test_convert_invalid_image_to_template(self):
        invalid_image = ImageDTO(
            path=os.path.join(images_path, 'bla.png'),
            date=datetime.datetime.now(),
            is_dir=False
        )

        response = self.service.convert_image_to_template(invalid_image)
        assert not response.success
        assert response.data is None

    @classmethod
    def tearDownClass(cls):
        response = cls.service.delete_experiment(cls.experiment_name)
        if not response.success:
            raise response.error


if __name__ == '__main__':
    unittest.main()
