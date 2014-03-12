import subprocess

args = ["ssh","rjw41005@scarf.rl.ac.uk","-p 2222"]
handle = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
handle.stdin.write("ls")

print("test")