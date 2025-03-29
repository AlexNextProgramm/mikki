<?php

$conf = (include __DIR__ . '/config.php');

$outputFile = __DIR__ . '/class/uploads/sleep.wav';
$command = "arecord -f cd -c 1 -t wav -d 6 -r 44000 " . escapeshellarg($outputFile);

exec($command, $output, $returnVar);
exec("aplay \"$outputFile\"");
