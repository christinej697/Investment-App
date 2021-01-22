<?php
$file = fopen("states.txt","r");

while(! feof($file))
  {
  echo fgets($file). "<br />";
  }

fclose($file);
?>
