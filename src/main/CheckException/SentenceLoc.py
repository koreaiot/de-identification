
def sentence_loc(start_idx, end_idx, sentence_length) -> str:
    if start_idx == 0 and end_idx == sentence_length:  # 문장 전체
        return "all"
    elif start_idx == 0 and end_idx != sentence_length:  # 문장 맨 앞
        return "head"
    elif 0 < start_idx < end_idx < sentence_length:  # 문장 중간
        return "mid"
    else:  # 문장 맨 뒤
        return "tail"
