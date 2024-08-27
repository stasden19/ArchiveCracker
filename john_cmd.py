import hashlib
import sqlite3
import subprocess
import os


# Первая команда: ./7z2john.pl 4.7z > 4.hashes

def zip7(archive_path, passlist='passlist.txt'):
    try:
        # os.system('rm 4.hashes')
        os.system('rm john/run/john.pot')
        os.system('rm john/run/john.rec')
    except:
        pass
    command1 = ["./john/run/7z2john.pl", archive_path]
    # print(os.path.splitext(archive_path)[0].split('/')[-1])
    with open(f'static/hashes/{os.path.splitext(archive_path)[0].split('/')[-1]}.hashes', "w") as f:
        subprocess.run(command1, stdout=f)
    with open(f'static/hashes/{os.path.splitext(archive_path)[0].split('/')[-1]}.hashes', "r") as f:
        hashe = f.read()
        if len(hashe) < 10:
            return 'No hash'
        else:
            conn = sqlite3.connect('./static/passwords.db')
            cur = conn.cursor()
            res = cur.execute(f'SELECT password FROM passwords WHERE hash = "{hashlib.sha3_256(hashe.split(":")[1].encode()).hexdigest()}"')
            res = res.fetchall()
            if len(res):
                cur.close()
                conn.close()
                return res[0][0]
    # Вторая команда: ./john --wordlist=passlist.txt 4.hashes
    command2 = ["./john/run/john", f"--wordlist={passlist}",
                f'static/hashes/{os.path.splitext(archive_path)[0].split('/')[-1]}.hashes']
    result = subprocess.run(command2, capture_output=True, text=True)
    # print('stdout: ', result.stdout, 'end stdout')
    return result.stdout


def rar(archive_path, passlist='passlist.txt'):
    try:
        # os.system('rm 4.hashes')
        os.system('rm john/run/john.pot')
    except:
        pass
    command1 = ["./john/run/rar2john", archive_path]
    with open(f'static/hashes/{os.path.splitext(archive_path)[0].split('/')[-1]}.hashes', "w") as f:
        subprocess.run(command1, stdout=f)
    with open(f'static/hashes/{os.path.splitext(archive_path)[0].split('/')[-1]}.hashes', "r") as f:
        hashe = f.read()
        if len(hashe) < 10:
            return 'No hash'
        else:
            conn = sqlite3.connect('./static/passwords.db')
            cur = conn.cursor()
            res = cur.execute(f'SELECT password FROM passwords WHERE hash = "{hashlib.sha3_256(hashe.split(":")[1].encode()).hexdigest()}"')
            res = res.fetchall()
            if len(res):
                cur.close()
                conn.close()
                return res[0][0]

    # Вторая команда: ./john --wordlist=passlist.txt 4.hashes
    command2 = ["./john/run/john", f"--wordlist={passlist}",
                f'static/hashes/{os.path.splitext(archive_path)[0].split('/')[-1]}.hashes']
    result = subprocess.run(command2, capture_output=True, text=True)
    # print('stdout: ', result.stdout, 'end stdout')
    return result.stdout


def zip(archive_path, passlist='passlist.txt'):
    try:
        # os.system('rm 4.hashes')
        os.system('rm john/run/john.pot')
    except:
        pass
    command1 = ["./john/run/zip2john", archive_path]
    with open(f'static/hashes/{os.path.splitext(archive_path)[0].split('/')[-1]}.hashes', "w") as f:
        subprocess.run(command1, stdout=f)
    with open(f'static/hashes/{os.path.splitext(archive_path)[0].split('/')[-1]}.hashes', "r") as f:
        hashe = f.read()
        if len(hashe) < 10:
            return 'No hash'
        else:
            conn = sqlite3.connect('./static/passwords.db')
            cur = conn.cursor()
            res = cur.execute(f'SELECT password FROM passwords WHERE hash = "{hashlib.sha3_256(hashe.split(":")[1].encode()).hexdigest()}"')
            res = res.fetchall()
            if len(res):
                cur.close()
                conn.close()
                return res[0][0]

    # Вторая команда: ./john --wordlist=passlist.txt 4.hashes
    command2 = ["./john/run/john", f"--wordlist={passlist}",
                f'static/hashes/{os.path.splitext(archive_path)[0].split('/')[-1]}.hashes']
    result = subprocess.run(command2, capture_output=True, text=True)
    # print('stdout: ', result.stdout, 'end stdout')
    return result.stdout
