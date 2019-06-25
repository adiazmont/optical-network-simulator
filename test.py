# Test multiple files for the optical MAN simulator

import sys, os
import subprocess

if len(sys.argv) != 2:
    print("Err: test script must receive a test-file name\n e.g., python test.py test_node")
    sys.exit(0)

os.chdir("../") # change to parent directory
test_file = "opticalMAN.testScripts." + str(sys.argv[1]) # concatenate test file name
subprocess.call(["python", "-m", test_file]) # execute test
