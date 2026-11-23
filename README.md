# 馆校版画套装的销售与授权凭证

馆方的生产用授权和印售账务按部件归集，套装款项以整数分记账。

## 资料来源与口径

以下均为本地合成记录。CSV 为 UTF-8，空白字段表示来源未提供值。时间均按北京时间，日期和分钟采用原资料的业务口径。

交易合同按交易发生地和当地日期生效。金额均为分。版次是实际货品印次，底版属于作品图案共享额度，套装部件份数不一定等于盒数。已结账簿可追加更正分录。

### `资料/parts.csv`

part 是部件号。printing 为货品名，block 是可共用额度的底版。standalone 表示有独立销售的规格。

主键 `part`。

### `资料/packs.csv`

每个组合包含各 amount 件部件。同一已付订单仅允许一次履约，orders 中另列可接受组合。

主键 `pack`、`part`。

### `资料/rights.csv`

bucket 同号消耗同一权利额度，entitlement 不同日期并用仍共享。refund_restores 指退款凭证仅在作品实物退回时恢复额度，纯价差退款可以更正应分款但不恢复该交易已占额度。

主键 `grant`。

### `资料/transactions.csv`

sell 初始售出，price_refund 仅退差价，part_refund 退部件，exchange_out/in 是换货的原部件退出与新部件进入。original 引用原交易行。component 非空可定位具体件。closed 是已对账期间。

主键 `line`。

### `资料/reference_prices.csv`

low/high 为没有充分同期独立销售时合同允许的单件参照范围。真实单售同渠道同期时优先，联系每盒净额时统一考虑全部部件。

主键 `component`、`market`、`starts`。

### `资料/orders.csv`

每盒 price，订单不拆，paid 为付款承诺，其余为下一轮可比候选。

主键 `order`。

## 读取交接资料

使用 Python 3.11。下面的入口读取本地交接表并检查表头、主键和已知引用。单元测试覆盖资料读取和已记录的基础契约。

```sh
python3 source_check.py
python3 -m unittest discover -s tests -v
```
