import itertools
import collections
import numpy as np
import cv2

# カラーコード
cols = {'1':0x93818b, '2':0xf3a3b7, '3':0x0b0306, '4':0x5a2a3a, '5':0xfdfdfd, '6':0x114b78, '7':0xed7983}

# カラーidで全セルの色を指定した配列
ids = ['5555555550', 
       '5533335550', 
       '3322223300', 
       '2222222230', 
       '2222222220', 
       '2222222220', 
       '3522235220', 
       '3522235220', 
       '3322233220', 
       '6322263220', 
       '2222222270', 
       '2244222270', 
       '2277222220']


# 明るい色はカラーidを0（＝テトリス盤面上ではブランク）に置き換え。色数が少ないほうがアート探索アルゴリズムの成功確率が高いため。
for id, col in zip(cols, cols.values()):
    if col > 0xe00000 and (col%0x10000 > 0xe000) and (col%0x100 > 0xe0):
        ids = [s.replace(id, '0') for s in ids]


# カラーidが多い順に4, 2, 3, 6, 7, 1, 5となるようidを入れ替える。以下は参考。
# 1:端だと見つかるが、端以外が絶望的
# 2:意外といろんなところ置ける(ただし端から2つ目のところは厳しいかも)
# 3:意外といろんなところ置ける(ただし端から2つ目のところは厳しいかも)
# 4:無敵
# 5:使い所がございません(1dot残せません)
# 6:左端に置くのが絶望的
# 7:右端に置くのが絶望的
id_order_ideal = [4, 2, 3, 6, 7, 1, 5]
replace_dict = {}
ids_reshaped = list(itertools.chain.from_iterable(ids))
i = 0
for (id, _) in collections.Counter(ids_reshaped).most_common():
    if id == '0':
        continue
    else:
        replace_dict[id] = str(id_order_ideal[i])
        i += 1

cols_replaced = {}
cols_replaced_hex = {}
for (id, id_new) in zip(replace_dict, replace_dict.values()):
    cols_replaced[id_new] = cols[id]
    cols_replaced_hex[id_new] = hex(cols[id])
print(cols_replaced_hex)

ids_replaced = []
for id in ids:
    ids_replaced.append(id.translate(str.maketrans(replace_dict)))
print(ids_replaced)


# 描画
# 画像のサイズと背景色
image_width = 800
image_height = 600
background_color = (255, 255, 255)

# 画像を作成
image = np.zeros((image_height, image_width, 3), dtype=np.uint8)
image[:, :] = background_color

# カラーIDに基づいて画像を描画
# x, p, spcingの値を変えると縮尺が変わる（chatgptに書かせたのでよくわからない）
x, y = 25, 25
spacing = 25

for row in ids_replaced:
    for color_id in row:
        if(color_id == '0'):
            x += spacing
            continue
        color = cols_replaced[color_id]
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        image[y:y + spacing, x:x + spacing] = (b, g, r)
        x += spacing

    y += spacing
    x = 50

# 画像を保存
cv2.imwrite("colored_image.png", image)




