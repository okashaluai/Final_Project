import os
import shutil
import unittest

from Dev.NBIS.NBIS import detect_minutiae, match_templates
from Dev.Tests.TestUtils import templates_path, images_path


class DetectingMinutiae(unittest.TestCase):
    def setUp(self):
        self.png1_24_bit_image_path = os.path.join(images_path, '1_24bit')
        self.png2_8_bit_image_path = os.path.join(images_path, '2_8bit')

        self.generated_templates_path = os.path.join(templates_path, 'Generated')

        if os.path.exists(self.generated_templates_path):
            shutil.rmtree(self.generated_templates_path)

        os.mkdir(self.generated_templates_path)

    def test_detect_minutiae_8bit(self):
        detect_minutiae(self.png2_8_bit_image_path, self.generated_templates_path)

        generated_templates_count = 0

        # Search for .min and .xyt for the expected template
        for template in os.listdir(self.generated_templates_path):
            if template.lower().startswith(os.path.basename(self.png2_8_bit_image_path)):
                generated_templates_count += 1

        assert generated_templates_count == 2

        # Check that .xyt file contains 99 minutiae
        with open(os.path.join(self.generated_templates_path,
                               f"{os.path.basename(self.png2_8_bit_image_path)}.xyt")) as t:
            minutiae_count = len(t.readlines())

        assert minutiae_count == 99

    def test_detect_minutiae_24bit(self):
        generated_templates_count = 0

        try:
            detect_minutiae(self.png1_24_bit_image_path, self.generated_templates_path)

            # Search for .min and .xyt for the expected template
            for template in os.listdir(self.generated_templates_path):
                if template.lower().startswith(os.path.basename(self.png1_24_bit_image_path)):
                    generated_templates_count += 1
        except:
            pass

        assert generated_templates_count == 0

    def tearDown(self):
        # Remove the expected template files if exists
        if os.path.exists(self.generated_templates_path):
            shutil.rmtree(self.generated_templates_path)


class MatchTemplates(unittest.TestCase):
    def setUp(self):
        self.same_person_template1_path = os.path.join(templates_path, '109_1_8bit', '109_1_8bit.xyt')
        self.same_person_template2_path = os.path.join(templates_path, '109_2_8bit', '109_2_8bit.xyt')
        self.same_person_template3_path = os.path.join(templates_path, '109_3_8bit', '109_3_8bit.xyt')

    def test_match_identical_templates(self):
        matching_score = match_templates(self.same_person_template1_path, self.same_person_template1_path)
        assert matching_score == 499

    def test_match_same_person_different_templates(self):
        matching_score_t1_t2 = match_templates(self.same_person_template1_path, self.same_person_template2_path)
        assert matching_score_t1_t2 == 27

        matching_score_t1_t3 = match_templates(self.same_person_template1_path, self.same_person_template3_path)
        assert matching_score_t1_t3 == 100

        matching_score_t2_t3 = match_templates(self.same_person_template2_path, self.same_person_template3_path)
        assert matching_score_t2_t3 == 32

    def test_match_invalid_templates(self):
        matching_score = None
        try:
            matching_score = match_templates(f"{self.same_person_template1_path}blabla",
                                             self.same_person_template1_path)
        except:
            pass

        assert matching_score is None


if __name__ == '__main__':
    unittest.main()
