<?php
// This is a Hack script, not a PHP script. Any resemblance is purely coincidental.
$d = file_get_contents('report.xml');
$d = preg_replace_callback('~<xi:include href="([^"]+)" />~', function($m) {
	return file_get_contents($m[1]);
}, $d);
file_put_contents('report.tmp.xml', $d);
