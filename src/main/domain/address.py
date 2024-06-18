from src.main.CheckException.exceptional import ChkException
from src.main.setting_variable import lot_number_address, road_name_address
import re


def address_masking(sentence_group):
    address_group = sentence_group.group()
    return "*" * len(address_group)


class deidentify_address(ChkException):
    # regex_str = "([가-힣]+(시|도)|서울|인천|대구|광주|부산|울산)+( |)([가-힣]+(시|군|구))" +\
    #             "|(([가-힣A-Za-z·\d~\-\.]{2,}(로|길).[\d]+)" + \
    #             "|([가-힣A-Za-z·\d~\-\.]+(읍|동|번지/면/가/리)\s)[\d]+)" + \
    #             "|([가-힣A-Za-z]+(구)+\s*[가-힣A-Za-z]+(동))" + \
    #             "|([가-힣a-zA-Z\d]+(아파트|빌라|빌딩|마을))"

    regex_str = "(서울(?:시|특별시)?|(경기|강원)(?:도)?|(광주|대구|대전|부산|울산|인천)(?:광역시|시)?|제주(?:도|특별자치도)?|(경상|전라|충청)(:?도|북도|남도)|경남|충남|전남|전북|충북|경북)?( |)(([가-힣]+시( |)[가-힣]+구)|([가-힣]+(시|군|구)))( |)(([가-힣]+(읍|면)( |)[가-힣\d]+(로|길)|[가-힣\d]+(길|로))|(([가-힣]+(읍|면)( |)[가-힣]+리)|(([가-힣]+(읍|면|리))|([가-힣\d]+동))))( |)(\d{1}가|산)?( |)(\d{1,5}(?:-\d{1,5})?(길|번길|사길|,)?)?( |)(([0-9 a-zA-Z가-힣]{0,20}(?:(빌딩|아파트|파크빌|타워|빌라|마을|교회|단지|번지|학교|상가|오피스텔)))?)( |)([0-9]+층)?([0-9, A-Z]+동)?([0-9 ]{1,10}호)?( |)([(](.*)[)])?"
    # ([(\[]?((우\.?)?\d+(\-\d+)?)[)\]]?)?( |)  <-- 주소 앞 우편번호는 지움 얘를 살리면 문제가 됨.
    address_regex = re.compile(regex_str)
    # address_regex = re.compile('([가-힣]+(시|도)|서울|인천|대구|광주|부산|울산)+( |)([가-힣]+(시|군|구))( |)([가-힣0-9.]+(구|길|로|읍|면|동|가|리))')
    # address_regex = re.compile("(([가-힣]+(시|군|구))( |)([가-힣0-9.]+(구|길|로|읍|면|동|가|리)))( |)(([가-힣](읍|면)( |)[가-힣]리)|([가-힣]+(동|읍|면|리)))")
    result_address = []
    range_address = []

    def find_address(self):

        address_in_sentence = deidentify_address.address_regex.search(self.sentence)
        if address_in_sentence:
            deidentify_address.result_address.clear()
            deidentify_address.range_address.clear()
            return True
        else:
            return False

    def filter_address(self, sentence_group) -> str:
        """
            state: 시도, county: 시군구, city, town, village
        """
        address_group = sentence_group.group()
        address_group_strip = address_group.strip()
        sido_comp = address_group_strip[:2]

        if sido_comp == "경북":
            sido_comp = "경상북도"
        if sido_comp == "경남":
            sido_comp = "경상남도"
        if sido_comp == "충북":
            sido_comp = "충청북도"
        if sido_comp == "충남":
            sido_comp = "충청남도"
        if sido_comp == "전북":
            sido_comp = "전라북도"
        if sido_comp == "전남":
            sido_comp = "전라남도"

        for siDo in lot_number_address.keys():
            if sido_comp in siDo:  # 주소에 시도가 있을 때,
                for siGunGu in lot_number_address[siDo].keys(): # 시군구 (지번, 도로명 같음)
                    if siGunGu in address_group:
                        for eupMyeonDong in lot_number_address[siDo][siGunGu]: # 지번
                            if eupMyeonDong in address_group:
                                # 읍면동 기준으로 before, after 나누기. after는 비식별화 대상.
                                address_before = "".join([address_group.split(eupMyeonDong)[0], eupMyeonDong])
                                address_after = address_group.split(eupMyeonDong)[1]
                                if len(address_after) <= 1:
                                    return address_group
                                else:  # after 있으면, **빌딩, **아파트, 모든 숫자 전부 *처리,
                                    deidentify_address.result_address.append(address_group)
                                    deidentify_address.range_address.append(sentence_group.span())
                                    address_after_regex = "(([a-zA-Z가-힣]+(?=(길|동|로|빌딩|아파트|파크빌|타워|빌라|마을|교회|단지|번지|학교|상가|오피스텔))))|([0-9])+"
                                    address_after_deidentify = re.sub(address_after_regex, address_masking, address_after)
                                    return "".join([address_before, address_after_deidentify])

                            # elif re.sub("[0-9]", "", eupMyeonDong) in address_group: # 양평1동을 양평동으로 바꾸고 할라 하는데 잘 안되는 듯
                            #     eupMyeonDong_no_num = re.sub("[0-9]", "", eupMyeonDong)
                            #     address_before = "".join([address_group.split(eupMyeonDong_no_num)[0], eupMyeonDong_no_num])
                            #     address_after = address_group.split(eupMyeonDong_no_num)[1]
                            #     if len(address_after) <= 1:
                            #         return address_group
                            #     else:
                            #         deidentify_address.result_address.append(address_group)
                            #         deidentify_address.range_address.append(sentence_group.span())
                            #         tmp_regex = "(([a-zA-Z가-힣]+(?=(길|동|로|빌딩|아파트|파크빌|타워|빌라|마을|교회|단지|번지|학교|상가|오피스텔))))|([0-9])+"
                            #         tmp_sentence = re.sub(tmp_regex, address_masking, address_after)
                            #         return "".join([address_before, tmp_sentence])

                        for road_name in road_name_address[siDo][siGunGu]: # 도로명
                            if road_name in address_group:
                                # 도로명 기준으로 before, after 나누기. after는 비식별화 대상.
                                address_before = "".join([address_group.split(road_name)[0], road_name])
                                address_after = address_group.split(road_name)[1]
                                if len(address_after) <= 1:
                                    return address_group
                                else:
                                    deidentify_address.result_address.append(address_group)
                                    deidentify_address.range_address.append(sentence_group.span())
                                    address_after_regex = "(([a-zA-Z가-힣]+(?=(길|동|로|빌딩|아파트|파크빌|타워|빌라|마을|교회|단지|번지|학교|상가|오피스텔))))|([0-9])+"
                                    address_after_deidentify = re.sub(address_after_regex, address_masking, address_after)
                                    return "".join([address_before, address_after_deidentify])

        else:
            # 주소에 시도가 없을 때, 얘를 하면 "일산동구청쪽으로", "남동구 간석동" 이것까지 필터 됨..
            # 동구를 찾으면 거기서 자르고, 그 뒤에서만 검색하고,
            # 시군구-읍면동라인을 발견했을 때, Flag를 줘서 if문으로 검사하기(시간 줄여)
            for siDo in lot_number_address.keys():
                for siGunGu in lot_number_address[siDo].keys(): # 시군구 (지번, 도로명 같음)
                    if siGunGu in address_group:
                        print("siGunGu : ", siGunGu)
                        for eupMyeonDong in lot_number_address[siDo][siGunGu]: # 지번
                            if eupMyeonDong in address_group:
                                print("eupMyeonDong :", eupMyeonDong)
                                # 읍면동 기준으로 before, after 나누기. after는 비식별화 대상.
                                address_before = "".join([address_group.split(eupMyeonDong)[0], eupMyeonDong])
                                address_after = address_group.split(eupMyeonDong)[1]
                                if len(address_after) <= 1:
                                    return address_group
                                else:  # after 있으면, **빌딩, **아파트, 모든 숫자 전부 *처리,
                                    deidentify_address.result_address.append(address_group)
                                    deidentify_address.range_address.append(sentence_group.span())
                                    address_after_regex = "(([a-zA-Z가-힣]+(?=(길|동|로|빌딩|아파트|파크빌|타워|빌라|마을|교회|단지|번지|학교|상가|오피스텔))))|([0-9])+"
                                    address_after_deidentify = re.sub(address_after_regex, address_masking, address_after)
                                    return "".join([address_before, address_after_deidentify])

                        for road_name in road_name_address[siDo][siGunGu]: # 도로명
                            if road_name in address_group:
                                # 도로명 기준으로 before, after 나누기. after는 비식별화 대상.
                                address_before = "".join([address_group.split(road_name)[0], road_name])
                                address_after = address_group.split(road_name)[1]
                                if len(address_after) <= 1:
                                    return address_group
                                else:
                                    deidentify_address.result_address.append(address_group)
                                    deidentify_address.range_address.append(sentence_group.span())
                                    address_after_regex = "(([a-zA-Z가-힣]+(?=(길|동|로|빌딩|아파트|파크빌|타워|빌라|마을|교회|단지|번지|학교|상가|오피스텔))))|([0-9])+"
                                    address_after_deidentify = re.sub(address_after_regex, address_masking, address_after)
                                    return "".join([address_before, address_after_deidentify])
        return address_group