from utils import pycui

color = pycui.color()
cui = pycui.pycui()

cui.info("this is a info message~")
cui.warning("this is a warning message~")

color.p("black", color.BLACK)
color.p("WRONG!", color.RED)
