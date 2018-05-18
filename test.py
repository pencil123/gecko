#! /usr/bin/env python
# -*- coding: utf-8 -*-

# from ctrl.platform import platform
# test = platform()

# from extends.merryguess import MerryGuess
# test = MerryGuess()
# test.guess()

from ctrl.publish import Publish

handler = Publish()
handler.random_publis()