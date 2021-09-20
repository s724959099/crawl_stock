import requests
from pyquery import PyQuery as pq
import re
import typing


def find_apple(st_date: str, end_date: str) -> typing.List[typing.Dict[str, typing.Any]]:
    pattern = r'^\d{4}/\d{2}/\d{2}$'
    assert re.match(pattern, st_date), 'start date error'
    assert re.match(pattern, end_date), 'end date error'
    url = 'https://cn.investing.com/instruments/HistoricalDataAjax'
    data = {
        'curr_id': '6408',
        'smlID': '1159963',
        'header': 'AAPL历史数据',
        'st_date': st_date,
        'end_date': end_date,
        'interval_sec': 'Daily',
        'sort_col': 'date',
        'sort_ord': 'DESC',
        'action': 'historical_data',
    }
    headers = {
        'accept': 'text/plain, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-TW,zh;q=0.9,en;q=0.8,zh-CN;q=0.7,en-US;q=0.6',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    r = requests.post(url, data=data, headers=headers)
    doc = r.text
    dom = pq(doc)
    res = []
    for el in dom('#curr_table tbody tr').items():
        item = {
            'date': el('td').eq(0).text(),
            'close': el('td').eq(1).text(),
            'open': el('td').eq(2).text(),
            'high': el('td').eq(3).text(),
            'low': el('td').eq(4).text(),
            'vol': el('td').eq(5).text(),
        }
        res.append(item)
    return res


if __name__ == '__main__':
    st_date = '2021/05/20'
    end_date = '2021/08/20'
    res = find_apple(st_date, end_date)
    print(res)
