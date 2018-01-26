from ftplib import FTP

HOST = 'ftp.fisski.com'
ftp = FTP(HOST)
ftp.login()
ftp.cwd('/Software/Files/Fislist')
filenames = ftp.nlst('ALFP*.zip')

for filename in filenames:
    print(filename)

ftp.quit()
