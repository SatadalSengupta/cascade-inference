set title "Community: Max edge density; Threshold: Mean of confidence values"
set terminal postscript eps color enhanced "Helvetica" 60 dl 8
set output "max-size_mean_content-count.eps"

set size 3,2
set ylabel "Ratio"
set xlabel "No. of contents introduced"

set yrange[0.000000:1.000000]
set key top right

plot "gnuplot/max-size_mean_content-count.txt" using 2:3 with linespoints lc rgb "blue" lw 30 title "True Positive", "gnuplot/max-size_mean_content-count.txt" using 2:4 with linespoints lc rgb "red" lw 30 title "False Positive", "gnuplot/max-size_mean_content-count.txt" using 2:5 with linespoints lc rgb "green" lw 30 title "Missed Edges"
