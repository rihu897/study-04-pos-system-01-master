import pandas as pd
from os import path
import datetime
import sys

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=int(price)
    
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        # self.item_order_list[0]:商品コード, [1]:個数
        self.item_order_list=[]
        self.item_master=item_master
    
    ## オーダリスト追加メソッド
    def add_item_order(self,item_code):
        # 商品の存在確認
        existence = False
        for item in self.item_master :
            if item_code == item.item_code :
                existence = True
        
        if existence :
            ### 課題4：オーダ登録時に個数も登録できるようにする
            # 商品が存在する場合、個数を入力
            number = 0
            # 1以上の個数が入力されるまで、無限ループ
            while number <= 0 :
                number = int(input("1以上の個数を入力してください："))
            # オーダを追加
            self.item_order_list.append([item_code, number])
            print("オーダを追加しました。")
        else :
            print("ERROR：該当する商品が存在しません。")

    ## オーダリスト出力メソッド    
    def view_item_list(self):
        for item in self.item_order_list:
            print("商品コード:{0}, 個数:{1}".format(item[0], item[1]))
    
### メイン処理
def main():
    ### 課題3：商品マスタをCSVから登録できるようにする
    # マスタ登録
    # CSVファイルを読み込み、データをリストに格納
    csv_path = path.dirname(__file__) + "/ITEM_MASTER.csv"
    df = pd.read_csv(csv_path, dtype=str, encoding='utf-8-sig').values.tolist()
    # 商品単位でインスタンスを作成し、アイテムマスタに格納
    item_master=[]
    for item in df :
        # item[0]:商品コード, [1]:商品名, [2]:価格
        item_master.append(Item(item[0], item[1], item[2]))
    #item_master.append(Item("001","りんご",100))
    #item_master.append(Item("002","なし",120))
    #item_master.append(Item("003","みかん",150))
    
    ### 課題2：オーダをコンソールから登録できるようにする
    # オーダー登録
    order=Order(item_master)
    while True :
        order.add_item_order(input("3桁の商品コードを入力してください(例：001)："))
        # "y"または"n"が入力されるまでループ
        while True :
            choice = input("続けてオーダを登録しますか？（y/n）：")
            if choice == "y" or choice == "n" :
                break
            else :
                print("ERROR：'y'または'n'で入力してください")
        # "n"が入力された場合、オーダ登録を終了
        if choice == "n" :
            break
    #order.add_item_order("001")
    #order.add_item_order("002")
    #order.add_item_order("003")
    #order.add_item_order("004")
    
    # オーダー表示
    order.view_item_list()

    ### 課題1：オーダ登録した商品の一覧を表示
    ### 課題5:オーダ登録した商品の一覧、合計金額、個数を表示
    # レシートファイル出力用リスト
    txt_list = ["--------------------"]
    total = 0
    # 商品一覧表示
    for order in order.item_order_list :
        order_item_code = order[0]
        order_number = int(order[1])
        # 商品コードが一致する商品を検索
        for item in item_master :
            if order_item_code == item.item_code :
                # 商品単位の合計金額を計算
                subtotal = item.price * order_number
                # 合計金額を加算
                total += subtotal
                # レシートファイル出力用リスト更新
                txt_list.append("{0} ¥{1} ({2}ｺ) ¥{3}".format(item.item_name, str(item.price), str(order_number), str(subtotal)))
                print(txt_list[-1])
    # レシートファイル出力用リスト更新
    txt_list.append("--------------------")
    txt_list.append("合計金額：¥{}".format(str(total)))
    print(txt_list[-1])

    ### 課題6：お預かり金額を入力しお釣りを計算
    # 支払い処理
    while True :
        money = int(input("お支払金額を入力してください："))
        if money < total :
            print("お金が足りません！")
            # "y"または"n"が入力されるまでループ
            while True :
                choice = input("再入力しますか？（y/n）")
                if choice == "y" or choice == "n" :
                    break
                else :
                    print("ERROR：'y'または'n'で入力してください")
            # "n"が入力された場合、処理を終了
            if choice == "n" :
                print("処理を中断します")
                sys.exit()
        else :
            # 支払い可能な場合おつりを計算し、ループを終了
            change = money - total
            break
    # レシートファイル用リスト更新
    txt_list.append("お預り：¥{}".format(str(money)))
    txt_list.append("おつり：¥{}".format(str(change)))

    ### 課題7：日付時刻をファイル名としたレシートファイルの出力
    dt_now = datetime.datetime.now()
    receipt_path = path.dirname(__file__) + "/receipt/{}.txt".format(dt_now.strftime("%Y%m%d_%H%M%S"))
    receipt = open(receipt_path, "w", encoding="utf-8")
    for txt in txt_list :
        receipt.write(txt + '\n')
    print("レシートファイルを出力しました。({})".format(receipt_path))
    receipt.close()

if __name__ == "__main__":
    main()