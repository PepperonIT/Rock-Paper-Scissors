import paramiko
import sys

def main(ip, pwd, lang, RPS_server_address):
    for obj in (ip, pwd, lang, RPS_server_address):
        assert isinstance(obj, str)
    pythonpath = ":/opt/aldebaran/lib/python2.7/site-packages"

    ssh = paramiko.client.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username="nao", password=pwd, allow_agent=False)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("export PYTHONPATH='{}'; python ./rps/src/app.py {} '{}'".format(pythonpath, lang, RPS_server_address))
    exit_status = ssh_stdout.channel.recv_exit_status()  
    ssh.close()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
