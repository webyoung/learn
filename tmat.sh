#!/bin/sh
#./tmat.sh
myfunc()
{
fna='gtsv/gtr/mtxd.tsv'
t=$1
ln=1
while read lr;do
IFS=' ' read -ra lum <<< "$lr"
la=${lum[0]}
lc=${lum[2]}
for (( i=$ln;  i < la ;  i++))
do
    echo "0" >> gtsv/gtr/mtxda.tsv
done
    ln=1+$i
    echo $lc >> gtsv/gtr/mtxda.tsv
done < $fna
for (( i=$ln; i <= $t; i++))
do
    echo "0" >> gtsv/gtr/mtxda.tsv
done
paste gtsv/gtr/mtxdb.tsv gtsv/gtr/mtxda.tsv > gtsv/gtr/mtxdt.tsv
rm gtsv/gtr/mtxd.tsv gtsv/gtr/mtxda.tsv gtsv/gtr/mtxdb.tsv
mv gtsv/gtr/mtxdt.tsv gtsv/gtr/mtxdb.tsv
}

### Main script starts here
if [ -d 'gtsv/gtr' ]; then
   rm -r gtsv/gtr
fi
fa=gtsv/gn.tsv
mkdir gtsv/gtr
cat $fa | cut -f 2 >> gtsv/gtr/mtxdb.tsv
fb=gtsv/mt.mtx
n=1
while read -r line;do
if [ $n -eq 2 ]; then
    IFS=' ' read -ra num <<< "$line"
    gn=${num[0]}
fi
n=$((n+1));
if [ $n -eq 3 ]; then
      break
fi
done < $fb
sed '1,2d' $fb > gtsv/gtr/mtx.tsv
fc=gtsv/gtr/mtx.tsv
cs=1
while read -r li;do
    IFS=' ' read -ra num <<< "$li"
    if [ $cs != ${num[1]} ]; then
        myfunc $gn
    fi
    cs=${num[1]}
    echo $li>> gtsv/gtr/mtxd.tsv;
done < $fc
myfunc $gn
echo "Gene" >> gtsv/gtr/da.txt
cat gtsv/bc.tsv >> gtsv/gtr/da.txt
cut -f 1 gtsv/gtr/da.txt | paste -s -d "\t" >> gtsv/gtr/tda.txt
cat gtsv/gtr/mtxdb.tsv>>gtsv/gtr/tda.txt
mv gtsv/gtr/tda.txt gtsv/gtr/matrix.tsv
rm gtsv/gtr/mtx.tsv gtsv/gtr/da.txt gtsv/gtr/mtxdb.tsv
