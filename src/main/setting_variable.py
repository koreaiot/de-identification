import pandas as pd
import json

bin_number_data = pd.read_csv("src/data/bin_number_list.csv")
bin_number_list = bin_number_data["bin_number"].to_list()
bank_account = pd.read_csv("src/data/bank_account.csv")
# bank_account_regex_list = bank_account["패턴"].to_list()
bank_account_regex_list = ["(d{3}-\d{2}-\d{4}-\d{3})|(\d{6}-\d{2}-\d{6})|(\d{3}-\d{6}-\d{2}-\d{3})|(\d{3}-\d{4}-\d{4}-\d{2})|(\d{3}-\d{2}-\d{6})|(\d{3}-\d{3}-\d{6})|(\d{4}-\d{3}-\d{6})|(\d{3}-\d{6}-\d{5})|(\d{3}-\d{6}-\d{3})|(\d{3}-\d{6}-\d{3})|(\d{3}-\d{2}-\d{6}-\d{1})|(\d{3}-\d{4}-\d{4}-\d{2})|(\d{3}-\d{2}-\d{6})|(\d{3}-\d{3}-\d{6})|(\d{4}-\d{2}-\d{7})|(\d{3}-\d{7}-\d{1}-\d{3})|(\d{3}-\d{2}-\d{6}-\d{1})|(\d{4}-\d{4}-\d{4}-\d{1})"]
address_data = pd.read_csv('')
address_list = list(address_data['시군구이름'].unique())[:87] + list(address_data['시군구이름'].unique())[88:]
address_example_data = pd.read_csv('')
address_example_lst = address_example_data['주소'].to_list()

homepage_example_data = pd.read_csv('src/data/homepage.csv')
homepage_example_lst = homepage_example_data['홈페이지'].to_list()

rare_disease_data = pd.read_csv('src/data/rare_disease.csv')
rare_disease_lst = rare_disease_data['병명'].to_list()

bad_word_data = pd.read_csv('src/data/badword_lst.csv')
bad_word_lst = bad_word_data['bad_word'].to_list()


sentence_lst = [
    "서울 강남구 삼성1동 12132번지"
]

with open("src/data/address/lot_number_address.json", "r") as f:
    lot_number_address = json.load(f)

with open("src/data/address/road_name_address.json", "r") as f:
    road_name_address = json.load(f)

