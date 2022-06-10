from pykiwoom.kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

# 주식계좌
accounts = kiwoom.GetLoginInfo("ACCNO")
stock_account = accounts[0]

#주식매도 리스트 및 매도수량
sellList = {}


#주식 매도주문
for i in sellList:
    kiwoom.SendOrder("시장가매도", "0101", stock_account, 2, "005930", 10, 0, "03", "")

#주식매수 리스트 및 매수수량
buyList = {}


#주식 매수주문
for i in buyList:
    kiwoom.SendOrder("시장가매수", "0101", stock_account, 1, "005930", 10, 0, "03", "")



# # 삼성전자, 10주, 시장가주문 매수
# kiwoom.SendOrder("시장가매수", "0101", stock_account, 1, "005930", 10, 0, "03", "")