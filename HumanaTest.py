#Shipra Arjun 
#05/07/2020


def convert16to8(f_in: str, f_out: str):
    """ Input: .tsv utf-16-le file.
            Output: .tsv utf-8 file"""       
    try:
        with codecs.open(f_in, 'rb', encoding='utf-16-le') as og_Data:
            with open(f_out, 'w', encoding='utf-8') as utf8_Data:  
                read_ogdata = og_Data.readlines()
                for l in read_ogdata:    
                    utf8_Data.write(l.encode('utf-8').decode('utf-8'))
        print('Successful Conversion to UTF-8')   
        return 1
    except:
        print('Error Converting UTF-16 to UTF-8')
        
        
def transformData(f_out: str):
    """ Input: .tsv utf-8 file that is created during convert16to8 method.
        Output: two files- fixedLines.tsv and brokenLines.tsv """
    try:
        with open(f_out, 'r') as input_broken_file:
            with open('fixedLines.tsv', 'w', encoding='utf-8') as output_fixed:
                with open('brokenLines.tsv', 'w', encoding='utf-8') as output_negated:
                    data = input_broken_file.readlines()
    
                    for row in data:
                        entries = row.split('\t')
                        if len(entries) == 5: 
                            output_fixed.write(row)
                        else: 
                            output_negated.write(row)
                            
        print('Outputted fixedLines.tsv and brokenLines.tsv')              
        
    except:
        print('Failed to output files')
                

if __name__ == '__main__':

    import codecs

    #f_in should be in the same dir where this script is running from. outputs will also be saved here
    f_in = 'data.tsv'
    f_out = 'utf8_data.tsv'
    
    #use conver16to8 method to output a utf-8 file equivalent
    dec = convert16to8(f_in, f_out)
  
    #if output of convert16to8 is successful, run the transformData method
    if dec == 1:
        transformData(f_out)   