// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// author © KivancOzbilgic
// developer © KivancOzbilgic
//@version=5
strategy('test')
indicator('AlphaTrend', shorttitle='AT', overlay=true, format=format.price, precision=2, timeframe='')
coeff = input.float(1, 'Multiplier', step=0.1)
AP = input(14, 'Common Period')
ATR = ta.sma(ta.tr, AP)
src = input(close)
showsignalsk = input(title='Show Signals?', defval=true)
novolumedata = input(title='Change calculation (no volume data)?', defval=false)
upT = low - ATR * coeff
downT = high + ATR * coeff
AlphaTrend = 0.0
AlphaTrend := (novolumedata ? ta.rsi(src, 14) >= 50 : ta.mfi(hlc3, 14) >= 50) ? upT < nz(AlphaTrend[1]) ? nz(AlphaTrend[1]) : upT : downT > nz(AlphaTrend[1]) ? nz(AlphaTrend[1]) : downT

color1 = AlphaTrend > AlphaTrend[2] ? #00E60F : AlphaTrend < AlphaTrend[2] ? #80000B : AlphaTrend[1] > AlphaTrend[3] ? #00E60F : #80000B
k1 = plot(AlphaTrend, color=color.new(#0022FC, 0), linewidth=3)
k2 = plot(AlphaTrend[2], color=color.new(#FC0400, 0), linewidth=3)

fill(k1, k2, color=color1)


alertcondition(ta.cross(close, AlphaTrend), title='Cross Alert', message='Price - AlphaTrend Crossing!')
alertcondition(ta.crossover(low, AlphaTrend), title='CrossOver Alarm', message='BUY SIGNAL!')
alertcondition(ta.crossunder(high, AlphaTrend), title='CrossUnder Alarm', message='SELL SIGNAL!')

alertcondition(ta.cross(close[1], AlphaTrend[1]), title='Cross Alert After Bar Close', message='Price - AlphaTrend Crossing!')
alertcondition(ta.crossover(low[1], AlphaTrend[1]), title='CrossOver Alarm After Bar Close', message='BUY SIGNAL!')
alertcondition(ta.crossunder(high[1], AlphaTrend[1]), title='CrossUnder Alarm After Bar Close', message='SELL SIGNAL!')




buySignalk = ta.crossover(AlphaTrend, AlphaTrend[2])
sellSignalk = ta.crossunder(AlphaTrend, AlphaTrend[2])


K1 = ta.barssince(buySignalk)
K2 = ta.barssince(sellSignalk)
O1 = ta.barssince(buySignalk[1])
O2 = ta.barssince(sellSignalk[1])

plotshape(buySignalk and showsignalsk and O1 > K2 ? AlphaTrend[2] * 0.9999 : na, title='BUY', text='BUY', location=location.absolute, style=shape.labelup, size=size.tiny, color=color.new(#0022FC, 0), textcolor=color.new(color.white, 0))

strategy.order("buy", strategy.long, 1, when = buySignalk)

plotshape(sellSignalk and showsignalsk and O2 > K1 ? AlphaTrend[2] * 1.0001 : na, title='SELL', text='SELL', location=location.absolute, style=shape.labeldown, size=size.tiny, color=color.new(color.maroon, 0), textcolor=color.new(color.white, 0))

