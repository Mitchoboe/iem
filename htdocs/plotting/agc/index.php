<?php 
include("../../../config/settings.inc.php");
include_once "../../../include/myview.php";
$t = new MyView();
$t->title = "ISU Ag Plotting";
$t->thispage="networks-agclimate";

$t->content = <<<EOF

<p>This application is no longer maintained, please see <a href="/plotting/auto/?q=177">automated data plotting</a> instead.</p>

EOF;
$t->render('single.phtml');
?>
