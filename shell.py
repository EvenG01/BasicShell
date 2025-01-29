import sys
import os
import subprocess

def exit_shell():
    sys.exit(0)

def pwd():
    sys.stdout.write(os.getcwd())
    sys.stdout.write("\n")

def cd(new_path):
    try:
        if new_path == "~":
            os.chdir(os.path.expanduser("~"))
        else:
            os.chdir(new_path)
    except OSError:
        sys.stdout.write(f"cd: {new_path}: No such file or directory\n")

def cmd_not_found(command):
    sys.stdout.write(f"{command}: command not found\n")

def echo(a):
    if a.startswith("'") and a.endswith("'"):
        a = a[1:-1]
    sys.stdout.write(f"{a}\n")

def type(a):
    builtins = ["echo", "type", "exit", "pwd", "cd"]
    if a in builtins:
        sys.stdout.write(f"{a} is a shell builtin\n")
        return
    paths = os.environ.get("PATH").split(':')

    for p in paths:
        full_path = os.path.join(p, a)
        if os.path.exists(full_path):
            sys.stdout.write(f"{a} is {full_path}\n")
            return

    sys.stdout.write(f"{a}: not found\n")

def external_program(args, cmd):

    run = subprocess.run([cmd] + args,  capture_output=True, text=True)
    sys.stdout.write(run.stdout)

    if run.stderr:
        sys.stderr.write(run.stderr)




commands = {"echo": echo,
            "exit": exit_shell,
            "type": type,
            "pwd": pwd,
            "cd": cd,}

def main():
    while True:
        sys.stdout.write("$ ")
        command = input()
        parts = command.split()
        cmd = parts[0]
        text = parts[1:]
        input_data = " ".join(text)


        if cmd in commands:
            if cmd == "echo":
                echo(input_data)

            elif cmd == "type":
                type(text)
                print(text)
            elif cmd == "pwd":
                pwd()
            elif cmd == "cd":
                cd(input_data)
            elif cmd == "exit":
                exit_shell()
            continue

        paths = os.environ.get("PATH").split(':')
        for p in paths:
            full_path = os.path.join(p, cmd)
            if os.path.exists(full_path):
                external_program(text, cmd)
                break

        else:
            cmd_not_found(cmd)


if __name__ == "__main__":
    main()
