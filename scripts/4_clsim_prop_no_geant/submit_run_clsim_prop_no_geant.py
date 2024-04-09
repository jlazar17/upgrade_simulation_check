import pycondor
import sys
import os

XLINES = [
    "request_memory = (NumJobStarts is undefined) ? 2 * pow(2, 10) : 1024 * pow(2, NumJobStarts + 1)",
    "periodic_release = (HoldReasonCode =?= 21 && HoldReasonSubCode =?= 1001) || HoldReasonCode =?= 21",
    "periodic_remove = (JobStatus =?= 5 && (HoldReasonCode =!= 34 && HoldReasonCode =!= 21)) || (RequestMemory > 13192)"
]

def initialize_args():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--infiles",
        nargs="+",
        required=True
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default=f"{os.path.expanduser('~')}/condor_logs/run_clsim_prop_no_geant/"
    )
    return parser.parse_args()

def main():

    args = initialize_args()
    output = f"{args.prefix}/output/"
    log = f"{args.prefix}/log/"
    error = f"{args.prefix}/error/"
    submit = f"{args.prefix}/submit/"
    
    run = pycondor.Job(
        "run_clsim_prop_no_geant",
        f"{os.getcwd()}/run_clsim_prop_no_geant.sh", 
        error=error, 
        output=output, 
        log=log, 
        submit=submit, 
        universe="vanilla", 
        notification="never",
        verbose=2,
        extra_lines=XLINES
    )
    infiles = [os.path.realpath(f) for f in args.infiles]
    run.add_arg(" ".join(infiles))
    run.build()

if __name__=="__main__":
    main()
