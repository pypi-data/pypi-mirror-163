# gpquant说明文档
## 介绍
gpquant是对Python的遗传算法包[gplearn](https://gplearn.readthedocs.io/en/stable/)的一个改造，用于进行因子挖掘
## 模块
### Function
计算因子的函数，用仿函数类Function实现了23个基本函数和37个时间序列函数。所有的函数本质上都是标量函数，但因为采用了向量化计算，所以输入和输出都是向量形式
### Fitness
适应度评价指标，用仿函数类Fitness实现了几个适应度函数，主要是应用其中的夏普比率sharpe_ratio
### Backtester
向量化的因子回测框架，逻辑是先根据定义的策略函数把拿到的因子factor变成信号signal，再通过信号处理函数把信号signal变成资产asset实现回测，这两步统一在仿函数Backtester类里实现
### SyntaxTree
公式树，把因子的计算公式写成前缀表达式，然后用公式树SyntaxTree表示。每一个公式树代表一个因子，由节点Node构成；每个Node存放了自身数据、父节点和子节点。节点的自身数据可以是Function、变量、常量，或者时间序列常数

公式树可以交叉crossover、子树突变subtree_mutate、提升突变hoist_mutate、点突变point_mutate或者繁殖reproduce（逻辑可参照gplearn）
### SymbolicRegressor
符号回归类，gpquant因子挖掘本质上是用遗传算法解决符号回归问题，其中定义了遗传过程中的一些参数，如种群数量population_size、遗传代数generations等

## 使用
### 导入
下载gpquant包（pip install gpquant），导入SymbolicRegressor类
```Python
from gpquant.SymbolicRegressor import SymbolicRegressor
```
### 测试
跟gplearn一样的例子，把$y=X_0^2 - X_1^2 + X_1 - 1$对$X_0$和$X_1$进行符号回归，大约在第9代能找到正确答案
```Python
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.utils import *
from gpquant.SymbolicRegressor import SymbolicRegressor


# Step 1
x0 = np.arange(-1, 1, 1/10.)
x1 = np.arange(-1, 1, 1/10.)
x0, x1 = np.meshgrid(x0, x1)
y_truth = x0**2 - x1**2 + x1 - 1

ax = plt.figure().gca(projection='3d')
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
surf = ax.plot_surface(x0, x1, y_truth, rstride=1, cstride=1,
                       color='green', alpha=0.5)
plt.show()

# Step 2
rng = check_random_state(0)

# training samples
X_train = rng.uniform(-1, 1, 100).reshape(50, 2)
y_train = X_train[:, 0]**2 - X_train[:, 1]**2 + X_train[:, 1] - 1
X_train = pd.DataFrame(X_train, columns=['X0', 'X1'])
y_train = pd.Series(y_train)

# testing samples
X_test = rng.uniform(-1, 1, 100).reshape(50, 2)
y_test = X_test[:, 0]**2 - X_test[:, 1]**2 + X_test[:, 1] - 1

# Step 3
sr = SymbolicRegressor(population_size = 2000,
                       tournament_size = 20,
                       generations = 20,
                       stopping_criteria = 0.01,
                       p_crossover = 0.7,
                       p_subtree_mutate = 0.1,
                       p_hoist_mutate = 0.1,
                       p_point_mutate = 0.05,
                       init_depth = (6, 8),
                       init_method = 'half and half',
                       function_set = ['add', 'sub', 'mul', 'div', 'square'],
                       variable_set = ['X0', 'X1'],
                       const_range = (0, 1),
                       ts_const_range = (0, 1),
                       build_preference = [0.75, 0.75],
                       metric = 'mean absolute error',
                       parsimony_coefficient = 0.01)

sr.fit(X_train, y_train)

# Step 4
print(sr.best_estimator)
```
