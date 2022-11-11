import streamlit as st
import requests

def getAllBookstore():
    url = 'https://cloud.culture.tw/frontsite/trans/emapOpenDataAction.do?method=exportEmapJson&typeId=M' 
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    res = response.json()
    return res

def getCountyOption(items):
    optionList = []
    for item in items:
        name = item['cityName'][0:3]
        if name in optionList:
            continue
        else:
            optionList.append(name)
    return optionList

def getDistrictOption(items, target):
    optionList = []
    for item in items:
        name = item['cityName']
        cityname = name[0:3]
        if cityname in target:
            continue
        # 如果 name 裡面不包含我們選取的縣市名稱(target) 則略過該次迭代
        # hint: 使用 if-else 判斷式並且用 continue 跳過
        name.strip()
        district = name[5:]
        if len(district) == 0: continue
        if target in name:
            optionList.append(item)
        # 如果 district 不在 optionList 裡面，將 district 放入 optionList
        # hint: 使用 if-else 判斷式並使用 append 將內容放入 optionList
    return optionList

def getSpecificBookstore(items, county):
    specificBookstoreList = []
    for item in items:
        name = item['cityName']
        if county in name:
            specificBookstoreList.append(item)
    return specificBookstoreList

def getBookstoreInfo(items):
    expanderList = []
    for item in items:
        expander = st.expander(item['name'])
        expander.image(item['representImage'])
        expander.metric('hitRate', item['hitRate'])
        expander.subheader('Introduction')
        expander.write(item['intro'])
        expander.subheader('Address')
        expander.write(item['address'])
        expander.subheader('Open Time')
        expander.write(item['openTime'])
        expander.subheader('Email')
        expander.write(item['email'])
        expanderList.append(expander)
    return expanderList


def app():
    bookstoreList = getAllBookstore()
    countyOption = getCountyOption(bookstoreList)
    st.header('特色書店地圖')
    st.metric('Total bookstore', len(bookstoreList))
    county = st.selectbox('請選擇縣市', countyOption)
    districtOption = getDistrictOption(bookstoreList, county)
    district = st.multiselect('請選擇區域', districtOption)
    specificBookstore = getSpecificBookstore(bookstoreList,district)
    num = len(specificBookstore)
    st.write(f'總共有{num}項結果', num)
    bookstoreInfo = getBookstoreInfo(specificBookstore)

if __name__ == '__main__':
    app()
