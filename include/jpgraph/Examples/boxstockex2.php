<?php // content="text/plain; charset=utf-8"
// Example of a stock chart
require_once ("jpgraph/jpgraph.php");
require_once ("jpgraph/jpgraph_stock.php");

// Data must be in the format : open,close,min,max,median
$datay = array(
    34,42,27,45,36,
    55,25,14,59,40,
    15,40,12,47,23,
    62,38,25,65,57,
    38,49,32,64,45);

// Setup a simple graph
$graph = new Graph(300,200);
$graph->SetScale("textlin");
$graph->SetMarginColor('lightblue');
$graph->title->Set('Box Stock chart example');
$graph->subtitle->Set('(Indented X-axis)');

// Create a new stock plot
$p1 = new BoxPlot($datay);

// Width of the bars (in pixels)
$p1->SetWidth(9);

// Indent bars so they dont start and end at the edge of the
// plot area
$p1->SetCenter();

// Uncomment the following line to hide the horizontal end lines
//$p1->HideEndLines();

// Add the plot to the graph and send it back to the browser
$graph->Add($p1);
$graph->Stroke();

?>
