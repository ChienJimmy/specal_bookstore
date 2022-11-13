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

def getDistrictOption(items, county):
    distList = []
    for item in items:
        name = item['cityName']
        ctname = name[0:3]
        name.strip()
        dist = name[5:]
        if len(dist) == 0:
            continue
        if county in ctname:
            if dist in distList:
                continue
            else:
                distList.append(dist)
    return distList

def getSpecificBookstore(items, district):
    specificBookstoreList = []
    for item in items:
        name = item['cityName']
        for dist in district:
            if dist in name:
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
