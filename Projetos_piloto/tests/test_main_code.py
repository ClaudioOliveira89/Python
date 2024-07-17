import os
import sys
import pytest

# Adicionar o caminho do diretório pai ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main_code import soma, subtracao

def test_soma():
    assert soma(128, 256) == 384
    assert soma(-128, 512) == 384
    assert soma(0, 0) == 0

def test_subtracao():
    assert subtracao(256, 128) == 128
    assert subtracao(886, 256) == 630
    assert subtracao(0, 1) == -1