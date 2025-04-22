import ttkbootstrap as ttk
from ttkbootstrap.constants import *

app = ttk.Window(size=(500, 500))

gauge = ttk.Floodgauge(
    bootstyle='succsess',
    mask = 'TTT',
)

gauge.pack(fill='y', expand=False, padx=10, pady=10)

# autoincrement the gauge
#gauge.start()
# increment the value by 10 steps
#gauge.step(20)

app.mainloop()
