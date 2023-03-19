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
        print('found new label!',l.strip())
        # Is it just an additional label, though?
        # If so, ideally make multiple entries.
        # However, for now, we'll just keep the
        # leading label.
        if current_label is None:
          current_label=l.strip()
        try:
          # What list of notes do we already have for
          # this label?
          # Try fails if first of its kind.
          notes=data[current_label]
        except:
          # This means first label of its kind.
          notes=[]
      if '&&' not in l and current_label is not None:
        # Note we only append if working under a
        # current label. To prevent unwanted scoops.
        notes.append(l)
      else:
        # Dump total list of notes so far into
        # current label.
        data[current_label]=notes
        # Remember that current label needs to
        # be emptied, else we'll scoop unwanted
        # next lines if they're unlabelled.
        current_label=None

        
          
                

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