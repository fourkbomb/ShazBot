import re

class Plugin:
	active=True
	pointers=dict()
	ptr=0
	lbracket=False
	lbracks=list()
	rbracks=list()
	pointers[0]=0
	current_phrase=''

	def __init__(self, controller):
		self.controller=controller


	def exec_bf(self, i, pos):
		if self.lbracket and i != ']':
			return -23
		if i=='>':
			self.ptr+=1
			self.pointers.setdefault(self.ptr,0)
		elif i=='<':
			self.ptr-=1
			self.pointers.setdefault(self.ptr,0)
		elif i=='+':
			self.pointers[self.ptr]+=1
		elif i=='-':
			self.pointers[self.ptr]-=1
		elif i=='.':
			#print(chr(self.pointers[self.ptr]),end='')
			self.current_phrase+=chr(self.pointers[self.ptr])
			if self.current_phrase[-1]=="\n":
				self.controller.send_message(current_phrase.strip())
				self.current_phrase=''
		elif i==',':
			#self.pointers[self.ptr]=input()[0]
			self.controller.send_message("operation unsupported: ','")
		elif i=='[':
			self.lbracks.append(pos)
			if self.pointers[self.ptr]==0:
				self.lbracket=True
		elif i==']':
			self.rbracks.append(pos)
			if self.pointers[self.ptr]!=0:
				# go back!
				self.rbracks.pop()
				return self.lbracks.pop()
			if self.lbracket:
				self.lbracket=False
		return -23

	def run(self,bf,pos=0,ep=-23):
		for i in bf:
			if pos > ep and ep != -23:
				return
			num=self.exec_bf(i,pos)
			if num >= 0:
				self.run(bf[num:pos+1],0,pos-num)
			pos+=1

	def on_message(self, msg):
		if msg.startswith("--bf") or re.match(r'[+-.,><\[\]]',msg):
			bf=msg
			if msg.startswith("--bf"):
				bf=msg.split(" ",2)[1]
			self.run(str(bf))
			if self.current_phrase != '':
				self.controller.send_message(self.current_phrase)

	
	

	
	
	
		
