# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 15:47:39 2024

@author: jyshin
"""

import numpy as np
import pandas as pd


def DataMerge():
    file_paths = [ 
        "2020_chungju.csv",
        "2021_chungju.csv",
        "2022_chungju.csv",
        "2023_chungju.csv"
    ]

    data_list = []

    # 미 사용 데이터 제거
    columns_to_drop = ["지면상태(지면상태코드)", "현상번호(국내식)", "지점명", "지점", "풍향(16방위)", "현지기압(hPa)","해면기압(hPa)"]

    for file_path in file_paths:
        print(f"=== 파일 : {file_path} ===")
        try:
            # csv읽기
            data = pd.read_csv(file_path, encoding='cp949')
            
            # 특정 열 제거
            data = data.drop(columns=columns_to_drop, errors="ignore")
             
            #print("\일조 일사 값 0으로 채우기 (밤에는 해당 값은 0) :")

            # 밤 시간에 결측치를 모두 0으로 채우기        
            data['일시'] = pd.to_datetime(data['일시'])
            night_cond = (data['일시'].dt.hour >= 17) | (data['일시'].dt.hour <= 8)
            
            columns_to_fill_zero = ['일조(hr)', '일사(MJ/m2)']
                   
            for column in columns_to_fill_zero:
               data.loc[night_cond & data[column].isnull(), column] = 0 
           
            # 밤 시간 결측치를 0으로 채우니 대부분 데이터 결측 해결
            #print(data.isnull().sum())
            
            # 처리하지 못한 데이터 0으로 처리
            for column in columns_to_fill_zero:
               data[columns_to_fill_zero] = data[columns_to_fill_zero].fillna(0) 
               
            
            # 강수량 데이터 처리 필요
            data["강수량(mm)"] = data["강수량(mm)"].fillna(0)
            # 강수량 데이터 결측은 0으로 채움( 비 안왔다고 가정 )        
            #print(data.isnull().sum())     
            
            # 나머지 결측치가 있는 행은 제거
            data = data.dropna(axis=0) 
            
            # 일시 데이터 월-일-시간으로 나누기
            #data["일시"] = pd.to_datetime(data["일시"]) 
            data["월"] = data["일시"].dt.month
            data["일"] = data["일시"].dt.day
            data["시간"] = data["일시"].dt.hour    
            
            data = data.drop(columns=["일시"])   
            
            data_list.append(data)        
            
        except Exception as e:
            print(f"오류 : {e}")

    # 4개의 파일 하나로 병합
    merged_data = pd.concat(data_list, ignore_index=True)

    # 외부 경로에 저장
    output_path = "merged_data.csv"
    merged_data.to_csv(output_path, index=False)