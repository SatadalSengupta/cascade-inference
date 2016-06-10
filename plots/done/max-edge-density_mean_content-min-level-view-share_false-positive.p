set title "FALSE POSITIVE; Community: Max edge density; Threshold: Mean of confidence values"
set terminal postscript eps color enhanced "Helvetica" 40 dl 8
set output "max-edge-density_mean_content-min-level-view-share_false-positive.eps"

set size 3,2
set view map
set dgrid3d
set pal gray
set pm3d interpolate 0,0

set ylabel "Min. content level boost - View"
set xlabel "Min. content level boost - Share"

splot "gnuplot/max-edge-density_mean_content-min-level-view-share.txt" using 2:3:5 with pm3d
