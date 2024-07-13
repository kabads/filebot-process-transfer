import sh
import argparse
import os 

SSH_PRIV_KEY = 'ssh -i /home/adam/.ssh/id_rsa'
REMOTE_LOCATION = "adam@pi:/mnt/2tb/kabads-films/"

parser = argparse.ArgumentParser(description='Process media files')
parser.add_argument('source', type=str, help='Source file')
args = parser.parse_args()

def process_output(line):
    print(line)


def find_output(line):
    file = line.split('[')[-1].replace(']', '')
    filename = os.path.basename(file)
    return filename


def process_media(source):
    filename = None
    if sh.which('filebot'):
        result = sh.filebot('-non-strict', '-rename', source) #, _out=find_output, _err=find_output)
        output = result.split('\n')
        filename = find_output(output[-3])
        return filename


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

# Let's rename the file back
sh.mv(filename, args.source)
# TODO Once this process is proven, we can delete the original