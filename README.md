### 目的
使用台北市政府API, 做室內停車位即時資訊<br>
- http://[AWS elastic ip]/api/available?keyword=[car,motor or bus]&area=[區域]

### 流程

1. 先用Download_file.py下載政府提供的.gz 檔，並轉存成json檔（剩餘停車位數.json、臺北市停車場資訊.json）
2. 透過get_data.py取得json中的資料，並存到local端的MySQL中
3. 利用api即可取得最新資訊
