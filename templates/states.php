<?php
  $fn = fopen("states.txt","r");
  
  while(! feof($fn))  {
	$result = fgets($fn);
	echo $result;
  }

  fclose($fn);
?>
