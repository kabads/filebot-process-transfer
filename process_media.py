import sh
import argparse
import os
import sys

SSH_PRIV_KEY = 'ssh -i /home/adam/.ssh/id_rsa'
REMOTE_LOCATION = "adam@pi:/mnt/2tb/kabads-films/"

parser = argparse.ArgumentParser(description='Process media files')
parser.add_argument('source', type=str, help='Source file')
args = parser.parse_args()


def find_output(line):
    file = line.split('[')[-1].replace(']', '')
    filename = os.path.basename(file)
    return filename


def process_media(source):
    if not os.path.exists(source):
        sys.exit("File does not exist")
    filename = None
    if sh.which('filebot'):
        result = sh.filebot('-non-strict', '-rename', source) #, _out=find_output, _err=find_output)
        output = result.split('\n')
        filename = find_output(output[-3])
        return filename

def main():

    filename = process_media(args.source)
    print(f"Processed filename: {filename}")

    # Let's move the file to the remote location
    try:
        sh.rsync ('-avz', '-e', SSH_PRIV_KEY, filename, REMOTE_LOCATION)
    except sh.ErrorReturnCode as e:
        print('Error in file transfer: {e}')
    except Exception as e:
        print('Unexpected error: {e}')
        traceback.print_exc()
    # Let's delete the file now it has been processed
    sh.rm(filename)

if __name__ == '__main__':
    main()
