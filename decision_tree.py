import numpy as np
import random
from typing import List, Dict, Tuple

# Converts a string to a number
def to_number(s:str) -> float:
    s = s.strip()
    if s == '' or s == '?':
        return np.nan
    return float(s)

# Returns true iff s represents a number
def is_number(s:str) -> bool:
    try:
        to_number(s)
    except:
        return False
    return True

# Divides the data on a random attribute.
# Returns the two halves, and information about how the data was split.
def divide_data(data:List[List[str]], label_col:int) -> Tuple[List[List[str]],List[List[str]],int,str,bool]:
    for attempt in range(min(6, len(data) - 1)): # Try a few times
        row_index = random.randrange(len(data))
        row = data[row_index]
        col_index = random.randrange(len(row) - 1)
        col_index += (1 if col_index >= label_col else 0)
        value = row[col_index].strip()
        a:List[List[str]] = []
        b:List[List[str]] = []
        _isnumber = False
        if is_number(value):
            _isnumber = True
            val = to_number(value)
            if np.isnan(val):
                for i in range(len(data)):
                    if np.isnan(to_number(data[i][col_index])):
                        b.append(data[i])
                    else:
                        a.append(data[i])
            else:
                for i in range(len(data)):
                    if to_number(data[i][col_index]) >= val:
                        b.append(data[i])
                    else:
                        a.append(data[i])
        else:
            for i in range(len(data)):
                if data[i][col_index].strip() == value:
                    b.append(data[i])
                else:
                    a.append(data[i])
        if len(a) == 0 or len(b) == 0:
            continue
        return a, b, col_index, value, _isnumber
    raise ValueError('Failed to divide data')

# Returns the mean of numerical values,
# or the most common categorical value.
def summarize_labels(data:List[List[str]], label_col:int) -> str:
    if len(data) == 1:
        # print(f'rows={len(data)}')
        # print(f'cols={len(data[0])}')
        # print(f'label_col={label_col}')
        return data[0][label_col]
    numerical = True
    for i in range(len(data)):
        # print(f'cols_in_row_{i}={len(data[i])}, label_col={label_col}')
        if not is_number(data[i][label_col]):
            numerical = False
            break
    if numerical:
        # Compute the mean
        sum = 0.
        val_count = 0
        for i in range(len(data)):
            try:
                val = to_number(data[i][label_col])
                if not np.isnan(val):
                    val_count += 1
                    sum += val
            except:
                pass
        return str(sum / val_count) if val_count > 0 else '?'
    else:
        # Find the most common value
        counts:Dict[str,int] = {}
        for i in range(len(data)):
            value = data[i][label_col].strip()
            if value in counts:
                counts[value] += 1
            else:
                counts[value] = 1
        most = 0
        for k in counts:
            if counts[k] > most:
                most = counts[k]
                value = k
        return value


class Tree():
    def __init__(self, data:List[List[str]], label_col:int) -> None:
        assert len(data) > 0, "Expected at least one row of data"
        assert label_col < len(data[0]), f"label_col={label_col} out of range for data with {len(data[0])} columns"
        try:
            a, b, col, val, _isnumber = divide_data(data, label_col)
            self.a = Tree(a, label_col)
            self.b = Tree(b, label_col)
            self.col = col
            self.val = val
            self.is_num = _isnumber
            self.label = None
        except:
            self.label = summarize_labels(data, label_col)

    def predict(self, features:List[str]) -> str:
        if not (self.label is None):
            return self.label
        if self.is_num:
            val = to_number(features[self.col])
            if np.isnan(to_number(self.val)):
                if np.isnan(val):
                    return self.b.predict(features)
                else:
                    return self.a.predict(features)
            else:
                if val >= to_number(self.val):
                    return self.b.predict(features)
                else:
                    return self.a.predict(features)
        else:
            if features[self.col].strip() == self.val:
                return self.b.predict(features)
            else:
                return self.a.predict(features)

class Forest():
    def __init__(self, data:List[List[str]], label_col:int, size:int=30) -> None:
        assert len(data) > 0, "Expected at least one row of data"
        assert label_col >= 0, "label_col={label_col} must not be negative"
        assert label_col < len(data[0]), f"label_col={label_col} out of range for data with {len(data[0])} columns"
        self.trees = []
        for i in range(size):
            self.trees.append(Tree(data, label_col))

    def predict(self, features:List[str]) -> str:
        preds:List[List[str]] = []
        for tree in self.trees:
            preds.append([ tree.predict(features) ])
        return summarize_labels(preds, 0)