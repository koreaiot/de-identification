from src.main.CheckException.exceptional import ChkException
import re


class deidentify_driver_license(ChkException):
    # 12-24-684532-16
    driver_license_regex = re.compile("((1[1-9])|(2[0-8]))[-]\d{2}[-]\d{6}[-]\d{2}")
    result_driver_license = []
    range_driver_license = []

    def find_driver_license(self):

        driver_license_in_sentence = deidentify_driver_license.driver_license_regex.search(self.sentence)
        if driver_license_in_sentence:
            deidentify_driver_license.result_driver_license.clear()
            deidentify_driver_license.range_driver_license.clear()
            return True
        else:
            return False

    def filter_driver_license(self, sentence_group):
        driver_license_group = sentence_group.group()
        driver_license_group_filter = driver_license_group.split("-")
        if deidentify_driver_license.chk_only_number(self, sentence_group) and \
                deidentify_driver_license.chk_arithmetic_sequence(self, driver_license_group_filter[2]):
            deidentify_driver_license.result_driver_license.append(driver_license_group)
            deidentify_driver_license.range_driver_license.append(sentence_group.span())
            return "-".join([driver_license_group_filter[0], "*"*2, "*"*6, "*"*2])
        else:
            return driver_license_group






