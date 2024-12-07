# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 15:38:19 2024

@author: jyshin
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def TrainData(data):
    
    X = data[['시간', '일', '월',  '일조(hr)', '일사(MJ/m2)', '지면온도(°C)', '습도(%)', '풍속(m/s)', '기온(°C)' ]]
    y = data['시정(10m)']
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 랜덤 포레스트 모델 학습
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)    
    
    # 예측값 생성
    y_pred = model.predict(X_test)
    
    importances = model.feature_importances_

    # 변수 중요도와 특성 이름 출력
    for feature, importance in zip(X_train.columns, importances):
        print(f'{feature}: {importance:.4f}')
    
    # 결과 시각화
    plt.figure(figsize=(8, 6))
    
    # 실제 값 vs 예측 값 비교
    plt.scatter(y_test, y_pred, color='b', label="Predicted vs Original", linewidth=1)
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='r', linestyle='--', label="Good Predicted")
    
    # 그래프 제목 및 레이블
    plt.title("Prediction Result( Original vs Predicted )")
    plt.xlabel("Original")
    plt.ylabel("Predicted")
    plt.legend()
    plt.grid(True)
    plt.show()    
    
    # 1. R² (결정 계수)
    r2 = r2_score(y_test, y_pred)
    
    # 2. 평균 제곱 오차 (MSE)
    mse = mean_squared_error(y_test, y_pred)
    
    # 3. 평균 절대 오차 (MAE)
    mae = mean_absolute_error(y_test, y_pred)
    
    # 결과 출력
    print(f"결정 계수 (R²): {r2:.4f}")
    print(f"평균 제곱 오차 (MSE): {mse:.4f}")
    print(f"평균 절대 오차 (MAE): {mae:.4f}")
    
    

# 데이터 읽기
data = pd.read_csv("merged_data.csv", encoding='utf-8')

# 데이터 학습
TrainData(data)