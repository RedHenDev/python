def parse_file(filename):
    import os
    data = {}
    current_label = None

    with open(os.path.dirname(os.path.abspath(__file__))+'/n1.txt', 'r') as f:
        notes = []
        lines=[]
        for line in f:
            line = line.strip()
            lines.append(line)
            
    for line in range(len(lines)):
      l=lines[line]
      if l.isupper():
        current_label=l
        print('found new label!',current_label)
        try:
          notes=data[current_label]
        except:
          notes=[]
      if '&&' not in l:
        notes.append(l)
      else:
        data[current_label]=notes
        
          
                

    return data

"""
            if line.isupper():
                current_label = line
                newlist = []
                ready_for_new_entry=False
                print('found label!', current_label)
            elif '&&' in line:
                if current_label is not None:
                    data[current_label]newlist.append()
                current_label = None
                ready_for_new_entry=True
            elif current_label is not None:
                newlist.append(line)
          """

n=parse_file('n1.txt')

while True:
  ml=[]
  try:
    ml=n[input('What label?').upper()]
  except:
    a=input('No such label, sorry. Continue (y/n)?')
    if a.lower().strip()=='y': continue
    break
  # First, print report about length of list etc.
  print(len(ml))
  
  for i in range(0,len(ml)):
      print(ml[i])

print('Program exited. Thank you.')