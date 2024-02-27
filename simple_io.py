def confirm(s):
    confirm = input(s)
    while(confirm not in list("nNyY")):
        print("Error: Command not recognized", file = sys.stderr)
        confirm = input(s)
    if(confirm in "nN"): return False
    return True

def quoted(s):
    return s if(s[0] == '\"') else '\"' + s + '\"'
