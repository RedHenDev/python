def nMap(n, min1, max1, min2, max2):
    return ((n-min1)/(max1-min1))*(max2-min2)+min2

if __name__=='__main__':
    print('Input percent value; this will be mapped to value out of 3.')
    per = float(input('>'))
    print('Thank you. Result is', nMap(per,0,100,0,3), ' :)')
    
