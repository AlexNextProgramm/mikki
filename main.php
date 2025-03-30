<?php

$conf = (include __DIR__ . '/config.php');

$outputFile = __DIR__ . '/class/uploads/goood_Moning.wav';
$command = "arecord -f cd -c 1 -t wav -d 4 -r 44000 " . escapeshellarg($outputFile);

exec($command, $output, $returnVar);
exec("aplay \"$outputFile\"");
