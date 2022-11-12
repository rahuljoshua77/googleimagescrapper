myfile = open(f".\pisah.txt","r")
list_account = myfile.read()
list_accountsplit = list_account.split("\n")
for i in list_accountsplit:
    print(i)
    with open('filename.txt','a') as f:
        f.write(i.split("|")[0]+'\n')
    with open('keyword.txt','a') as f:
        f.write(i.split('|')[1]+'\n')