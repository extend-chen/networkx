#!/usr/bin/env python

"""p2g
===
"""

from nose.tools import assert_equal
from networkx import *
import os,tempfile

class TestPajek():
    def test_pajek(self):
        data="""*network Tralala\n*vertices 4\n   1 "A1"         0.0938 0.0896   ellipse x_fact 1 y_fact 1\n   2 "Bb"         0.8188 0.2458   ellipse x_fact 1 y_fact 1\n   3 "C"          0.3688 0.7792   ellipse x_fact 1\n   4 "D2"         0.9583 0.8563   ellipse x_fact 1\n*arcs\n1 1 1  h2 0 w 3 c Blue s 3 a1 -130 k1 0.6 a2 -130 k2 0.6 ap 0.5 l "Bezier loop" lc BlueViolet fos 20 lr 58 lp 0.3 la 360\n2 1 1  h2 0 a1 120 k1 1.3 a2 -120 k2 0.3 ap 25 l "Bezier arc" lphi 270 la 180 lr 19 lp 0.5\n1 2 1  h2 0 a1 40 k1 2.8 a2 30 k2 0.8 ap 25 l "Bezier arc" lphi 90 la 0 lp 0.65\n4 2 -1  h2 0 w 1 k1 -2 k2 250 ap 25 l "Circular arc" c Red lc OrangeRed\n3 4 1  p Dashed h2 0 w 2 c OliveGreen ap 25 l "Straight arc" lc PineGreen\n1 3 1  p Dashed h2 0 w 5 k1 -1 k2 -20 ap 25 l "Oval arc" c Brown lc Black\n3 3 -1  h1 6 w 1 h2 12 k1 -2 k2 -15 ap 0.5 l "Circular loop" c Red lc OrangeRed lphi 270 la 180"""
        G=parse_pajek(data)
        assert_equal(sorted(G.nodes()), ['A1', 'Bb', 'C', 'D2'])
        assert_equal(sorted(G.edges()),
                     [('A1', 'A1'), ('A1', 'Bb'), ('A1', 'C'), ('Bb', 'A1'),
                      ('C', 'C'), ('C', 'D2'), ('D2', 'Bb')])

        (fd,fname)=tempfile.mkstemp()
        fh=open(fname,'w')
        fh.write(data)
        fh.close()
        Gin=read_pajek(fname)
        assert_equal(sorted(G.nodes()), sorted(Gin.nodes()))
        assert_equal(sorted(G.edges()), sorted(Gin.edges()))
        os.close(fd)
        os.unlink(fname)

        (fd,fname)=tempfile.mkstemp()
        write_pajek(G,fname)
        H=read_pajek(fname)
        assert_equal(sorted(H.nodes()), sorted(G.nodes()))
        assert_equal(sorted(G.edges()), sorted(H.edges()))

        # Example without node positions or shape
        data="""*Vertices 2\n1 "1"\n2 "2"\n*Edges\n1 2\n2 1"""
        G=parse_pajek(data)
        assert_equal(sorted(G.nodes()), ['1', '2'])
        assert_equal(sorted(G.edges()), [('1', '2'), ('1', '2')])

