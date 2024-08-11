import re
import pandas as pd
from pyvi import ViTokenizer, ViPosTagger


class VietnameseTextPreprocessor:
    def __init__(self, path_stopwords=None, multi_label=True, is_remove_np=True):
        self.multi_label = multi_label
        self.stopwords = self.load_stopwords(path_stopwords)
        self.is_remove_np = is_remove_np
        self.dicchar = self.loaddictchar()
        self.bang_nguyen_am = [['a', 'à', 'á', 'ả', 'ã', 'ạ'],
                               ['ă', 'ằ', 'ắ', 'ẳ', 'ẵ', 'ặ'],
                               ['â', 'ầ', 'ấ', 'ẩ', 'ẫ', 'ậ'],
                               ['e', 'è', 'é', 'ẻ', 'ẽ', 'ẹ'],
                               ['ê', 'ề', 'ế', 'ể', 'ễ', 'ệ'],
                               ['i', 'ì', 'í', 'ỉ', 'ĩ', 'ị'],
                               ['o', 'ò', 'ó', 'ỏ', 'õ', 'ọ'],
                               ['ô', 'ồ', 'ố', 'ổ', 'ỗ', 'ộ'],
                               ['ơ', 'ờ', 'ớ', 'ở', 'ỡ', 'ợ'],
                               ['u', 'ù', 'ú', 'ủ', 'ũ', 'ụ'],
                               ['ư', 'ừ', 'ứ', 'ử', 'ữ', 'ự'],
                               ['y', 'ỳ', 'ý', 'ỷ', 'ỹ', 'ỵ']]
        self.nguyen_am_to_ids = self.build_nguyen_am_to_ids()

    def load_stopwords(self, path_stopwords):
        if not path_stopwords:
            return set()
        with open(path_stopwords, "r", encoding='utf-8') as file:
            words = file.readlines()
        return set(n.replace('\n', '') for n in words)

    def loaddictchar(self):
        dic = {}
        char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
            '|')
        charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
            '|')
        for i in range(len(char1252)):
            dic[char1252[i]] = charutf8[i]
        return dic

    def build_nguyen_am_to_ids(self):
        nguyen_am_to_ids = {}
        for i in range(len(self.bang_nguyen_am)):
            for j in range(len(self.bang_nguyen_am[i])):
                nguyen_am_to_ids[self.bang_nguyen_am[i][j]] = (i, j)
        return nguyen_am_to_ids

    def convertwindown1525toutf8(self, txt):
        return re.sub(
            r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
            lambda x: self.dicchar[x.group()], txt)

    def is_valid_vietnam_word(self, word):
        chars = list(word)
        nguyen_am_index = -1
        for index, char in enumerate(chars):
            x, y = self.nguyen_am_to_ids.get(char, (-1, -1))
            if x != -1:
                if nguyen_am_index == -1:
                    nguyen_am_index = index
                else:
                    if index - nguyen_am_index != 1:
                        return False
                    nguyen_am_index = index
        return True

    # Sửa lỗi sử dụng các dấu thanh kiểu cũ (òa, úy thay vì oà, uý)
    def chuan_hoa_dau_tu_tieng_viet(self, word):
        if not self.is_valid_vietnam_word(word):
            return word

        chars = list(word)
        dau_cau = 0
        nguyen_am_index = []
        qu_or_gi = False
        for index, char in enumerate(chars):
            x, y = self.nguyen_am_to_ids.get(char, (-1, -1))
            if x == -1:
                continue
            elif x == 9:  # check qu
                if index != 0 and chars[index - 1] == 'q':
                    chars[index] = 'u'
                    qu_or_gi = True
            elif x == 5:  # check gi
                if index != 0 and chars[index - 1] == 'g':
                    chars[index] = 'i'
                    qu_or_gi = True
            if y != 0:
                dau_cau = y
                chars[index] = self.bang_nguyen_am[x][0]
            if not qu_or_gi or index != 1:
                nguyen_am_index.append(index)
        if len(nguyen_am_index) < 2:
            if qu_or_gi:
                if len(chars) == 2:
                    x, y = self.nguyen_am_to_ids.get(chars[1])
                    chars[1] = self.bang_nguyen_am[x][dau_cau]
                else:
                    x, y = self.nguyen_am_to_ids.get(chars[2], (-1, -1))
                    if x != -1:
                        chars[2] = self.bang_nguyen_am[x][dau_cau]
                    else:
                        chars[1] = self.bang_nguyen_am[5][dau_cau] if chars[1] == 'i' else self.bang_nguyen_am[9][
                            dau_cau]
                return ''.join(chars)
            return word

        for index in nguyen_am_index:
            x, y = self.nguyen_am_to_ids[chars[index]]
            if x == 4 or x == 8:  # ê, ơ
                chars[index] = self.bang_nguyen_am[x][dau_cau]
                return ''.join(chars)

        if len(nguyen_am_index) == 2:
            if nguyen_am_index[-1] == len(chars) - 1:
                x, y = self.nguyen_am_to_ids[chars[nguyen_am_index[0]]]
                chars[nguyen_am_index[0]] = self.bang_nguyen_am[x][dau_cau]
            else:
                x, y = self.nguyen_am_to_ids[chars[nguyen_am_index[1]]]
                chars[nguyen_am_index[1]] = self.bang_nguyen_am[x][dau_cau]
        else:
            x, y = self.nguyen_am_to_ids[chars[nguyen_am_index[1]]]
            chars[nguyen_am_index[1]] = self.bang_nguyen_am[x][dau_cau]
        return ''.join(chars)

    def chuan_hoa_dau_cau_tieng_viet(self, sentence):
        sentence = self.convertwindown1525toutf8(sentence)

        ##Do nếu không tách các ký tự đặc biệt ra từng từ, thì def chuan_hoa_dau_tu_tieng_viet sẽ sửa dấu sai
        # Sử dụng regex để tách các từ và ký tự đặc biệt
        words_with_indices = [(match.group(), match.start()) for match in re.finditer(r'\w+|[^\w\s]', sentence)]

        # Chuẩn hóa từng từ tiếng Việt
        for index, (word, pos) in enumerate(words_with_indices):
            if word.isalnum():  # Chỉ chuẩn hóa nếu từ là chữ cái hoặc số
                words_with_indices[index] = (self.chuan_hoa_dau_tu_tieng_viet(word.lower()), pos)

        # Khôi phục lại câu với các ký tự đặc biệt đúng vị trí và giữ nguyên viết hoa viết thường
        result = list(sentence)
        for word, pos in words_with_indices:
            for i, char in enumerate(word):
                if sentence[pos + i].isupper():
                    result[pos + i] = char.upper()
                else:
                    result[pos + i] = char

        return ''.join(result)

    # Np - Proper noun
    # M - Numeral
    # F - Filtered out (punctuation)
    def filter_and_join_words(self, tagged_sentence, is_remove_np):
        exclude_pos_tags = ['M', 'F']
        if is_remove_np:
            exclude_pos_tags.append('Np')

        words, postags = tagged_sentence
        filtered_words = []

        for word, postag in zip(words, postags):
            if postag not in exclude_pos_tags:
                filtered_words.append(word)

        return ' '.join(filtered_words)

    def process_text(self, text):
        text = self.chuan_hoa_dau_cau_tieng_viet(
            text)  # Chuẩn hóa dấu câu tiếng việt và chuyển đổi Windown1525 thành UTF8
        text = text.replace('_x000D_',
                            '')  # _x000D_ là mã Unicode biểu diễn ký tự xuống dòng (CR-Carriage Return) (Cái này khi up file excel, mở bằng GG Sheets sẽ bị ở những chổ xuống dòng dữ liệu '\n')

        # Kiểm tra tỷ lệ ký tự viết hoa trong văn bản
        upper_case_chars = sum(1 for char in text if char.isupper())
        total_chars = len(text)
        if upper_case_chars / total_chars >= 0.9:
            text = text.lower()  # Nếu tỷ lệ ký tự viết hoa cao hơn 90%, chuyển đổi văn bản thành viết thường
        """
        Ví dụ:   V/V CỬ NHÂN SỰ THAM GIA TỔ CÔNG TÁC VÀ TỔ GIÚP VIỆC XÂY DỰNG ĐỀ ÁN PHÂN CẤP, ỦY QUYỀN
                 BÁO CÁO VỀ TỔ CHỨC HOẠT ĐỘNG VẬN TẢI PHÒNG, CHỐNG DỊCH COVID-19 TRONG TÌNH HÌNH MỚI ĐỐI VỚI LĨNH VỰC GIAO THÔNG VẬN TẢI (Ngày 23 tháng 11 năm 2021)
            -Những từ này nếu không đưa về lower thì khi tách từ đa phần sẽ nhận định là danh từ, danh từ riêng,... ra kết quả không chính xác với nội dung của text
        """

        postagging_text = ViPosTagger.postagging(ViTokenizer.tokenize(text))  # Dùng Vi để tách từ và gán postagger
        text = self.filter_and_join_words(postagging_text,
                                          self.is_remove_np)  # Loại bỏ các từ có postagger không cần thiết
        text = re.sub(r'[^\w\s]', '', text)  # Loại bỏ các ký tự đặc biệt thêm 1 lần nữa nếu sau khi tách từ vấn còn
        word_tokens = text.split()
        filtered_text = []
        for word in word_tokens:
            if word.lower() in self.stopwords:
                continue
            else:
                filtered_text.append(word)
        filtered_text = [word for word in filtered_text if len(word) > 1]  # Loại bỏ các từ đơn
        filtered_text = ' '.join(filtered_text)
        return filtered_text.lower()  # Trả về text lower

    #Lấy ra dữ liệu có trùng trích yếu, khác nhãn
    def get_data_duplicated(self, df, column_input, column_output):
        # Lấy các hàng trùng lặp dựa trên cột "Trích yếu"
        duplicated_data = df[df.duplicated(subset=column_input, keep=False)]

        grouped = duplicated_data.groupby(column_input)
        filtered_data = []
        for name, group in grouped:
            counts = group[column_output].value_counts()
            if len(counts) == 1:
                filtered_data.append(group)
            else:
                # Lấy số lượng count của counts top 2
                top_counts = counts.nlargest(2)
                first_top_count = top_counts.iloc[0]
                second_top_count = top_counts.iloc[1]
                count_data = first_top_count - second_top_count
                top_id = counts.idxmax()
                top_group = group[group[column_output] == top_id]
                get_data_top = top_group.head(count_data)
                filtered_data.append(get_data_top)
        filtered_data = pd.concat(filtered_data)  # Dữ liệu đã loại bỏ các trích yếu nhiều nhãn

        return duplicated_data.drop(filtered_data.index)  # Dữ liệu mà trích yếu có nhiều nhãn

    def process_df(self, df, column_input, column_label, column_input_name, column_label_name):
        df.dropna(inplace=True)
        if not self.multi_label:
            df_duplicated = self.get_data_duplicated(df, column_input, column_label)
            df = df.drop(df_duplicated.index)

        df[column_input_name] = df[column_input].apply(lambda x: self.process_text(x))
        df[column_label_name] = df[column_label]
        result_df = df[[column_input_name, column_label_name]]
        return result_df

