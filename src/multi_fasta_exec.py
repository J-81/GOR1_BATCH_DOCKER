#!/usr/local/bin/python
""" Jonathan Oribello 2020-06-29
Reads an input of fasta files, inputs the sequence into a function, 
parses return values and formats into csv format
includes controls to check for finished sequences
"""
import os
import csv
import time
import argparse
from datetime import datetime

from Bio import SeqIO

SERVICE = "GOR1"
from gor1_server import retrieveGOR1 as SERVICE_FCN 



def _pdb_fasta_description(seqID):
    """ checks if Chain or Chains is in description, if so, it returns correct pdb5ID
    """
    if "Chain " in seqID:
        parts = seqID.split("|")
        return parts[0][0:4] + parts[1].replace("Chain ","")
    elif "Chains " in seqID:
        parts = seqID.split("|")
        return parts[0][0:4] + parts[1].replace("Chains ","")
    else:
        print("Does not appear to be a PDB style fasta descriptor, returning original desription")
        return SeqID

def main(fastafile, rerun_errors=False, interval=1):
    
    # create output directory
    os.makedirs(SERVICE, exist_ok=True)

    # read input file
    with open(fastafile, "r") as f:
        sequences = SeqIO.parse(f,format="fasta")

        # iterate through sequences, run based on main arguments
        for sequence in sequences:
            
            # pause between each run
            # useful for race conditions and for server operations
            time.sleep(interval)
    
            _id = _pdb_fasta_description(sequence.description)
            err_out_name = f"{SERVICE}/ERROR_{_id}.txt"
            out_name = f"{SERVICE}/{_id}.result"
            if os.path.isfile(out_name):
                print(f"Skipping {_id}, already completed")
            elif all((os.path.isfile(err_out_name), rerun_errors==False)):
                print(f"Skipping {_id}, error found and rerun_errors not enabled")
            else:
                try:
                    print(f"Running {SERVICE} with {_id}")
                    result = SERVICE_FCN(str(sequence.seq))
                    with open(out_name, "w") as f:
                        f.write(result)
                    if all((os.path.isfile(err_out_name),rerun_errors==True)):
                        with open(err_out_name, "a") as f:
                            f.write("Succesful Run Accomplished on Rerun")
                except Exception as e:
                    print(f"Error for {_id}, saving error message to {err_out_name}")
                    with open(err_out_name, "w") as f:
                        f.write(f"{datetime.now()}\n\nstr(e)")

def __argparse():
    # Create the parser
    my_parser = argparse.ArgumentParser(description=f"Runs {SERVICE} against input fasta file")
    
    # Add the arguments
    my_parser.add_argument('input_file',
                           type=str,
                           help='Path to a multiple sequence fasta file')
    
    my_parser.add_argument('rerun_errors',
                           type=bool,
                           help='Reruns pdb IDs which caused an error previously',
                           nargs="*",
                           default=False)
    
    # Execute the parse_args() method
    return my_parser.parse_args()

if __name__ == "__main__":
    args = __argparse()
    main(fastafile=args.input_file, rerun_errors=args.rerun_errors)
