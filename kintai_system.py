#!/usr/bin/env python
# coding: utf-8




import pandas as pd







# 勤怠システムの読み込み
df = pd.read_csv('kintai.csv')


# ここで年月を取得
Ym = df.iloc[3,4]

# 年と月を抽出し、整形する
year = Ym[0:4]
month = Ym[5:7].lstrip('0')

Ym = f'{year}/{month}/'


# ここから勤怠システムを整形
df = pd.read_csv('kintai.csv', skiprows=10, usecols=(0,1,11,13,14,17,21), names=['年月日','曜日','所定時間','開始','終了','超過勤務','昼休み'])

# NaNを０に置き換え(土日祝日はブランクにして結合したい)
df=df.fillna('0')

# 日にちのみの記載をyy/mm/ddに変更　 
df['年月日'] = df['年月日'].apply(lambda x: Ym + str(x))

# 変更点１：開始と終了もここで「：００」を付け足すことにしました
df['開始'] = df['開始'].apply(lambda x: str(x) + ':00')
df['終了'] = df['終了'].apply(lambda x: str(x) + ':00') 
                          

# hとmを置き換え
df['所定時間'] = df['所定時間'].apply(lambda x: str(x).replace('h',':').replace('m',':00'))

df['超過勤務'] = df['超過勤務'].apply(lambda x: str(x).replace('h',':').replace('m',':00'))

df['昼休み'] = df['昼休み'].apply(lambda x: str(x).replace('h',':').replace('m',':00'))

# 列の入れ替え
df = df[['年月日','曜日','開始','終了','所定時間','超過勤務','昼休み']]




# 年月日の一覧を作ります。
# NOTE: xls 側の日付は YYYY/MM/DD 形式なのでこのままで OK です。
text_1_to_output = ''
for index, row in df.iterrows():
    text_1_to_output += (row['年月日'] + '\n')
# 年月日の一覧を、コピペしやすいようファイルに起こします。
with open('年月日一覧.txt', mode='w') as f:
    f.write(text_1_to_output)





# 変更点１で直接Serieseに「：００」を結合させたため関数は今回は使わないことにしました。
# ですが、この関数はシンプルながら大変感動したところです。

"""
def convert_for_xls(cell_value):
    # 精査しやすいよう str にします。
    # NOTE: もともとの dataframe に int の 0 と str の 0 が混ざっていました。
    #       その違いを消すためでもあります。
    cell_value = str(cell_value)
    # なんか 0 のセルには空欄が入っているっぽかったので空欄にします。
    if cell_value == '0':
        return ''
    # なんか時刻のセルには :00 が追加で入っているっぽかったのでつけます。
    return cell_value + ':00'
"""




# 変更点２：関数を使わなくて良くなったことと、row[[]]というフィルターをかけて必要なSeriesのみ抽出
text_2_to_output = ''
for index, row in df.iterrows():
    text_2_to_output += '\t'.join(row[['開始','終了','所定時間','超過勤務','昼休み']])+ '\n'
with open('開始から昼休み一覧.txt', mode='w') as f:
    f.write(text_2_to_output)





"""
for index, row in df.iterrows():
    # 各項目を xls 側の形式に合わせます。
    row['開始'] = convert_for_xls(row['開始'])
    row['終了'] = convert_for_xls(row['終了'])
    row['所定時間'] = convert_for_xls(row['所定時間'])
    row['超過勤務'] = convert_for_xls(row['超過勤務'])
    row['昼休み'] = convert_for_xls(row['昼休み'])
    # \t はタブです。
    # NOTE: タブ区切りの行をコピペすると xls ではひとつずつセルに入ります。
    text_2_to_output += '\t'.join([
        row['開始'],
        row['終了'],
        row['所定時間'],
        row['超過勤務'],
        row['昼休み'],
    ]) + '\n'
# 開始〜昼休みの一覧を、コピペしやすいようファイルに起こします。
with open('開始から昼休み一覧.txt', mode='w') as f:
    f.write(text_2_to_output)

"""







