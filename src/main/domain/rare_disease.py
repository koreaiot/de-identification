from src.main.CheckException.exceptional import ChkException
import re


class deidentify_rare_disease(ChkException):
    str_regex = "(강직성 척추염|강직인간증후군|거대백악종|고양이 울음 증후군|공뇌증|근위축성측색경화증|기면증|기텔만 증후군|낫 모양 적혈구 증후군|누난 " \
                "증후군|다발경화증|다지증|단안기형|담도폐쇄증|돌발운동유발 이상운동증|동공과다증|라론 증후군|라이 증후군|람베르트-이튼 근무력증후군|레쉬-니한 증후군|레이노 증후군|레트 증후군|로하드 " \
                "증후군|루푸스|류마티스성 다발근통|마들룽|마르팡 증후군|멘케스 증후군|묘안 증후군|무뇌수두증|무뇌증|백색증|버거씨병|버드 키아리 증후군|베게너육아종증|베르니케-코르사코프 " \
                "증후군|베체트병|복합부위 통증 증후군|부신백질이영양증|분열뇌증|블룸 증후군|비주얼스노우|색소 융모 결절성 활액막염|샤르코-마리-투스 병|서번트 증후군|선천 부신 과다형성|선천성 경상 " \
                "증후군|선천성 다감증|선천성 면역 결핍 증후군|선천성 무통각증 및 무한증|선천성 횡격막 탈장증|섬유성 골이형성증|셀리악병|수분성 알레르기|스티븐스-존슨 증후군|심장암|아동기 붕괴성 " \
                "장애|안드로겐 무감응 증후군|에드워드 증후군|엔젤만 증후군|엘러스-단로스 증후군|왓슨 증후군|용혈성 요독 증후군|원발 경화 쓸개관염|원발성 왜소증|윌리엄스 " \
                "증후군|윌슨병|유전성혈관부종|조로증|중증근무력증|진행성 골화성 섬유형성이상|척 스트라우스 증후군|초남성 증후군|치명적 가족성 불면증|카일러 증후군|코타르 " \
                "증후군|쿠루병|크론병|키엔벡병|타카야스 동맥염|태아 알코올 증후군|터너 증후군|털곰팡이증|투렛 증후군|트리메틸아민뇨증|트리처 콜린스 증후군|파브리병|파타우 " \
                "증후군|페닐케톤뇨증|포피리아|프라더-윌리 증후군|할리퀸 어린선|헌팅턴 무도병|혈구탐식성 림프조직구증)"

    rare_disease_regex = re.compile(str_regex)
    result_rare_disease = []
    range_rare_disease = []

    def find_rare_disease(self):

        rare_disease_in_sentence = deidentify_rare_disease.rare_disease_regex.search(self.sentence)
        if rare_disease_in_sentence:
            deidentify_rare_disease.result_rare_disease.clear()
            deidentify_rare_disease.range_rare_disease.clear()
            return True
        else:
            return False

    def filter_rare_disease(self, sentence_group):
        rare_disease_group = sentence_group.group()
        deidentify_rare_disease.result_rare_disease.append(rare_disease_group)
        deidentify_rare_disease.range_rare_disease.append(sentence_group.span())
        return "*"*(len(rare_disease_group))




