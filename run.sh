#!usr/bin/bash
xterm -hold -e "python Lsr.py A 2000 configA.txt" &
xterm -hold -e "python Lsr.py B 2001 configB.txt" &
xterm -hold -e "python Lsr.py C 2002 configC.txt" &
xterm -hold -e "python Lsr.py D 2003 configD.txt" &
xterm -hold -e "python Lsr.py E 2004 configE.txt" &
xterm -hold -e "python Lsr.py F 2005 configF.txt" &
