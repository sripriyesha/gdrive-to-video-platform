import subprocess


def run_command(command, return_output=True):
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output_lines = []
    while True:
        output = process.stdout.readline()
        output = str(output.strip(), "utf-8")
        poll = process.poll()

        if output == "" and poll is not None:
            break
        if output:
            if return_output:
                output_lines.append(output)
            print(output)
    return_code = poll

    return (return_code, output_lines)