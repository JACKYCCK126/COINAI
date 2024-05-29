from selenium_driverless import webdriver
from selenium_driverless.types.by import By
import asyncio
import csv
from datetime import datetime
import os

# 設置 WebDriver 的路徑
url = 'https://dexscreener.com/base?rankBy=pairAge&order=asc'

# 定義數據提取函數
async def extract_data(driver):
    try:
        # 等待頁面加載完成
        await driver.sleep(10)

        # 定位包含數據的主 div
        main_div = await driver.find_element(By.CSS_SELECTOR, '.ds-dex-table.ds-dex-table-new')

        # 查找表格行
        rows = await main_div.find_elements(By.CSS_SELECTOR, 'a.ds-dex-table-row.ds-dex-table-row-new')

        # 提取每行數據
        data = []
        for row in rows:
            try:
                token_elem = await row.find_element(By.CSS_SELECTOR, 'div.ds-table-data-cell.ds-dex-table-row-col-token')
                price_elem = await row.find_element(By.CSS_SELECTOR, 'div.ds-table-data-cell.ds-dex-table-row-col-price')
                pair_age_elem = await row.find_element(By.CSS_SELECTOR, 'div.ds-table-data-cell.ds-dex-table-row-col-pair-age')
                cells = await row.find_elements(By.CSS_SELECTOR, 'div.ds-table-data-cell')

                token = await token_elem.get_property('textContent')
                price = await price_elem.get_property('textContent')
                pair_age = await pair_age_elem.get_property('textContent')
                buys = await cells[3].get_property('textContent')
                sells = await cells[4].get_property('textContent')
                volume = await cells[5].get_property('textContent')
                makers = await cells[6].get_property('textContent')
                five_min_change = await cells[7].get_property('textContent')
                one_hour_change = await cells[8].get_property('textContent')
                six_hour_change = await cells[9].get_property('textContent')
                twenty_four_hour_change = await cells[10].get_property('textContent')
                liquidity = await cells[11].get_property('textContent')
                mcap = await cells[12].get_property('textContent')

                # 提取 URL
                url = await row.get_attribute('href')

                # 將 token 分割為 Token0 和 Token1
                token_parts = token.split('/')
                token0 = token_parts[0] if len(token_parts) > 0 else ""
                token1 = token_parts[1] if len(token_parts) > 1 else ""

                # 獲取當前時間
                run_time = datetime.now().strftime('%Y/%m/%d %I:%M:%S %p')

                row_data = [token0, token1, price, pair_age, buys, sells, volume, makers, five_min_change, one_hour_change, six_hour_change, twenty_four_hour_change, liquidity, mcap, run_time, url]
                data.append(row_data)
                print(row_data)
            except Exception as e:
                print(f"Error processing row: {e}")
        return data
    except Exception as e:
        print(f"Error extracting data: {e}")
        return []

async def main():
    options = webdriver.ChromeOptions()
    async with webdriver.Chrome(options=options) as driver:
        await driver.get(url, wait_load=True)
        data = await extract_data(driver)

        # 指定保存 CSV 文件的路徑
        csv_file_path = 'C:\\COINAI\\selenium_dexscanner\\selenium_dexscanner\\RESULT\\DEX\\dexscreener_data_TEST.csv'
        headers = ['Token0', 'Token1', 'Price', 'Pair Age', 'Buys', 'Sells', 'Volume', 'Makers', '5 Min Change', '1 Hour Change', '6 Hour Change', '24 Hour Change', 'Liquidity', 'MCAP', 'Run Time', 'URL']

        # 確保目錄存在
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

        # 檢查文件是否存在
        file_exists = os.path.isfile(csv_file_path)

        # 以具 BOM 的 UTF-8 編碼保存 CSV 文件，並且使用附加模式
        with open(csv_file_path, 'a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(headers)  # 只在文件不存在時寫入標題
            writer.writerows(data)

        print(f"Data has been saved to {csv_file_path}")

# 執行主函數
asyncio.run(main())
