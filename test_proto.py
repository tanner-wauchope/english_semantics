from proto import lex


def test_lex():
    assert lex('\t_ Ab 12\n') == ['_', 'Ab', '12']
    assert lex('!#$%&()*+,-./:;<=>?@[\\]^_`{|}~') == \
          list('!#$%&()*+,-./:;<=>?@[\\]^_`{|}~')
