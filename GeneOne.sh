#!/bin/bash
#one.sh g.tsv Gata3
#Please pay attention for the tab in the code line
#In a fold, put g.tsv m.mtx and one.sh and qsub file to run it.

myf()
{
cn=0
while read fi1 fi2 fi3
do
if [ $fi1 -eq $1 ]; then
  echo "$fi1	$fi2	$fi3" >> res/fin.txt
fi
done < res/m.txt
cbg
}

cbg()
{
mkdir res/cb
while read c1 c2 c3
 do
  cn=0
  while read f1 f2 f3
  do
  if [ $f2 -eq $c2 ]; then
    echo "$f1	$f2	$f3" >> res/cb/"$c2".txt
  fi
  done < res/m.txt
done < res/fin.txt
fcg
}

fxg()
{
while read a
do
head -n $a res/gl.txt | tail -1 >> res/fx.txt
done < res/fc.txt
lsma
}

fcg()
{
a=$(ls res/cb)
eval "ar=($a)"
for x in "${ar[@]}"
do
while read f1 f2 f3
do
echo "$f1" >> res/fa.txt
done < res/cb/"$x"
done
sort -n res/fa.txt | uniq >> res/fc.txt
rm res/fa.txt
fxg
}

lsma()
{
rm -rf res/abc
mkdir res/abc
cp res/fx.txt res/abc/gl.txt
echo "Code	ID	Syno" >> res/abc/glo.txt
while read f1 f2 f3 f4
do
echo "$f1	$f2	$f3" >> res/abc/glo.txt
done < res/abc/gl.txt
echo "total count	...	..." >> res/abc/glo.txt
a=$(ls res/cb)
eval "ar=($a)"
cei=1
for x in "${ar[@]}"
do
rm -f res/abc/gls.txt res/abc/ft.txt
cp res/abc/gl.txt res/abc/gls.txt
echo "Cell $cei" >> res/abc/ft.txt
tn=0
while read cl1 cl2 cl3
do
ln=0
while read fl1 fl2
do
ln=$(( ln + 1 ))
if [ $cl1 -gt $fl1 ]; then
echo "0" >> res/abc/ft.txt
fi
if [ $fl1 -eq $cl1 ]; then
tn=$(( tn + 1 ))
echo "$cl3" >> res/abc/ft.txt
break
fi
done < res/abc/gls.txt
ln=$(( ln + 1 ))
tail -n +"$ln" res/abc/gls.txt >> res/abc/glr.txt
rm res/abc/gls.txt
mv res/abc/glr.txt res/abc/gls.txt
done < res/cb/$x
while read h1 h2
do
echo "0" >> res/abc/ft.txt
done < res/abc/gls.txt
echo $tn >> res/abc/ft.txt
paste res/abc/glo.txt res/abc/ft.txt >> res/abc/res.txt
mv res/abc/res.txt res/abc/glo.txt
cei=$(( cei + 1 ))
done
lag
}

lag()
{
mkdir res/ac
tail -n +2 res/abc/glo.txt >> res/ac/g.txt
cp ../gl/glbod.txt res/ac/d.txt
while read cf1 cf2 cf3
do
n=1
while read fc1 fc2 fc3 fc4
do
if [ $fc1 -eq $cf1 ]; then
echo "$fc4" >> res/ac/ga.txt
n=$(( n + 1 ))
tail -n +"$n" res/ac/d.txt >> res/ac/dt.txt
mv res/ac/dt.txt res/ac/d.txt
break
fi
n=$(( n + 1 ))
done < res/ac/d.txt
done < res/ac/g.txt
echo "Name" >> res/ac/gb.txt
cat res/ac/ga.txt >> res/ac/gb.txt
echo "..." >> res/ac/gb.txt
cut -f 4- res/abc/glo.txt >> res/ac/gc.txt
cut -f 1-3 res/abc/glo.txt >> res/ac/ge.txt
paste res/ac/ge.txt res/ac/gb.txt res/ac/gc.txt >> res/ac/gd.txt
}

rm -rf res
mkdir res results
cn=1
while read f1 f2
do
  echo "$cn	$f1	$f2" >> res/gl.txt
  cn=$((cn+1))
done < $1
tail -n +3 m.mtx >> res/m.txt
gn=1
while read f1 f2
do
   if test "$f2" = "$2"
      then
      myf $gn
   fi
gn=$((gn+1))
done < $1
cp res/ac/gd.txt results/glist.txt
rm -r res
