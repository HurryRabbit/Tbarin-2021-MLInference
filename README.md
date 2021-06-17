# Serverless ML Inference API 架構分享

## Why Serverless?
使用API進行預測一直是玉山AI挑戰賽的一大亮點，API的形式能靈活的將機器學習的成果整合在現有的系統中，可謂是非常實用的應用方式。
想像只要銀行行員上傳客戶手寫的掃描圖片，經過手寫辨識API處理後，便能轉換成文字被自動輸入在銀行系統中，可以節省大量輸入資料的人力以及減少無可避免的人為錯誤。

然而，現實中ML推論API的實踐，在費用及流量上有相當的限制──
開一台host API 的server需要24/7全年無休的運行，而實際上API的使用卻可能大多集中在上班時間。另一方面，Server還需要有足夠強的算力應付可能同時湧進的大量request (例如，銀行三點半關門後的行政作業時間可能會是資料輸入高峰期)，如此一來選用的伺服器費用也不可能便宜。更別說當server算力需要升級時，整個API需要下線維護等待重啟，造成時間金錢上的損失。

![](https://i.imgur.com/H0wvmZL.png)

傳統伺服器流量的痛點，出處: https://www.getshifter.io/shifter-in-action/

於是無伺服器(Serverless)架構便為了這種流量變化大的需求提供了最佳解法: 只在API被呼叫時喚醒機器進行計算、可應付瞬間高流量、且日後流量漸增時不需要停機擴充。

## 需求規格
- **流量:** 可同時處理至少1000個request，隨需升級
- **穩定度:** 在API call同時處理量穩定情況下，ML Inference耗時 在超過99%情況下皆<1000ms
- **可靠度:** 在API call同時處理量短時間內暴衝情況下，仍可在5s內回傳結果

## 雲端資源
| AWS資源名稱 | 規格 | 費用 |
| -------- | -------- | -------- |
| API Gateway    | standard    | $1/百萬次 API call     |
| Lambda    | 8GB RAM   | $0.2/百萬次喚醒 <br> $0.133/每執行1000秒   |

<br>

以這次的ML Inference API為例，假設使用8GB記憶體的機器，用API進行推論每天1萬次，每次執行0.5秒，30天中運行22個工作天，計算傳統伺服器跟Serverless的費用差距(不考慮免費額度):

![](https://i.imgur.com/wzkKqm7.png)
此案例中成本差距高達77.5%以上。流量需求尖峰離峰差異愈大，無伺服器架構的優勢愈明顯。

## 系統架構

![](https://i.imgur.com/cee9q00.jpg)


**架構簡介**
- API Gateway用於接收來自外部的API請求，並喚醒Lambda函數
- Lambda函數進行數據前處理&推論
(按照需求可以分別放在兩個不同Lambda串聯，或者放在同個Lambda函數中)
- EFS (Elastic File System)用於存放Lambda中需要呼叫的package以及ML model
(作為一個虛擬local drive的概念，每一次lambda執行時都可與其內容互動)

## 系統維運

### API使用情況監控
使用AWS Cloudwatch建立Dashboard監控API使用情形
所有指標(執行時間、執行次數等)皆可使用現成功能呈現
![](https://i.imgur.com/Yq8dVvr.png)

### 運行紀錄與排錯
所有Lambda的運行log都會被自動存放至AWS Cloudwatch，可以使用網頁UI或者AWS SDK存取
![](https://i.imgur.com/vPku7e0.png)

### Python Script改版
在lambda介面上傳或輸入新版程式碼，並佈署成新的版本
在佈署後，之後進來的api call都會改為執行新版程式碼，**無停機時間**
![](https://i.imgur.com/EGjPAbj.png)

### Model改版
使用AWS EC2虛擬機或是sFTP覆蓋原本在EFS中的model檔案即可，**無停機時間**

## 資料安全
API Gateway可使用API金鑰(API Key)驗證，確保不會被惡意濫用
<br>又API Gateway是AWS的全託管服務之一，AWS會定期測試安全性並且遵循國際資安標準

## Lambda程式碼範例
https://github.com/HurryRabbit/Tbarin-2021-MLInference/blob/e6d5a74db1c1bfd87bae78d50133698713a0bbfd/inference_lambda.py
