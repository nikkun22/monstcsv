# coding: utf-8

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import re


def chrome_start(chromedriver_path, access_url=''):
    options = Options()
    options.add_argument('--headless')  # headlessモードを使用する
    options.add_argument('--disable-gpu')  # headlessモードで暫定的に必要なフラグ(そのうち不要になる)
    options.add_argument('--hide-scrollbars')  # スクロールバー非表示
    options.add_argument('--disable-extensions')  # すべての拡張機能を無効にする。ユーザースクリプトも無効にする
    options.add_argument('--proxy-server="direct://"')  # Proxy経由ではなく直接接続する
    options.add_argument('--proxy-bypass-list=*')  # すべてのホスト名
    options.add_argument('--start-maximized')  # 起動時にウィンドウを最大化する

    print('Chromeを自動起動中...')
    driver_options_path = webdriver.Chrome(executable_path=chromedriver_path, options=options)

    # ページにアクセス
    driver_options_path.get(access_url)

    # 暗黙的な待機
    # 要素が見つかるまで、最大10秒間待機する
    driver_options_path.implicitly_wait(10)

    # 検索先のページのHTMLを取得
    html_source = driver_options_path.page_source.encode('utf-8')
    soup_html = BeautifulSoup(html_source, 'lxml')

    return driver_options_path, soup_html


# chromeを閉じる
def chrome_close():
    driver.close()
    driver.quit()
    print('chromeを自動終了しました...')


# タグの空判定関数
def blank_check(get_tag):
    if type(get_tag) == str:
        if not get_tag:
            get_tag = '-'
            return get_tag
        else:
            return get_tag
    else:
        if not get_tag:
            get_tag = '-'
            return get_tag
        else:
            get_tag = [get_tag.text for get_tag in get_tag]
            get_tag = get_tag[0]
            return get_tag


# データセット
# ヘッダ－
csv_header = [
    '主キー', '図鑑No.', 'モンスター名', '進化状態', 'レアリティ', 'レアリティ(★)',
    '属性', '種族',
    '戦型', '撃種', 'ラックスキル',
    'ストライクショット名', 'ストライクショットターン数', 'ストライクショット内容',
    'メイン友情コンボ名', 'メイン友情コンボ威力', 'メイン友情コンボ内容',
    '副友情コンボ名', '副友情コンボ威力', '副友情コンボ内容',
    '素アビリティ_1', '素アビリティ_2', '素アビリティ_3', '素アビリティ_4',
    'ゲージアビリティ_1', 'ゲージアビリティ_2', 'ゲージアビリティ_3', 'ゲージアビリティ_4',
    'コネクトスキル_1', 'コネクトスキル_2', 'コネクトスキル条件',
    '最大レベル', 'HP', '攻撃力', 'スピード',
    'タス+値最大', 'タス+値最大_HP', 'タス+値最大_攻撃力', 'タス+値最大_スピード',
    'ゲージ成功', 'ゲージ成功_HP', 'ゲージ成功_攻撃力', 'ゲージ成功_スピード',
    'Lv120_タス+値無し', 'Lv120_HP', 'Lv120_攻撃力', 'Lv120_スピード',
    'Lv120_タス+値最大', 'Lv120_タス+値最大_HP', 'Lv120_タス+値最大_攻撃力', 'Lv120_タス+値最大_スピード',
    'Lv120_タス+値最大_ゲージ成功', 'Lv120_タス+値最大_ゲージ成功_HP', 'Lv120_タス+値最大_ゲージ成功_攻撃力', 'Lv120_タス+値最大_ゲージ成功_スピード',
]

# CSVファイルを開く。ファイルがなければ新規作成する。
with open('monster_strike_list.csv', mode='r', newline='', encoding='utf-16') as f:
    f.readline()  # skip header
    line = f.readline()
    if line == '':
        print('csvが空ファイルのため新規作成しています...')
        null_csv = True
    else:
        null_csv = False
    # CSVファイルを閉じる。
    f.close()

