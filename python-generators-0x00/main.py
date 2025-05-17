# main.py
import sys
processing = __import__('1-batch_processing')
try:
        processing.batch_processing(50)
except BrokenPipeError:
    import sys
    sys.stderr.close()
