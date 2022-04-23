"""This module is a main module for tictactoe package"""
from ticitactoe import TerminalView, Field


def main():
    """Main method to init tictactoe game"""
    TerminalView(Field(9)).init_loop()


main()
