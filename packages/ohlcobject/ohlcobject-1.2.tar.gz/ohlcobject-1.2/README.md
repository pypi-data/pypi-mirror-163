为 OHLC 处理去 pandas 化，从而避免大量的 pandas 内存拷贝，达到性能优化的效果（大概 8000%）。  

内部存储为 { "low": [], "high": [] }  

可将 ohlc_object[num]['key'] 的调用转化为 ohlc_object['key'][num] 的调用。  

# init

```
obj = OHLCObject()
obj['open'] = [1, 2, ...]
obj['high'] = [100, 200, ...]
obj['low'] = [1, 2, ...]
obj['close'] = [100, 200, ...]
obj['timestamp'] = [1498924800000, 1498939200000, ...]
return obj
```

# merge (concat OHLC)

Merge obj2 into obj1, automatically sort using 'timestamp' key

```
obj1.merge(obj2)
```

# read

```
obj['low'][1]  # best performance
obj[1]['low']
obj[3:][1]['low']
```
