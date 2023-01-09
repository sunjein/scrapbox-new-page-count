import datetime
import json
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Scrapboxのエクスポートされたjsonファイルから、ページ数の増加量を作成日を元に表示します。')
    parser.add_argument('input', help='Projectのjsonファイル')
    parser.add_argument('--csv', help='csv形式で出力', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    return args


def open_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def monthly_count(created_list):
    monthly_data = {}
    for i, created in enumerate(created_list):
        month_str = created.strftime("%Y/%m")
        if month_str not in monthly_data:
            monthly_data[month_str] = 1
        else:
            monthly_data[month_str] += 1

    sorted_monthly_data = sorted(monthly_data.items())
    return sorted_monthly_data


def make_csv(monthly_data):
    csv_text = ""
    total = 0
    for month in monthly_data:
        total += month[1]
        csv_text += "{},{}\n".format(month[0], month[1])
    return csv_text


def make_scrapbox_table(monthly_data):
    table_text = "table:page\n"
    table_text += "\t{}\t{}\t{}\t{}\n".format("年/月", "合計", "増加", "コメント")
    total = 0
    for month in monthly_data:
        total += month[1]
        table_text += "\t{}\t{}\t{}\t\n".format(month[0], total, month[1])
    return table_text


def main():
    args = parse_arguments()
    created_list = []
    json_data = open_json(args.input)['pages']
    json_data = sorted(json_data, key=lambda x:x['created'])

    for page in json_data:
        dt = datetime.datetime.fromtimestamp(int(page['created']))
        created_list.append(dt)

    monthly_data = monthly_count(created_list)

    if args.csv:
        csv_text = make_csv(monthly_data)
        print(csv_text)
    else:
        table_text = make_scrapbox_table(monthly_data)
        print(table_text)

if __name__ == '__main__':
    main()
