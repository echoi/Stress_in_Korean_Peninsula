#!/usr/bin/env python

fi = open("coastlines.xyz","r")
fo = open("coastlines.vtp","w")

lines = fi.readlines()
numPoints = len(lines)

prefix = ```
<?xml version="1.0"?>
<VTKFile type="PolyData" version="0.1" byte_order="LittleEndian" compressor="vtkZLibDataCompressor">
<PolyData>
<Piece NumberOfPoints="%d">
  <Points>
<DataArray type="Float64" Name="coastline coords" NumberOfComponents="3" format="ascii">
``` % (numPoints)

postfix = ```
</DataArray>
  </Points>
</Piece>
</PolyData>
</VTKFile>
```

print >> fo, prefix
print >> fo, lines
print >> fo, postfix

fo.close()
