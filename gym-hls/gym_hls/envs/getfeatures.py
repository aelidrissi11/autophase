import re 
import geto3
import subprocess
from  subprocess import call
import os
import getpgm

#features = [' # of BB where total args for phi nodes is [1, 5]', " # of BB's with Phi node # in range (0, 3]", " # of BB's with no Phi nodes", ' # of Phinodes at beginning of BB', ' # of calls that return an int', ' Binary operations with a constant operand', ' # of Add insts', ' # of And insts', " # of BB's with instructions between [15, 500]", " # of BB's with less than 15 instructions", ' # of Br insts', ' # of Call insts', ' # of GetElementPtr insts', ' # of ICmp insts', ' # of LShr insts', ' # of Load insts', ' # of PHI insts', ' # of Ret insts', ' # of SExt insts', ' # of Select insts', ' # of Shl insts', ' # of Store insts', ' # of Trunc insts', ' # of Xor insts', ' # of ZExt insts', ' # of basic blocks', ' # of instructions (of all types)', ' # of memory instructions', ' # of nonexternal functions', ' Total arguments to Phi nodes', ' Unary']
features = ["# of BB where total args for phi nodes > 5", "# of BB where total args for phi nodes is [1, 5]", "# of BB's with 1 predecessor", "# of BB's with 1 predecessor and 1 successor", "# of BB's with 1 predecessor and 2 successors", "# of BB's with 1 successor", "# of BB's with 2 predecessors", "# of BB's with 2 predecessors and 1 successor", "# of BB's with 2 predecessors and successors", "# of BB's with 2 successors", "# of BB's with >2 predecessors", "# of BB's with Phi node # in range (0, 3]", "# of BB's with more than 3 Phi nodes", "# of BB's with no Phi nodes", "# of Phi-nodes at beginning of BB", "# of branches", "# of calls that return an int", "# of critical edges", "# of edges", "# of occurrences of 32-bit integer constants", "# of occurrences of 64-bit integer constants", "# of occurrences of constant 0", "# of occurrences of constant 1", "# of unconditional branches", "Binary operations with a constant operand", "Number of AShr insts", "Number of Add insts", "Number of Alloca insts", "Number of And insts", "Number of BB's with instructions between [15, 500]", "Number of BB's with less than 15 instructions", "Number of BitCast insts", "Number of Br insts", "Number of Call insts", "Number of GetElementPtr insts", "Number of ICmp insts", "Number of LShr insts", "Number of Load insts", "Number of Mul insts", "Number of Or insts", "Number of PHI insts", "Number of Ret insts", "Number of SExt insts", "Number of Select insts", "Number of Shl insts", "Number of Store insts", "Number of Sub insts", "Number of Trunc insts", "Number of Xor insts", "Number of ZExt insts", "Number of basic blocks", "Number of instructions (of all types)", "Number of memory instructions", "Number of non-external functions", "Total arguments to Phi nodes", "Unary"] 


def run_stats(bc_code, path="."):
    opt_path = "/scratch/qijing.huang/LegUp/legup-4.0/llvm/Release+Asserts/bin/"
    cmd = opt_path + "opt -stats -instcount " + bc_code + " "
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=path)
    (out, err) = proc.communicate()
    #print (err)
    m = parse_static_features_str(err)
    return m
    

def parse_static_features_str(out):
    feat_ids = []
    for feature in features: 
      my_regex = r"\s*(\d+) instcount - " + re.escape(feature)
      p = re.compile(my_regex) 
      m = p.findall(out.decode("utf-8"))
      if len(m):
        feat_ids.append(int(m[0]))
      else:
        feat_ids.append(0) 
      
    #print (len(feat_ids))
    #print (feat_ids)
    return feat_ids


#parse_static_features("static_features.txt")

def get_pgm_list():
    pgms = getpgm.lsFiles()
    pgms = pgms[0:1]
    return pgms 

def main ():
    fout = open("features.txt", "w")
    fout_o3 = open("features_o3.txt", "w")

    # Change to skeleton foler 
    os.chdir("./examples")
    pgms = ['gsm.c']

    #print(len(features))
    fout.write(str(features) + "\n")
    fout_o3.write(str(features) + "\n")
    for pgm in pgms: 
        # Copy to skeleton folder 
        # getpgm.copyFile(pgm, "../dataset", "../skeleton_o3")
        print("Program: %s" % pgm)

        c_code = pgm.replace('.c', '') 
        fout.write(c_code + "\t")
        fout_o3.write(c_code + "\t")
        # Compile the program with -O3
        geto3.getO3Cycles(c_code) 

        bc_code = c_code + ".prelto.bc" 
        bc_code_o3 = c_code + ".bc"

        feat = run_stats(bc_code)
        feat_o3 = run_stats(bc_code_o3) 

        fout.write(str(feat) + "\n")
        fout_o3.write(str(feat_o3) + "\n")
                
        #getpgm.rmFile(pgm, "../skeleton_o3")
        #call(["make", "clean"])
    fout.close()
    fout_o3.close()

if __name__ == "__main__":
    main()
