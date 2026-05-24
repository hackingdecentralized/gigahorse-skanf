import argparse
import os
import re


def check_jumptable(prev_out_dir, out_dir):
    prev_jump_to_calldata = os.path.join(prev_out_dir, "JTA_JUMP_To_Calldata.csv")
    prev_jump_to_mload = os.path.join(prev_out_dir, "JTA_JUMP_To_MLOAD.csv")
    prev_jump_to_sload = os.path.join(prev_out_dir, "JTA_JUMP_To_SLOAD.csv")
    prev_jump_to_callvalue = os.path.join(prev_out_dir, "JTA_JUMP_To_CallValue.csv")
                                          
    jump_to_calldata = os.path.join(out_dir, "JTA_JUMP_To_Calldata.csv")
    jump_to_mload = os.path.join(out_dir, "JTA_JUMP_To_MLOAD.csv")
    jump_to_sload = os.path.join(out_dir, "JTA_JUMP_To_SLOAD.csv")
    jump_to_callvalue = os.path.join(out_dir, "JTA_JUMP_To_CallValue.csv")

    is_zero = True
    for jump_to in [jump_to_calldata, jump_to_mload, jump_to_sload, jump_to_callvalue]:
        if not os.path.exists(jump_to):
            continue
        with open(jump_to, "r") as f:
            lines = f.readlines()
            if len(lines) > 1:
                is_zero = False
                break
    
    if is_zero:
        print("DONE")
    else:
        for prev_jump_to, jump_to in zip([prev_jump_to_calldata, prev_jump_to_mload, prev_jump_to_sload, prev_jump_to_callvalue],[jump_to_calldata, prev_jump_to_calldata, prev_jump_to_sload, prev_jump_to_callvalue]):
            lines = set()
            if os.path.exists(prev_jump_to):
                with open(prev_jump_to, "r") as f:
                    prev_lines = f.readlines()
                    for line in prev_lines:
                        if line.startswith("0x"):
                            match = re.search(r'0x[0-9a-z]+?(?=0x|$)', line.strip())
                            if match:
                                dst = int(match.group(0), 16)
                                lines.add(dst)
            if os.path.exists(jump_to):
                with open(jump_to, "r") as f:
                    new_lines = f.readlines()
                    for line in new_lines:
                        if line.startswith("0x"):
                            match = re.search(r'0x[0-9a-z]+?(?=0x|$)', line.strip())
                            if match:
                                dst = int(match.group(0), 16)
                                lines.add(dst)

            lines = sorted(list(lines))

            with open(prev_jump_to, "w") as f:
                for line in lines:
                    f.write(hex(line) + "\n")
        print("REDO")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("prev_out_dir", help="The previous out directory")
    parser.add_argument("out_dir", help="The out directory")
    args = parser.parse_args()
    check_jumptable(args.prev_out_dir, args.out_dir)
