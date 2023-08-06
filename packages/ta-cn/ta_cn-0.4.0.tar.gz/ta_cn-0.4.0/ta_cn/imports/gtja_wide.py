"""
通达信公式转alpha191

国泰君安－基于短周期价量特征的多因子选股
"""

from ta_cn.imports import wide as W

CORR = W.CORREL
REGSLOPE = W.LINEARREG_SLOPE
MEAN = W.SMA_TA
WMA = W.SMA_TA  # !!!WMA的公式没看懂，所以用另一个替代，以后再改
DECAYLINEAR = W.WMA

CUMPROD = W.CUMPROD
FILTER = W.FILTER
RANK = W.RANK
TSRANK = W.TS_RANK
LessThan = W.LessThan

IF = W.IF
ABS = W.ABS
LOG = W.LN  # 这里是用的自然对数
MAX = W.MAX2
MIN = W.MIN2
SIGN = W.SGN

SMA = W.SMA

COUNT = W.COUNT
DELTA = W.DIFF
TSMAX = W.HHV
HIGHDAY = W.HHVBARS
TSMIN = W.LLV
LOWDAY = W.LLVBARS
MA = W.MA
PROD = W.PRODUCT
DELAY = W.REF
SUM = W.SUM
SUMIF = W.SUMIF  # 注意，SUMIF参数的位置常用的方式不同

REGBETA = W.SLOPE_YX_NB
REGRESI = W.REGRESI4

COVIANCE = W.COVAR
STD = W.STDP  # 引入的是全体标准差
