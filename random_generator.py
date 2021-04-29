import numpy as np
import pandas as pd

classes = ["dog", "cat", "mouse", "horse"]
pmf = [0.5, 0.3, 0.1, 0.1]

a = np.random.choice(classes, 10000, p=pmf, )

total = np.unique(a, return_counts=True)
print(total[0])
print(total[1] / np.sum(total[1]))