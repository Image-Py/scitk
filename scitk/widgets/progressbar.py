import ttkbootstrap as ttk

class ProgressBar ( ttk.Floodgauge ):
	def __init__(self, parent, mask='no task', **key):
		super().__init__(parent, mask=mask, **key)
		self.auto = False
		self.cursor = 0
		self.taskcur = 0
		self.tasks = []
		self.hold()
		self.taskhode()

	def hold(self):
		if self.auto:
			self.cursor = (self.cursor+5)%200
			self.configure(value=100-abs(self.cursor-100))
		self.after(100, self.hold)

	def taskhode(self):
		if len(self.tasks)>0:
			self.taskcur = self.taskcur + 1
			cur = self.taskcur//50%len(self.tasks)
			text, prog = self.tasks[cur]
			self.set(prog(), text + ' {}%')
		self.after(100, self.taskhode)
		
	def set(self, value, mask=None):
		if not mask is None:
			self.configure(mask=mask)
		if value is None: 
			if not self.auto: self.cursor=0
			self.auto = True
		else: 
			self.auto = False
			self.configure(value=value)

	def task(self, tasks):
		self.tasks = tasks

class ProgressBar ( ttk.Frame ):
	def __init__(self, parent, length=100, text='', **key):
		super().__init__(parent)

		self.lab = ttk.Label(self, text=text+' ')
		self.lab.pack(side='left')

		self.pro = ttk.Progressbar(self, length=length, **key)
		self.pro.pack(side='left')

		self.auto = False
		self.cursor = 0
		self.taskcur = 0
		self.tasks = None
		self.hold()
		self.taskhode()

	def hold(self):
		if self.auto:
			self.cursor = (self.cursor+5)%200
			self.pro.config(value=100-abs(self.cursor-100))
		self.after(100, self.hold)

	def taskhode(self):
		if not self.tasks is None:
			if len(self.tasks)>0:
				self.taskcur = self.taskcur + 1
				cur = self.taskcur//50%len(self.tasks)
				text, prog = self.tasks[cur]
				self.set(prog(), text)
			else: self.set(0, '')
		self.after(100, self.taskhode)
		
	def set(self, value, text=None):
		if not text is None:
			self.lab.config(text=text+' ')
		if value is None: 
			if not self.auto: self.cursor=0
			self.auto = True
		else: 
			self.auto = False
			self.pro.config(value=value)

	def task(self, tasks):
		self.tasks = tasks

if __name__ == '__main__':
	app = ttk.Window(size=(500, 500))

	gauge = ProgressBar(
		app,
	    bootstyle='success',
	    mask='Memory Used',
	)
	gauge.pack(fill='y', expand=False, padx=10, pady=10)

	gauge.task([('task1', lambda :None), ('taks2', lambda :10)])
	app.mainloop()