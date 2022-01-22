import argparse
from Board import Board
from TUIController import TUIController
from GUIController import GUIController
from AI import AI

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--cli',type=bool,default=False,help='Use depth when detecting faces')
parser.add_argument('--debug',type=bool,default=False,help='Debug mode for CLI checkers')
args = parser.parse_args()

b1 = Board()
if args.cli:
    t1 = TUIController(b1, args.debug)
    t1.play()
else:
    g1 = GUIController(b1)
    g1.play()
  