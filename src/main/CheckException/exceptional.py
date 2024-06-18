from src.main.CheckException.SentenceLoc import sentence_loc


class ChkException:

    def __init__(self, sentence):
        self.sentence = sentence

    def chk_only_number(self, sentence_group) -> bool:
        start_idx, end_idx, sentence_length = sentence_group.start(), sentence_group.end(), len(self.sentence)

        if sentence_loc(start_idx, end_idx, sentence_length) == "mid":

            if not self.sentence[start_idx - 1].isdigit() and not self.sentence[end_idx].isdigit():  # 앞뒤 숫자 아닐 때
                if start_idx - 2 >= 0 and self.sentence[start_idx - 2:start_idx] == "0.":
                    return False
                else:
                    return True

        if sentence_loc(start_idx, end_idx, sentence_length) == "all":  # 문장 전체가 될 때
            return True

        if start_idx == 0 and not self.sentence[end_idx].isdigit():  # 맨 앞글자 일 때, 뒤만 검사
            return True

        if end_idx == sentence_length and not self.sentence[start_idx - 1].isdigit():  # 맨 뒷글자 일 때, 앞만 검사
            if start_idx - 2 >= 0 and self.sentence[start_idx - 2:start_idx] == "0.":
                return False
            else:
                return True

        return False

    def chk_char_number(self, sentence_group) -> bool:
        """
            input : 앞부분 문자, 뒷부분 숫자
            output : 앞 뒤 둘다 숫자 영어 불가, 띄어 쓰기 및 한글 가능
        """
        start_idx, end_idx, sentence_length = sentence_group.start(), sentence_group.end(), len(self.sentence)

        if sentence_loc(start_idx, end_idx, sentence_length) == "tail":
            if self.sentence[start_idx-1].isdigit() or self.sentence[start_idx-1].upper() != self.sentence[start_idx-1].lower():
                return False

        elif sentence_loc(start_idx, end_idx, sentence_length) == "all":
            return True

        elif sentence_loc(start_idx, end_idx, sentence_length) == "head":
            if self.sentence[end_idx].isdigit() or \
                    self.sentence[end_idx].upper() != self.sentence[end_idx].lower():
                return False

        elif sentence_loc(start_idx, end_idx, sentence_length) == "mid":

            if self.sentence[start_idx-1].isdigit() or self.sentence[start_idx-1].upper() != self.sentence[start_idx-1].lower() or \
                    self.sentence[end_idx].isdigit() or self.sentence[end_idx].upper() != self.sentence[end_idx].lower():
                return False

        return True

    def chk_arithmetic_sequence(self, group_lst):
        """
            다음 스텝으로 가면 True
        """
        if group_lst == "":
            return True

        split_mark = None
        for sm in group_lst:
            if sm in ["-", ".", " "]:
                split_mark = sm
                break
        group_lst_split = group_lst.split(split_mark)
        for i in range(len(group_lst_split)):
            chk = group_lst_split[i]
            if len(chk) == 1:
                continue

            if len(chk) > 2:
                if len(list(set(chk))) == 1:
                    continue
                for j in range(len(chk) - 2):
                    if int(chk[j + 2]) - int(chk[j + 1]) != 1:
                        return True

        return False
