# from utils.pycui import *
# %%
# color = pycui()
# cui = pycui.pycui()

# cui.info("this is a info message~")
# cui.warning("this is a warning message~")

# color.p("black", color.BLACK)
# color.p("WRONG!", color.RED)
import pandas as pd
x_data = [1,2,3,4]
y_data = [4,5,6,7]
df = pd.DataFrame(index=x_data,data=y_data,columns=["代码行覆盖率"])
df.to_excel("test.xlsx")
# %%
