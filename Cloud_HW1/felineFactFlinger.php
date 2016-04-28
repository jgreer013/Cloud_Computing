<?php
function felineFactFlinger() {
  $facts = file("Catfacts2.csv", FILE_IGNORE_NEW_LINES);
  $line_num = rand(0, count($facts)-1);
  echo $facts[$line_num];
}
felineFactFlinger();
?>
