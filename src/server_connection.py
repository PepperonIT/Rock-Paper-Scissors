import paramiko

def main():
    pythonpath = ""
    addedPaths = [
        ":/opt/aldebaran/lib/python2.7/site-packages",
    ]

    for path in addedPaths:
        pythonpath += path

    ssh = paramiko.client.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("130.240.238.32", username="nao", password="FBLovesLMS2019", allow_agent=False)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("export PYTHONPATH='{}'; python -c 'import sys; print(sys.path)'; python ./rps/rickard/src/app.py".format(pythonpath))
    print(ssh_stdout.read().decode())
    print(ssh_stderr.read().decode())
    ssh.close()

if __name__ == "__main__":
    main()