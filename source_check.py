"""读取交接表并核对表结构。"""
import argparse
import csv
from pathlib import Path

TABLES = {
    'parts': (['part', 'printing', 'block', 'maker', 'editions', 'standalone'], ['part'], []),
    'packs': (['pack', 'part', 'amount'], ['pack', 'part'], [('part', 'parts', 'part')]),
    'rights': (['grant', 'block', 'allowed_parts', 'market', 'starts', 'ends', 'bucket', 'metric', 'quota', 'refund_restores', 'basis_pct'], ['grant'], []),
    'transactions': (['line', 'action', 'original', 'transaction_day', 'received', 'market', 'sku', 'component', 'cents', 'quantity', 'status', 'ledger_period'], ['line'], []),
    'reference_prices': (['component', 'market', 'starts', 'ends', 'low', 'high', 'family'], ['component', 'market', 'starts'], []),
    'orders': (['order', 'market', 'date', 'due', 'allowed_packs', 'units', 'price', 'state'], ['order'], []),
}


def read_sources(root):
    """按源资料名称读取原始字段值。"""
    tables = {}
    for name, (fields, key, _) in TABLES.items():
        with (root / f"{name}.csv").open(encoding="utf-8", newline="") as stream:
            reader = csv.reader(stream, strict=True)
            if next(reader, None) != fields:
                raise ValueError(f"{name} 的表头与交接格式不符")
            rows = []
            identities = set()
            for line, values in enumerate(reader, 2):
                if len(values) != len(fields):
                    raise ValueError(f"{name} 第 {line} 行的列数不符")
                record = dict(zip(fields, values))
                if key:
                    identity = tuple(record[field] for field in key)
                    if not all(identity) or identity in identities:
                        raise ValueError(f"{name} 第 {line} 行的主键无效")
                    identities.add(identity)
                rows.append(record)
        tables[name] = rows
    for name, (_, _, references) in TABLES.items():
        for field, source, target in references:
            declared = {record[target] for record in tables[source]}
            for line, record in enumerate(tables[name], 2):
                if record[field] and record[field] not in declared:
                    raise ValueError(f"{name} 第 {line} 行的 {field} 没有来源记录")
    return tables


def main():
    """显示一次交接中的原始记录数。"""
    parser = argparse.ArgumentParser(description="读取并核对交接资料")
    parser.add_argument("folder", type=Path, nargs="?", default=Path(__file__).parent / "资料")
    args = parser.parse_args()
    for name, records in read_sources(args.folder).items():
        print(f"{name} {len(records)} 条")


if __name__ == "__main__":
    main()
