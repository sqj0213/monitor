def convertListToDict( _cf ):
    sectionsList = _cf.sections()
    retDict = {}
    for val1 in sectionsList:
        retDict[ val1 ] = dict( _cf.items( val1 ) )
    return retDict
