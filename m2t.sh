#!/bin/bash
#m2t.sh
#./m2t.sh matrix.tsv
if [ -d 'm2t' ]; then
   rm -r m2t
fi
mkdir m2t
fl=$(sed -n '1p' $1)
read -ra nu <<< $fl
for element in ${nu[@]}; do
    echo ${nu[i]} >> m2t/bl.tsv
    ((++i))
done
sed -i '1d' m2t/bl.tsv
cp $1 m2t/ta.txt
mf=m2t/ta.txt
sed -i '1d' $mf
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