# CSVファイルが空ファイルの場合ヘッダーを書く
if null_csv:
    with open('monster_strike_list.csv', mode='w', newline='', encoding='utf-16') as file:
        writer = csv.writer(file, dialect='excel-tab', quoting=csv.QUOTE_ALL)
        writer.writerow(csv_header)
    # CSVファイルを閉じる。
    file.close()

# モンスターNoのマックス数
monster_no_max = 6046 + 1

for i in range(6046, monster_no_max + 1):

    try:
        # 読み込むファイル
        file_path = r' file:///C:\Users\takum\PycharmProjects\monst\monster_data_list\monster_data_' + str(i) + '.html'

        # Chrome Optionsのパス
        driver_path = r'.\chromedriver.exe'
        driver, soup = chrome_start(driver_path, file_path)

        # データ、パラメータ取得
        # ---図鑑ナンバー---
        monster_number = soup.find('p', class_='monster-no').get_text()
        monster_number = blank_check(monster_number)
        # print(monster_number)

        # ---モンスター名---
        monster_name = soup.find('div', class_='monster-name').get_text()
        monster_name = blank_check(monster_name)
        # print(monster_name)

        # ---進化状態---
        """
        進化状態判定(7パターン)
        進化前
        神化前
        進化
        神化
        獣神化前
        獣神化
        獣神化・改
        """

        monster_evolutionary_state = soup.select('body > div > div.monster-container > div.monster-detail > '
                                                 'div.monster-page-title > p')
        monster_evolutionary_state = blank_check(monster_evolutionary_state)

        if '獣神化前' in monster_evolutionary_state:
            monster_evolutionary_state = '獣神化前'
        elif '獣神化改' in monster_evolutionary_state:
            monster_evolutionary_state = '獣神化改'
        elif '獣神化' in monster_evolutionary_state:
            monster_evolutionary_state = '獣神化'
        elif '進化前' in monster_evolutionary_state:
            monster_evolutionary_state = '進化前'
        elif '神化前' in monster_evolutionary_state:
            monster_evolutionary_state = '神化前'
        elif '進化' in monster_evolutionary_state:
            monster_evolutionary_state = '進化'
        elif '神化' in monster_evolutionary_state:
            monster_evolutionary_state = '神化'
        else:
            monster_evolutionary_state = '取得エラー'
            pass

        # print(monster_evolutionary_state)

        # ---レア度(★表記)---
        monster_rarity_star_mark = soup.find('p', class_='rarity').get_text()
        monster_rarity_star_mark = blank_check(monster_rarity_star_mark)
        # print(monster_rarity)

        # ---レア度(数字表記)---
        monster_rarity_numeral = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.status-table > '
            'table > tbody > tr:nth-child(1) > td:nth-child(2) > a')
        monster_rarity_numeral = blank_check(monster_rarity_numeral)
        monster_rarity_numeral = re.sub(r'[\u3000 \t\r\n]', '', monster_rarity_numeral)
        # print(monster_rarity_numeral)

        # ---属性---
        monster_attribute = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.status-table > '
            'table > tbody > tr:nth-child(2) > td:nth-child(2) > a')
        monster_attribute = blank_check(monster_attribute)
        monster_attribute = re.sub(r'[\u3000 \t\r\n]', '', monster_attribute)
        # print(monster_attribute)

        # 種族
        monster_species = soup.find('p', class_='species').get_text()
        monster_species = blank_check(monster_species)
        monster_species = monster_species.lstrip('種族：')
        # print(monster_species)

        # 戦型
        monster_battle_type = soup.select(
            'body > div > div.monster-container > div.monster-detail > div.monster-pcdetail > '
            'div.monster-title > div.monster-substatus > p:nth-child(3)')
        monster_battle_type = blank_check(monster_battle_type)
        monster_battle_type = monster_battle_type.lstrip('型：')
        # print(monster_battle_type)

        # 撃種
        monster_type_of_attack = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.status-table > '
            'table > tbody > tr:nth-child(5) > td:nth-child(2) > a')
        monster_type_of_attack = blank_check(monster_type_of_attack)
        # print(monster_type_of_attack)

        # ラックスキル
        monster_rack_skill = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.status-table > table > tbody > '
            'tr:nth-child(9) '
            '> td:nth-child(2) > a')
        monster_rack_skill = blank_check(monster_rack_skill)
        # print(monster_rack_skill)

        # ストライクショット名
        strikeshot_name = soup.find('p', class_='strikeshot-name').get_text()
        strikeshot_name = blank_check(strikeshot_name)
        # print(strikeshot_name)

        # ストライクショットターン数
        strikeshot_detail = soup.select('body > div > div.monster-container > div.monster-strikeshot > p:nth-child(3)')
        strikeshot_detail = blank_check(strikeshot_detail)

        strikeshot_detail = re.sub(r'[\u3000 \t\r\n]', '', strikeshot_detail)
        strikeshot_detail = strikeshot_detail.strip('ターン数:')
        # print(strikeshot_detail)

        # ストライクショット内容
        # body > div > div.monster-container > div.monster-strikeshot > p:nth-child(4)
        strikeshot_description = soup.select(
            'body > div > div.monster-container > div.monster-strikeshot > p:nth-child(4)')
        strikeshot_description = blank_check(strikeshot_description)
        # print(strikeshot_description)

        # メイン友情コンボ名
        friend_combo_name = soup.select(
            'body > div > div.monster-container > div.monster-friendcombo > p.friendcombo-name > a')
        friend_combo_name = blank_check(friend_combo_name)
        # print(friend_combo_name)

        # メイン友情コンボ威力
        friend_combo_power = soup.select(
            'body > div > div.monster-container > div.monster-friendcombo > p.friendcombo-name > '
            'span')
        friend_combo_power = blank_check(friend_combo_power)
        friend_combo_power = friend_combo_power.strip('/威力：')
        # print(friend_combo_power)

        # メイン友情コンボ内容
        friend_combo_description = soup.select(
            'body > div > div.monster-container > div.monster-friendcombo > p:nth-child(4)')
        friend_combo_description = blank_check(friend_combo_description)
        # print(friend_combo_description)

        # 副友情コンボ名
        friend_combo_name_sub = soup.select(
            'body > div > div.monster-container > div.monster-friendcombo > p:nth-child(5) > a')
        friend_combo_name_sub = blank_check(friend_combo_name_sub)
        # print(friend_combo_name_sub)

        # 副友情コンボ威力
        friend_combo_power_sub = soup.select(
            'body > div > div.monster-container > div.monster-friendcombo > p:nth-child(5) > '
            'span')
        friend_combo_power_sub = blank_check(friend_combo_power_sub)
        friend_combo_power_sub = friend_combo_power_sub.strip('/威力：')
        # print(friend_combo_power_sub)

        # 副友情コンボ内容
        friend_combo_description_sub = soup.select('body > div > div.monster-container > div.monster-friendcombo > '
                                                   'p:nth-child(7)')
        friend_combo_description_sub = blank_check(friend_combo_description_sub)
        # print(friend_combo_description_sub)

        # アビリティ
        monster_ability_1 = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.status-table > '
            'table > tbody > tr:nth-child(6) > td:nth-child(2) > a:nth-child(1)')
        monster_ability_1 = blank_check(monster_ability_1)
        # print(monster_ability_1)

        monster_ability_2 = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.status-table > '
            'table > tbody > tr:nth-child(6) > td:nth-child(2) > a:nth-child(2)')
        monster_ability_2 = blank_check(monster_ability_2)
        monster_ability_2 = monster_ability_2.lstrip('/')
        # print(monster_ability_2)

        monster_ability_3 = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.status-table > '
            'table > tbody > tr:nth-child(6) > td:nth-child(2) > a:nth-child(3)')
        monster_ability_3 = blank_check(monster_ability_3)
        monster_ability_3 = monster_ability_3.lstrip('/')
        # print(monster_ability_3)

        monster_ability_4 = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.status-table > '
            'table > tbody > tr:nth-child(6) > td:nth-child(2) > a:nth-child(4)')
        monster_ability_4 = blank_check(monster_ability_4)
        monster_ability_4 = monster_ability_4.lstrip('/')
        # print(monster_ability_4)

        monster_ability_gauge_1 = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.status-table > '
            'table > tbody > tr:nth-child(7) > td:nth-child(2) > a:nth-child(1)')
        monster_ability_gauge_1 = blank_check(monster_ability_gauge_1)
        # print(monster_ability_gauge_1)

        monster_ability_gauge_2 = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.status-table > '
            'table > tbody > tr:nth-child(7) > td:nth-child(2) > a:nth-child(2)')
        monster_ability_gauge_2 = blank_check(monster_ability_gauge_2)
        monster_ability_gauge_2 = monster_ability_gauge_2.lstrip('/')
        # print(monster_ability_gauge_2)

        monster_ability_gauge_3 = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.status-table > '
            'table > tbody > tr:nth-child(7) > td:nth-child(2) > a:nth-child(3)')
        monster_ability_gauge_3 = blank_check(monster_ability_gauge_3)
        monster_ability_gauge_3 = monster_ability_gauge_3.lstrip('/')
        # print(monster_ability_gauge_3)

        monster_ability_gauge_4 = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.status-table > '
            'table > tbody > tr:nth-child(7) > td:nth-child(2) > a:nth-child(4)')
        monster_ability_gauge_4 = blank_check(monster_ability_gauge_4)
        monster_ability_gauge_4 = monster_ability_gauge_4.lstrip('/')
        # print(monster_ability_gauge_4)

        # コネクトスキル
        monster_connect_skills_1 = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.status-table '
            '> table > tbody > tr:nth-child(8) > td:nth-child(2) > a:nth-child(1)')
        monster_connect_skills_1 = blank_check(monster_connect_skills_1)
        # print(monster_connect_skills_1)

        monster_connect_skills_2 = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.status-table '
            '> table > tbody > tr:nth-child(8) > td:nth-child(2) > a:nth-child(2)')
        monster_connect_skills_2 = blank_check(monster_connect_skills_2)
        monster_connect_skills_2 = monster_connect_skills_2.lstrip('/')
        # print(monster_connect_skills_2)

        # コネクトスキル条件
        monster_connect_skills_terms = soup.select('body > div > div.monster-container > div.monster-sp-status > '
                                                   'div.status-table > table > tbody > tr:nth-child(8) > '
                                                   'td:nth-child(2) > '
                                                   'span')
        monster_connect_skills_terms = blank_check(monster_connect_skills_terms)
        # print(monster_connect_skills_terms)

        # ステータス
        # 最大Lv
        monster_maximum_level = soup.select('body > div > div.monster-container > div.monster-sp-status > '
                                            'div.value-table > table > tbody > tr:nth-child(2) > td.value_title')
        monster_maximum_level = blank_check(monster_maximum_level)
        # print(monster_maximum_level)

        # HP
        monster_maximum_level_hp = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.value-table > '
            'table > tbody > tr:nth-child(2) > td:nth-child(2)')
        monster_maximum_level_hp = blank_check(monster_maximum_level_hp)
        # print(monster_maximum_level_hp)

        # 攻撃力
        monster_maximum_level_attack = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.value-table > table > tbody > '
            'tr:nth-child(2) > '
            'td:nth-child(3)')
        monster_maximum_level_attack = blank_check(monster_maximum_level_attack)
        # print(monster_maximum_level_attack)

        # スピード
        monster_maximum_level_speed = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.value-table > table > tbody > '
            'tr:nth-child(2) > '
            'td:nth-child(4)')
        monster_maximum_level_speed = blank_check(monster_maximum_level_speed)
        # print(monster_maximum_level_speed)

        # タス+値最大(タスカン)
        # HP
        monster_maximum_tsk_hp = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.value-table > table > tbody > '
            'tr:nth-child(3) > '
            'td:nth-child(2)')
        monster_maximum_tsk_hp = blank_check(monster_maximum_tsk_hp)
        # print(monster_maximum_tsk_hp)

        # 攻撃力
        monster_maximum_tsk_attack = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.value-table > table > tbody > '
            'tr:nth-child(3) > '
            'td:nth-child(3)')
        monster_maximum_tsk_attack = blank_check(monster_maximum_tsk_attack)
        # print(monster_maximum_tsk_attack)

        # スピード
        monster_maximum_tsk_speed = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.value-table > table > tbody > '
            'tr:nth-child(3) > '
            'td:nth-child(4)')
        monster_maximum_tsk_speed = blank_check(monster_maximum_tsk_speed)
        # print(monster_maximum_tsk_speed)

        # タス+値最大,ゲージ成功時
        # HP
        monster_maximum_tsk_gauge_hp = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.value-table > table > tbody > '
            'tr:nth-child(4) > '
            'td:nth-child(2)')
        monster_maximum_tsk_gauge_hp = blank_check(monster_maximum_tsk_gauge_hp)
        # print(monster_maximum_tsk_gauge_hp)

        # 攻撃力
        monster_maximum_tsk_gauge_attack = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.value-table > table > tbody > '
            'tr:nth-child(4) > '
            'td:nth-child(3)')
        monster_maximum_tsk_gauge_attack = blank_check(monster_maximum_tsk_gauge_attack)
        # print(monster_maximum_tsk_gauge_attack)

        # スピード
        monster_maximum_tsk_gauge_speed = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.value-table > table > tbody > '
            'tr:nth-child(4) > '
            'td:nth-child(4)')
        monster_maximum_tsk_gauge_speed = blank_check(monster_maximum_tsk_gauge_speed)
        # print(monster_maximum_tsk_gauge_speed)

        # Lv120,未タスカン
        # HP
        monster_lv_release_hp = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.value-table > table > tbody > '
            'tr:nth-child(5) > '
            'td:nth-child(2)')
        monster_lv_release_hp = blank_check(monster_lv_release_hp)
        # print(monster_lv_release_hp)

        # 攻撃力
        monster_lv_release_attack = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.value-table > table > tbody > '
            'tr:nth-child(5) > '
            'td:nth-child(3)')
        monster_lv_release_attack = blank_check(monster_lv_release_attack)
        # print(monster_lv_release_attack)

        # スピード
        monster_lv_release_speed = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.value-table > table > tbody > '
            'tr:nth-child(5) > '
            'td:nth-child(4)')
        monster_lv_release_speed = blank_check(monster_lv_release_speed)
        # print(monster_lv_release_speed)

        # Lv120,タス+値最大(Lv120タスカン)
        # HP
        monster_lv_release_tsk_hp = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.value-table > table > tbody > '
            'tr:nth-child(6) > '
            'td:nth-child(2)')
        monster_lv_release_tsk_hp = blank_check(monster_lv_release_tsk_hp)
        # print(monster_lv_release_tsk_hp)

        # 攻撃力
        monster_lv_release_tsk_attack = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.value-table > table > tbody > '
            'tr:nth-child(6) > '
            'td:nth-child(3)')
        monster_lv_release_tsk_attack = blank_check(monster_lv_release_tsk_attack)
        # print(monster_lv_release_tsk_attack)

        # スピード
        monster_lv_release_tsk_speed = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.value-table > table > tbody > '
            'tr:nth-child(6) > '
            'td:nth-child(4)')
        monster_lv_release_tsk_speed = blank_check(monster_lv_release_tsk_speed)
        # print(monster_lv_release_tsk_speed)

        # Lv120,タス+値最大,ゲージ成功時
        # HP
        monster_lv_release_tsk_gauge_hp = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.value-table > table > tbody > '
            'tr:nth-child(7) > '
            'td:nth-child(2)')
        monster_lv_release_tsk_gauge_hp = blank_check(monster_lv_release_tsk_gauge_hp)
        # print(monster_lv_release_tsk_gauge_hp)

        # 攻撃力
        monster_lv_release_tsk_gauge_attack = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.value-table > table > tbody > '
            'tr:nth-child(7) > '
            'td:nth-child(3)')
        monster_lv_release_tsk_gauge_attack = blank_check(monster_lv_release_tsk_gauge_attack)
        # print(monster_lv_release_tsk_gauge_attack)

        # スピード
        monster_lv_release_tsk_gauge_speed = soup.select(
            'body > div > div.monster-container > div.monster-sp-status > div.value-table > table > tbody > '
            'tr:nth-child(7) > '
            'td:nth-child(4)')
        monster_lv_release_tsk_gauge_speed = blank_check(monster_lv_release_tsk_gauge_speed)
        # print(monster_lv_release_tsk_gauge_speed)

        # データリスト
        dataList = [
            i, monster_number, monster_name, monster_evolutionary_state, monster_rarity_numeral,
            monster_rarity_star_mark,
            monster_attribute, monster_species,
            monster_battle_type, monster_type_of_attack, monster_rack_skill,
            strikeshot_name, strikeshot_detail, strikeshot_description,
            friend_combo_name, friend_combo_power, friend_combo_description,
            friend_combo_name_sub, friend_combo_power_sub, friend_combo_description_sub,
            monster_ability_1, monster_ability_2, monster_ability_3, monster_ability_4,
            monster_ability_gauge_1, monster_ability_gauge_2, monster_ability_gauge_3, monster_ability_gauge_4,
            monster_connect_skills_1, monster_connect_skills_2, monster_connect_skills_terms,
            monster_maximum_level, monster_maximum_level_hp, monster_maximum_level_attack, monster_maximum_level_speed,
            '-', monster_maximum_tsk_hp, monster_maximum_tsk_attack, monster_maximum_tsk_speed,
            '-', monster_maximum_tsk_gauge_hp, monster_maximum_tsk_gauge_attack, monster_maximum_tsk_gauge_speed,
            '-', monster_lv_release_hp, monster_lv_release_attack, monster_lv_release_speed,
            '-', monster_lv_release_tsk_hp, monster_lv_release_tsk_attack, monster_lv_release_tsk_speed,
            '-', monster_lv_release_tsk_gauge_hp, monster_lv_release_tsk_gauge_attack,
            monster_lv_release_tsk_gauge_speed
        ]

        # CSVファイルにデータを記載する
        with open('monster_strike_list.csv', mode='a', newline='', encoding='utf-16') as file:
            writer = csv.writer(file, dialect='excel-tab', quoting=csv.QUOTE_ALL)
            writer.writerow(dataList)

        print('No.'+str(i), '追記完了')
        # chromeを終了する
        chrome_close()

    except Exception as e:
        # データリスト
        dataList = [
            i, '-', '-', '-', '-',
            '-',
            '-', '-',
            '-', '-', '-',
            '-', '-', '-',
            '-', '-', '-',
            '-', '-', '-',
            '-', '-', '-', '-',
            '-', '-', '-', '-',
            '-', '-', '-',
            '-', '-', '-', '-',
            '-', '-', '-', '-',
            '-', '-', '-', '-',
            '-', '-', '-', '-',
            '-', '-', '-', '-',
            '-', '-', '-',
            '-'
        ]

        # CSVファイルにデータを記載する
        with open('monster_strike_list.csv', mode='a', newline='', encoding='utf-16') as file:
            writer = csv.writer(file, dialect='excel-tab', quoting=csv.QUOTE_ALL)
            writer.writerow(dataList)

        print(e)
        print('No.' + str(i), '例外処理(欠番)')

        i += 1
        # chromeを終了する
        chrome_close()

    if i == monster_no_max:
        print('chromeを自動終了しました...')
        print('処理が終了しました...')
        # CSVファイルを閉じる
        file.close()
        # chromeを終了する
        chrome_close()
    else:
        pass

# print('すべての処理が終了しました...')
# csvをpandasで開く(今後実装していく)
