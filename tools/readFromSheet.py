import requests
import json
import pprint

class read_columns():

    def __init__(self, sheet_name, row_range, access_token):
        self.title_list = []
        self.folder_token = "YEzAsao9khfQ3BtMAiUclcKznsc"
        self.sheet_name = sheet_name
        self.sheet_id_dict = {
            "技术大类": "53196a",
            "商业大类": "WuAvtZ",
            "健康大类": "VP9ODz",
            "爽文短视频": "wipOgq"
        }
        self.row_range = row_range
        self.access_token = access_token
    def readTopicsFromSheet(self):
        url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/"+ self.folder_token +"/values_batch_get"
        params = {
            "ranges": self.sheet_id_dict.get(self.sheet_name)+ "!" +self.row_range,
            "valueRenderOption": "ToString",
            "dateTimeRenderOption": "FormattedString"
        }
        headers = {
            "Authorization": "Bearer " + self.access_token
        }

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            print("响应成功！请查看响应结果")
        else:
            print(f"请求失败，状态码: {response.status_code}")
        
        return response.json()


    def write_to_md_file(response, file_path):
        data = response.json()
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)



    def write2variable(self, response):
        data = response.get('data',[])
        print(type(data))
        value_ranges = data.get('valueRanges',[])

        if not value_ranges or value_ranges == 0:
            print("valueRanges为空，无法获取指定行数据。")
            return []

        for element in value_ranges:
            self.title_list = element['values']
            for title in self.title_list:
                print(title,"已经写入标题列表中")
        
        return self.title_list