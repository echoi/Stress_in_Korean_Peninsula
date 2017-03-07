#!/usr/bin/env python

def write_prefix(file):
    print >> file, '''<VTKFile type="PolyData" version="0.1" byte_order="LittleEndian">
  <PolyData>'''

def write_postfix(file):
    print >> file, '''</PolyData>
</VTKFile>'''

def write_pieces(outfile, infile):
    # read in all the lines in the inpuf xyz file
    print "\nReading in %s.\n" % (infile.name)
    lines = infile.readlines()

    # store the total number lines
    numLines = len(lines)

    for i in range(numLines):
        # a line starting with '>' marks a line segment or 'Piece'
        if lines[i].startswith(">"):
            # reset the point counter for this segment/Piece.
            count = 0
            # 'j' is a helper index that will mark the number of the next line starting with '>'
            # or the last line.
            j = i + 1
            while j <= numLines-1 and lines[j].startswith(">") == False:
                j = j + 1
            # the number of points in the current Piece.
            count = j - i - 1
            # line nums for the begin and end of data block
            dataBlock_begin = i+1
            dataBlock_end = i+1+count
            # i can be updated to i+count for fast-forwarding
            i = i + count

            # monitoring message
            print "Line %d: Starting to process a line segment '%s' with %d points." % ( dataBlock_begin-1, lines[dataBlock_begin-1].rstrip('\n'), count)

            # Write the prefix for the 'Piece' block
            print >> outfile, '''<Piece NumberOfPoints="%s" NumberOfVerts="0" NumberOfLines="1" NumberOfStrips="0" NumberOfPolys="0">
              <Points>
                <DataArray type="Float32" Name="Points" NumberOfComponents="3" format="ascii">''' % (count)
            # Write the coordinates
            print "\tWriting point coordinates..."
            for np in range(dataBlock_begin,dataBlock_end):
                coords = lines[np].split()
                print >> outfile, "%se3 %se3 %se3" % (coords[0],coords[1],0.0)
            print >> outfile, '''</DataArray>
          </Points>
          <Lines>
            <DataArray type="Int64" Name="connectivity" format="ascii">'''
            print "\tWriting line connectivity..."
            for k in range(count):
                print >> outfile, k,
            print >> outfile, '''
            </DataArray>
            <DataArray type="Int64" Name="offsets" format="ascii">'''
            print "\tWriting offset..."
            print >> outfile, count
            print >> outfile, '''</DataArray>
          </Lines>
        </Piece>'''
    print "\nResults written to %s.\n" % (outfile.name)

if __name__ == "__main__":
    fi = open("coastlines_rot.xyz","r")
    fo = open("coastlines_rot.vtp","w")

    write_prefix(fo)
    write_pieces(fo, fi)
    write_postfix(fo)

    fi.close()
    fo.close()
