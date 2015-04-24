#!/bin/bash

region=-10/20/30/60
proj=N0/5i
cpt_val='gmt_scripts/temp/polar01.cpt'
cpt_hit='gmt_scripts/temp/haxby100.cpt'
squaresize='0.3i'
gridding='5g5/5g5'
outfile='gmt_scripts/temp/example'
coastres='i'
valueint=0.5


# plot the values themselves
gmt psxy ./gmt_scripts/temp/vals_xyz.txt -R$region -J$proj -K -B$gridding -C$cpt_val -Ss$squaresize >> testmap.ps
gmt pscoast -R -J -D$coastres -K -O -Wthick >> testmap.ps
gmt psscale -P -D9i/2.i/5.5c/0.3c -B$valueint -O -C$cpt_val >> testmap.ps
gs -dBATCH -dNOPAUSE -sDEVICE=jpeg -sOutputFile=$outfile.jpg -r600 testmap.ps


# plot the values with continents in black
gmt psxy ./gmt_scripts/temp/vals_xyz.txt -R$region -J$proj -K -B$gridding -C$cpt_val -Ss$squaresize >> testmap.ps
gmt pscoast -R -J -D$coastres -K -O -Wthick -Gblack >> testmap.ps
gmt psscale -P -D9i/2.i/5.5c/0.3c -B$valueint -O -C$cpt_val >> testmap.ps
gs -dBATCH -dNOPAUSE -sDEVICE=jpeg -sOutputFile=$outfile.cont.jpg -r600 testmap.ps
rm testmap.ps

# plot the hits
gmt psxy ./gmt_scripts/temp/hits_xyz.txt -R$region -J$proj -K -B$gridding -C$cpt_hit -Ss$squaresize >> testmap.ps
gmt pscoast -R -J -D$coastres -K -O -Wthick >> testmap.ps
gmt psscale -P -D9i/2.i/5.5c/0.3c -B10. -O -C$cpt_hit >> testmap.ps
gs -dBATCH -dNOPAUSE -sDEVICE=jpeg -sOutputFile=$outfile.hits.jpg -r600 testmap.ps
rm testmap.ps

# plot the stations that participated in this measurement
gmt psxy ./gmt_scripts/temp/asym_stas.txt -R$region -J$proj -K -B$gridding -Gred -Wthin -St0.075i >> testmap.ps
gmt pscoast -R -J -D$coastres -O -Wthick >> testmap.ps
gs -dBATCH -dNOPAUSE -sDEVICE=jpeg -sOutputFile=$outfile.stations.jpg -r600 testmap.ps
rm testmap.ps


cp gmt_scripts/temp/vals_xyz.txt $outfile.vals.txt
cp gmt_scripts/temp/hits_xyz.txt $outfile.hits.txt
cp gmt_scripts/temp/info_xyz.txt $outfile.info.txt
cp gmt_scripts/temp/asym_stas.txt $outfile.stas.txt