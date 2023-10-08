import subprocess, os, re
from consts import *

def execute_privileged_command(command_str):
        '''
        Executes the given privileged command on the device
        '''
        proc = subprocess.Popen(["adb", "shell", "su", "-c", "%s" % command_str], stdout=subprocess.PIPE)
        proc.wait()
        return proc.stdout.read()

def pull_file(remote_path, local_path):
        '''
        Pulls the remote path from the device to the local path
        '''
        proc = subprocess.Popen(["adb", "pull", remote_path, local_path], stdout=subprocess.PIPE)
        proc.wait()

def dev_mem_read_memory(address, length):
        '''
        Reads memory from the device using /dev/mem
        '''
        output = execute_privileged_command("dd if=/dev/mem of=%s bs=1 count=%d skip=%d" %
                     						(REMOTE_TEMP_DUMP_PATH, length, address))
        output = execute_privileged_command("hd %s" % REMOTE_TEMP_DUMP_PATH)
        return "".join(re.findall("^[0-9a-f]{8}: (.*?) s", str(output.decode("hex")), re.MULTILINE)).replace(" ","")
