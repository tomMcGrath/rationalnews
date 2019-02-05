def parse_keywords_old(x):
    """Parses given string to generate a list of keywords. For example:
    
    >>> parse_keywords('brain OR breast AND tumour OR tumor OR cancer | heart OR lung OR brain AND disease OR disorder OR issue')
    [['brain tumour',
      'brain tumor',
      'brain cancer',
      'breast tumour',
      'breast tumor',
      'breast cancer'],
     ['heart disease',
      'heart disorder',
      'heart issue',
      'lung disease',
      'lung disorder',
      'lung issue',
      'brain disease',
      'brain disorder',
      'brain issue']]
    """
    from itertools import product
    tokens = x.split('|')
    toks_all = list()
    for token in tokens:
        toks = token.split('AND')
        toks_curr = list()
        for tok in toks:
            t = tok.split('OR')
            t = [s.strip() for s in t]
            toks_curr.append(t)
        toks_all.append([' '.join(i).strip().lower() for i in product(*toks_curr, repeat=1)])
    return toks_all


def parse_keywords(x):
    import pyparsing
    content = pyparsing.Word(pyparsing.alphanums)
    parser = pyparsing.nestedExpr( '(', ')', content=content)
    token_list = parser.parseString(x).asList()                    
    return token_list  

