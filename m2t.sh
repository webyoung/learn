#!/bin/bash
#m2t.sh
#./m2t.sh matrix.tsv
rm -rf m2t
mkdir m2t
fl=$(head -1 $1)
read -ra nu <<< $fl
for element in ${nu[@]}; do
    echo ${nu[i]} >> m2t/bl.tsv
    ((++i))
done
tail -n +2 >> m2t/blt.tsv
mv m2t/blt.tsv m2t/bl.tsv
cp $1 m2t/ta.txt
tail -n +2 >> m2t/tat.txt
mv m2t/tat.txt m2t/ta.txt
mf=m2t/ta.txt
cut -f1 $mf > m2t/gl.tsv
cut -f1 --complement $mf > m2t/tb.txt
mfa=m2t/tb.txt
a=$(awk '{print NF; exit}' $mfa)
tn=1
for ((i=1; i<=$a; i++));do
   cat $mfa | cut -f $i >> m2t/cutfa.txt
   rn=1
   myf=m2t/cutfa.txt
   while IFS= read -r line; do
      if [ $line != 0 ]; then
         echo "$rn $i $line" >> m2t/mtx.txt;
         tn=$((tn+1));
      fi
      rn=$((rn+1));
   done < $myf
   rm m2t/cutfa.txt
done
rn=$((rn-1));
echo "%%MatrixMarket matrix coordinate integer general" >> m2t/m.mtx
echo "$rn $a $tn">>m2t/m.mtx
cat m2t/mtx.txt>>m2t/m.mtx
rm m2t/mtx.txt m2t/ta.txt  m2t/tb.txt
