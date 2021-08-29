import re # Regular Expression

s = "An có mssv là sdasdsads có email là an@gmail.com\nHà có email là 123a@gmail.com"
results = re.findall(r'\w+@+[\w.]+', s)
print(results)
