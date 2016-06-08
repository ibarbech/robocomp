from pyparsing import Word, alphas, alphanums, nums, OneOrMore, CharsNotIn, Literal, Combine
from pyparsing import cppStyleComment, Optional, Suppress, ZeroOrMore, Group, StringEnd, srange
from pyparsing import nestedExpr, CaselessLiteral

import sys, traceback, os





class SMDSLparsing:
    @staticmethod
    def fromFile(filename, verbose=False, includeIncludes=True):
        # Open input file
        # inputText = "\n".join([line for line in open(filename, 'r').read().split("\n") if not line.lstrip(" \t").startswith('//')])
        if filename == "none":
            return "none"
        inputText = open(filename, 'r').read()
        try:
            ret = SMDSLparsing.fromString(inputText)
        except:
            print 'Error reading', filename
            traceback.print_exc()
            print 'Error reading', filename
            sys.exit(1)
        ret['filename'] = filename
        return ret

    @staticmethod
    def fromString(inputText, verbose=False):
        if verbose: print 'Verbose:', verbose
        text = nestedExpr("/*", "*/").suppress().transformString(inputText)

        semicolon = Suppress(Word(";"))
        quote = Suppress(Word("\""))
        op = Suppress(Word("{"))
        cl = Suppress(Word("}"))
        opp = Suppress(Word("("))
        clp = Suppress(Word(")"))
        to = Suppress(CaselessLiteral("=>"))

        identifier = Word(alphas + "_", alphanums + "_")

        list_identifer = identifier + ZeroOrMore(Suppress(Word(',')) + identifier)

#---parse States
        stateslist = Group(Suppress(CaselessLiteral('states')) + list_identifer + semicolon).setResultsName('states')

#---parse Transitions
        transition = Group(identifier.setResultsName('src') + to + list_identifer.setResultsName('dest') + semicolon)
        transitions = Group(Suppress(CaselessLiteral('transition')) + op + transition + ZeroOrMore(transition) + cl + semicolon).setResultsName('transition')

#---parse initialstate finalstate
        initialstate = (Suppress(CaselessLiteral('initial_state')) + identifier + semicolon).setResultsName('initialstate')
        finalstate = (Suppress(CaselessLiteral('end_state')) + identifier + semicolon).setResultsName('finalstate')

#---parse machine
        contents = stateslist | initialstate | finalstate | transitions
        machinecontenido = Group(op + ZeroOrMore(contents) + cl + semicolon)

        parent = Suppress(Word(":")) + identifier
        parallel = CaselessLiteral('parallel')
        substate = Group(parent.setResultsName('parent') + ZeroOrMore(parallel.setResultsName('parallel')) + machinecontenido.setResultsName("contents"))
        machine = identifier.setResultsName("name") + machinecontenido.setResultsName("contents")

#---parse list machine
        machinelist = machine.setResultsName("machine") + ZeroOrMore(substate).setResultsName("substates")

        SMDSL = machinelist.ignore(cppStyleComment)

        tree= SMDSL.parseString(text)
        return SMDSLparsing.component(tree)

    @staticmethod
    def component(tree, start=''):
        component = {}
        component['machine'] = {}
        component['machine']['name'] = tree['machine']['name']
        component['machine']['contents'] = {}
        component['machine']['contents']['states'] = tree['machine']['contents']['states']
        try:
            component['machine']['contents']['finalstate'] = tree['machine']['contents']['finalstate']
        except:
            component['machine']['contents']['finalstate'] = "none"
        try:
            component['machine']['contents']['initialstate'] = tree['machine']['contents']['initialstate']
        except:
            component['machine']['contents']['initialstate'] = "none"
        try:
            component['machine']['contents']['transition'] = tree['machine']['contents']['transition']
        except:
            component['machine']['contents']['transition'] = "none"
        try:
            aux = tree['substates']
            component['substates'] = []
        except:
            component['substates'] = "none"
        if component['substates'] != "none":
            for sub in tree['substates']:
                a = {}
                # a['name'] = sub['name']
                try:
                    a['parallel'] = sub['parallel']
                except:
                    a['parallel'] = "none"
                try:
                    a['parent'] = sub['parent'][0]
                except:
                    print"Error missing parent"
                    exit(1)
                a['contents'] = {}
                a['contents']['states'] = sub['contents']['states']
                try:
                    a['contents']['finalstate'] = sub['contents']['finalstate'][0]
                except:
                    a['contents']['finalstate'] = "none"
                try:
                    a['contents']['initialstate'] = sub['contents']['initialstate'][0]
                except:
                    a['contents']['initialstate'] = "none"
                try:
                    a['contents']['transition'] = sub['contents']['transition']
                except:
                    a['contents']['transition'] = "none"
                component['substates'].append(a)

        return component

#if __name__ == '__main__':
#	SMDSLparsing.fromFile(sys.argv[1])