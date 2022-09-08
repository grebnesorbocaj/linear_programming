from lp import LP_Item, LP_Model

x = LP_Item("Table", "2 hours", 15, 90)
y = LP_Item("Chair", "5 hours", 45, 180)
model = LP_Model(x, y, 315, "1 workweeks")