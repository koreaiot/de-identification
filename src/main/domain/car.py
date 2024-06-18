from src.main.CheckException.exceptional import ChkException
import re


class deidentify_car_number(ChkException):
    car_number_regex = re.compile("\d{2,3}[- ]*[가나다라마거너더러머버서어저고노도로모보소오조구누두루무부수우주바사아자배하허호육공해국합][- ]*\d{4}")
    result_car_number = []
    def find_car_number(self):

        car_number_in_sentence = deidentify_car_number.car_number_regex.search(self.sentence)
        if car_number_in_sentence:
            deidentify_car_number.result_car_number.clear()
            return True
        else:
            return False

    def filter_car_number(self, sentence_group):
        car_group = sentence_group.group()
        if deidentify_car_number.chk_only_number(self, sentence_group):
            car_group_filter = car_group.replace("-", "").replace(" ", "")
            deidentify_car_number.result_car_number.append(car_group)
            return "".join(["*" * 2, car_group_filter[2], "*" * 4])
        else:
            return car_group
