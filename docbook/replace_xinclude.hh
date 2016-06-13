<?php
// This is a Hack script, not a PHP script. Any resemblance is purely coincidental.
$d = file_get_contents('docbook.xml');
$d = preg_replace_callback('~<xi:include href="([^"]+)" />~', function($m) {
	return file_get_contents($m[1]);
}, $d);
file_put_contents('docbook.tmp.xml', $d);
