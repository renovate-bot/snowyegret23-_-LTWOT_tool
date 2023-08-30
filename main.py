import json
import re
import csv
import os
import shutil
import urllib.request


def extract_data(name, append_name):
    filename = f"{name}{append_name}"
    print(f"Extract data from {filename}.txt...")
    with open(f"./1.original_txt/{filename}.txt", "r", encoding="utf-8") as f:
        data = f.readlines()
    with open(f"./2.export_csv/{filename}.csv", "w", encoding="utf-8", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["list", "index", "key", "src", "dst"])
        json_data = json.loads(data[1])
        for lst in json_data.keys():
            tmp_lst = json_data[lst].keys()
            pattern = re.compile(r"^.+:[12]$")
            result = [x for x in tmp_lst if pattern.match(x)]
            for n in range(0, len(result), 2):
                index = result[n].split(":")[0]
                key = json_data[lst][result[n]]
                en = json_data[lst][result[n + 1]]
                # 스프레드시트 수식 에러 방지
                if en[0] == "=":
                    print(f"{filename} | {lst} | {index} | {key} | {en}")
                    en = "'" + en
                # fmt: off
                csv_writer.writerow([lst, index, key, en, ""])


def sanitize_linefeed(text: str):
    # 필요시 " " 공백을 <br> 태그로 변경할 수 있음.
    return text.replace("\n", " ")


def download_csv(file_info: dict):
    print("Downloading CSV files...")
    shutil.rmtree("./3.download_csv")
    os.makedirs("./3.download_csv", exist_ok=True)
    for key in file_info.keys():
        name = f"{key}{file_info[key]['append_name']}"
        doc_id = file_info[key]["doc_id"]
        sheet_id = file_info[key]["sheet_id"]
        print(f"Downloading {name}.csv... (doc_id: {doc_id}, sheet_id: {sheet_id}))")
        url = f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv&gid={sheet_id}"
        urllib.request.urlretrieve(url, f"./3.download_csv/{name}.csv")
    print("Download complete.")


def insert_data(name, append_name):
    filename = f"{name}{append_name}"
    print(f"Insert data to {filename}.txt...")
    with open(f"./1.original_txt/{filename}.txt", "r", encoding="utf-8") as f:
        data = f.readlines()
        header = data[0].strip()
        json_data = json.loads(data[1])
    # fmt: off
    with open(f"./3.download_csv/{filename}.csv", "r", encoding="utf-8", newline="") as f:
        csv_list = list(csv.reader(f))
        del csv_list[0] # 헤더 삭제
        for line in csv_list:
            if len(line) > 4 and line[4] != "":
                ko = f"{line[1]}:2"
                json_data[line[0]][ko] = sanitize_linefeed(line[4])
    with open(f"./4.mod_txt/{filename}.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write(header + "\n")
        f.write(json.dumps(json_data, ensure_ascii=True, separators=(",", ":")))


def main(text, down_csv=False):
    # fmt: off
    file_info = {
        "Common_Ingame": {"doc_id": "19DZMQRlFL6tdJ_qSfrSkcfeoLBWq9KRcpEs23vs1ubA", "sheet_id": "1715646735", "append_name": ""},
        "Common_Strings": {"doc_id": "1eE9El2XH1vDvYG9nADfEpOdpdlew9X2dmcuWRJ3-9Og", "sheet_id": "1945704171", "append_name": ""},
        "Lab_Cards": {"doc_id": "14AvjYve48BWqjD2C3DX1lBZxp7zxEXzjmv2pTdlY00o", "sheet_id": "1129878959", "append_name": ""},
        "Lab_Ingame": {"doc_id": "1XYYg-sOkGQnEoGDH6RquoUV2W-I8SYaooJFKZeURPgQ", "sheet_id": "2086660956", "append_name": ""},
        "Lab_RulesTutorial": {"doc_id": "1MTAK-xmnWpJ7BRxkoOQi6-fZ-4BDUxmq0CmLtJI2Nx4", "sheet_id": "900279084", "append_name": ""},
        "Lab_Strings": {"doc_id": "1Bdxm6u0XjzDBDBpKJDRIUmyf7yuCx_IV9WEbhkMiU58", "sheet_id": "413374275", "append_name": ""},
    }
    namelist = list(file_info.keys())
    file_list = [i for i in os.listdir("./1.original_txt") if i.endswith(".txt")]
    for i in file_list:
        name = os.path.splitext(i)[0].split("-", maxsplit=1)
        # fmt: off
        if name[0] in namelist:
            file_info[name[0]]["append_name"] = f"-{name[1]}"
    if down_csv:
        download_csv(file_info)
    for name in file_info.keys():
        if text == "extract":
            extract_data(name, file_info[name]["append_name"])
        elif text == "insert":
            insert_data(name, file_info[name]["append_name"])
        else:
            print("Error: Invalid argument")


if __name__ == "__main__":
    main("extract", down_csv=False)
    # main("insert", down_csv=True)
