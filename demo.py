import console
c = console.Console()
speech = input('Input a sentence:')
res,path = c.rule_match(speech)
c.write_output(speech,res,path)
