# 记账数据转换工具

将 JSON 格式的记账数据转换为 BeeCount CSV 格式的 Python 脚本。

## 功能说明

本工具可以将从记账应用导出的 JSON 数据文件转换为 BeeCount 应用可识别的 CSV 格式，方便用户在不同记账应用之间迁移数据。

### 支持的转换

- ✅ 交易记录转换（收入/支出）
- ✅ 分类信息映射
- ✅ 账户信息映射
- ✅ 日期时间格式化
- ✅ 备注信息保留

## 使用方法

### 环境要求

- Python 3.6+

### 运行步骤

1. 将 JSON 文件放置在脚本所在目录
2. 运行脚本：
   ```bash
   python convert_json_to_csv.py
   ```
3. 根据提示输入 JSON 文件名（例如：`sync_20260327_102528.json`）
4. 脚本将在同一目录下生成对应的 CSV 文件

## 输入格式

JSON 文件应包含以下数据结构：

- `bk_user_bill_type`: 分类信息
  - `cbillid`: 分类 ID
  - `cname`: 分类名称
  - `itype`: 类型（0=收入，1=支出）
  - `ccolor`: 分类颜色

- `bk_fund_info`: 账户信息
  - `cfundid`: 账户 ID
  - `cacctname`: 账户名称

- `bk_user_charge`: 交易记录
  - `chargeType`: 交易类型（1=收入，2=支出）
  - `ibillid`: 分类 ID
  - `ifunsid`: 账户 ID
  - `imoney`: 金额
  - `cbilldate`: 日期
  - `cdetaildate`: 时间
  - `cmemo`: 备注

## 输出格式

CSV 文件包含以下字段：

| 字段 | 说明 |
|------|------|
| 类型 | 收入/支出 |
| 分类 | 交易分类 |
| 二级分类 | （暂不支持） |
| 金额 | 交易金额 |
| 账户 | 关联账户 |
| 转出账户 | （暂不支持） |
| 转入账户 | （暂不支持） |
| 备注 | 交易备注 |
| 时间 | 交易时间 |
| 标签 | （暂不支持） |
| 附件 | （暂不支持） |

## 示例

### 输入 JSON 文件示例

```json
{
  "bk_user_bill_type": [
    {
      "cbillid": "2001",
      "cname": "工资",
      "itype": 0,
      "ccolor": "#e1861b"
    }
  ],
  "bk_fund_info": [
    {
      "cfundid": "1001",
      "cacctname": "招商银行"
    }
  ],
  "bk_user_charge": [
    {
      "chargeType": "1",
      "ibillid": "2001",
      "ifunsid": "1001",
      "imoney": "10000.00",
      "cbilldate": "2026-03-26",
      "cdetaildate": "14:48:50",
      "cmemo": "三月份工资"
    }
  ]
}
```

### 输出 CSV 文件示例

```csv
类型,分类,二级分类,金额,账户,转出账户,转入账户,备注,时间,标签,附件
收入,工资,,10000.00,招商银行,,,,三月份工资,2026-03-26 14:48:50,,
```

## 注意事项

- CSV 文件使用 UTF-8-BOM 编码，确保 Excel 能正确显示中文
- 时间格式为 `YYYY-MM-DD HH:MM:SS`
- 金额保留两位小数
- 如果 JSON 中缺少某些字段，将使用默认值

## 许可证

MIT License