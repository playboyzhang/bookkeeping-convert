#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 sync_20251106_164627.json 转换为 beecount CSV 格式
"""

import json
import csv
from datetime import datetime
from pathlib import Path


def parse_json_file(json_file_path):
    """解析JSON文件，提取分类、账户和交易记录"""
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 构建分类映射表: cbillid -> 分类信息
    category_map = {}
    if 'bk_user_bill_type' in data:
        for category in data['bk_user_bill_type']:
            category_map[category['cbillid']] = {
                'name': category['cname'],
                'type': category['itype'],  # 0=收入, 1=支出
                'color': category['ccolor'],
            }

    # 构建账户映射表: cfundid -> 账户信息
    account_map = {}
    if 'bk_fund_info' in data:
        for account in data['bk_fund_info']:
            account_map[account['cfundid']] = account['cacctname']

    # 获取交易记录
    transactions = data.get('bk_user_charge', [])

    return category_map, account_map, transactions


def get_transaction_type(charge_type, category_map, ibillid):
    """
    判断交易类型
    charge_type: 1=收入, 2=支出
    category_map: 分类映射表
    ibillid: 分类ID
    """
    # 优先使用 charge_type 判断
    if charge_type == "1":
        return "收入"
    elif charge_type == "2":
        return "支出"

    # 如果 charge_type 无法判断，使用分类的 itype
    if ibillid in category_map:
        category_type = category_map[ibillid]['type']
        if category_type == 0:
            return "收入"
        elif category_type == 1:
            return "支出"

    return "支出"  # 默认为支出


def convert_to_csv_format(transaction, category_map, account_map):
    """
    将单条交易记录转换为CSV格式
    """
    # 获取交易类型
    transaction_type = get_transaction_type(
        transaction.get('chargeType'),
        category_map,
        transaction.get('ibillid')
    )

    # 获取分类名称
    category_name = ""
    if transaction.get('ibillid') in category_map:
        category_name = category_map[transaction['ibillid']]['name']

    # 获取账户名称
    account_name = ""
    if transaction.get('ifunsid') in account_map:
        account_name = account_map[transaction['ifunsid']]

    # 获取金额
    amount = transaction.get('imoney', '0.00')

    # 处理时间
    bill_date = transaction.get('cbilldate', '')
    detail_time = transaction.get('cdetaildate', '')

    # 合并日期和时间
    datetime_str = ""
    if bill_date and detail_time:
        datetime_str = f"{bill_date} {detail_time}"
    elif bill_date:
        datetime_str = bill_date

    # 获取备注
    memo = transaction.get('cmemo', '')

    # 构建CSV行
    # 格式: 类型,分类,二级分类,金额,账户,转出账户,转入账户,备注,时间,标签,附件
    csv_row = [
        transaction_type,  # 类型
        category_name,      # 分类
        "",                # 二级分类 (JSON中没有此字段)
        amount,            # 金额
        account_name,      # 账户
        "",                # 转出账户
        "",                # 转入账户
        memo,              # 备注
        datetime_str,      # 时间
        "",                # 标签
        "",                # 附件
    ]

    return csv_row


def main():
    # 文件路径
    json_file = Path("D:/iflow/bookkeeping/sync_20251106_164627.json")
    csv_file = Path("D:/iflow/bookkeeping/converted_transactions.csv")

    # 解析JSON文件
    print(f"正在解析JSON文件: {json_file}")
    category_map, account_map, transactions = parse_json_file(json_file)

    print(f"找到 {len(category_map)} 个分类")
    print(f"找到 {len(account_map)} 个账户")
    print(f"找到 {len(transactions)} 条交易记录")

    # 转换为CSV格式
    csv_rows = []
    # 添加CSV表头
    csv_rows.append([
        "类型", "分类", "二级分类", "金额", "账户",
        "转出账户", "转入账户", "备注", "时间", "标签", "附件"
    ])

    # 转换每条交易记录
    for transaction in transactions:
        csv_row = convert_to_csv_format(transaction, category_map, account_map)
        csv_rows.append(csv_row)

    # 写入CSV文件
    print(f"正在写入CSV文件: {csv_file}")
    with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)

    print(f"转换完成！共转换 {len(transactions)} 条交易记录")
    print(f"输出文件: {csv_file}")


if __name__ == "__main__":
    main()