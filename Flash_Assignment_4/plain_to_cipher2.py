import pexpect

child = pexpect.spawn('/usr/bin/ssh students@172.27.26.188')
child.expect('students@172.27.26.188\'s password:')
child.sendline('cs641a')
child.expect('Enter your group name: ', timeout=50) 
child.sendline("flash")

child.expect('Enter password: ', timeout=50)
child.sendline("Gate_Toppers")

child.expect('\r\n\r\n\r\nYou have solved 4 levels so far.\r\nLevel you want to start at: ', timeout=50)
# Note: After clearing level 4 this needs to be changed to "solved 4 levels so far"
child.sendline("4")

child.expect('.*')
child.sendline("read")

child.expect('.*')

f = open("plaintexts2.txt", 'r')
f1= open("ciphertexts2.txt",'w')

for line in f.readlines():
	child.sendline(line)
	print(child.before)
	f1.writelines(str(child.before)[48:64]+"\n")
	child.expect("Slowly, a new text starts*")
	child.sendline("c")
	child.expect('The text in the screen vanishes!')

data = child.read()
print(data)
child.close()
print(child.before, child.after)

f.close()
f1.close()
