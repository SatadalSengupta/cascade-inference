set title "MISSED EDGES; Community: Max edge density; Threshold: Mean of confidence values"
set terminal postscript eps color enhanced "Helvetica" 40 dl 8
set output "max-edge-density_mean_view-share-prob-mean-stdv_missed-edges.eps"

set size 3,2
set view map
set dgrid3d
set pal gray
set pm3d interpolate 0,0

set xrange[0.3:0.7]
set yrange[0.1:0.2]
set ylabel "View-share probability - Mean"
set xlabel "View-share probability - Standard Deviation"

splot "gnuplot/max-edge-density_mean_view-share-prob-mean-stdv.txt" using 2:3:6 with pm3d
