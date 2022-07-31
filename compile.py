import subprocess
import os
import argparse


def main():
	stickytape()


def stickytape():
	return os.system('stickytape main.py > output.py')


if __name__ == '__main__':
	main()
