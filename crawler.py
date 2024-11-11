import requests
import pandas as pd

def fetch_all_bond_data():
    url = "https://iftp.chinamoney.com.cn/ags/ms/cm-u-bond-md/BondMarketInfoListEN"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }

    # 初始化参数
    page_no = 1
    page_size = 15
    all_bond_data = []

    while True:
        # 设置查询参数
        search_params = {
            "pageNo": page_no,
            "pageSize": page_size,
            "isin": "",
            "bondCode": "",
            "issueEnty": "",
            "bondType": "100001",  # 国债类型
            "couponType": "",
            "issueYear": "2023",
            "rtngShrt": "",
            "bondSpclPrjctVrty": ""
        }

        session = requests.Session()
        result = session.post(url, data=search_params, headers=headers)
        

        if result.status_code == 200:
            json_data = result.json()
            print(json_data)
            total_bonds = json_data['data']['total']
            bond_data = json_data['data'].get('resultList', [])
            
            # 如果没有数据，则停止循环
            if not bond_data:
                break

            # 提取当前页的债券数据
            for bond in bond_data:
                all_bond_data.append([
                    bond.get('isin', 'N/A'),
                    bond.get('bondCode', 'N/A'),
                    bond.get('entyFullName', 'N/A'),
                    bond.get('bondType', 'N/A'),
                    bond.get('issueStartDate', 'N/A'),
                    bond.get('debtRtng', 'N/A')
                ])
            
            # 增加页面编号以获取下一页数据
            page_no += 1

            # 如果已获取所有数据，则停止循环
            if page_no > (total_bonds // page_size) + 1:
                break
        else:
            print("Failed to retrieve data")
            break

    # 保存为CSV文件
    columns = ["ISIN", "Bond Code", "Issuer", "Bond Type", "Issue Date", "Latest Rating"]
    df = pd.DataFrame(all_bond_data, columns=columns)
    df.to_csv('treasury_bonds_2023.csv', index=False, encoding='utf-8-sig')
    print("Data saved to treasury_bonds_2023.csv")

# 调用函数
fetch_all_bond_data()