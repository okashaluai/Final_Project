import csv
import os
from pathlib import Path

from Dev.LogicLayer.Matcher.Matcher import Matcher
from Dev.Utils import Singleton


class MatcherController(metaclass=Singleton):

    def __init__(self):
        self.matcher = Matcher()

    def match_one_to_one(self, template1_path: str, template2_path: str) -> int:
        matching_score = self.matcher.match_one_to_one(template1_path, template2_path)
        return matching_score

    def match_one_to_many(self, template_path: str, templates_dir_path: str) -> dict[str, dict[str, int]]:
        templates_path = []
        for t in os.listdir(templates_dir_path):
            templates_path.append(os.path.join(templates_dir_path, t))
        matching_score = self.matcher.match_one_to_many(template_path, templates_path)
        return matching_score

    def match_many_to_many(self, templates1_dir_path: str, templates2_dir_path: str) -> dict[str, dict[str, int]]:
        templates1_path = []
        templates2_path = []

        for t1 in os.listdir(templates1_dir_path):
            templates1_path.append(os.path.join(templates1_dir_path, t1))

        for t2 in os.listdir(templates2_dir_path):
            templates2_path.append(os.path.join(templates2_dir_path, t2))

        matching_score = self.matcher.match_many_to_many(templates1_path, templates2_path)
        return matching_score

    def export_matrix_score_as_csv(self, score, export_full_path: str):
        with open(export_full_path, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            scores_row_entry = dict()

            for i, t1_path in enumerate(score.keys()):
                row_entry = []
                scores_row_entry[i + 1] = []

                for t2_path in score[t1_path].keys():
                    row_entry.append(Path(t2_path).stem)
                    scores_row_entry[i + 1].append(score[t1_path][t2_path])

                if i == 0:
                    row_entry = [''] + row_entry
                elif i < len(score.keys()):
                    row_entry = [Path(list(score.keys())[i - 1]).stem] + scores_row_entry[i]

                writer.writerow(row_entry)

            last_row = [Path(list(score.keys())[i]).stem] + scores_row_entry[i + 1]
            writer.writerow(last_row)


if __name__ == '__main__':
    mc = MatcherController()
    score = mc.match_many_to_many(
        r"C:\Users\Yazan\Desktop\t1",
        r"C:\Users\Yazan\Desktop\t1"
    )
    print(score)
    mc.export_matrix_score_as_csv(score, r"C:\Users\Yazan\Desktop\myscores.csv")
