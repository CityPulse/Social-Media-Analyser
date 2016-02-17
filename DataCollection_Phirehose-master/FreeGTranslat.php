<?php
 //taken from http://rupeshpatel.wordpress.com/2012/06/23/usage-of-google-translator-api-for-free/
function curl($url,$params = array(),$is_coockie_set = false)
{
 
if(!$is_coockie_set){
/* STEP 1. let’s create a cookie file */
$ckfile = tempnam ("/tmp", "CURLCOOKIE");
 
/* STEP 2. visit the homepage to set the cookie properly */
$ch = curl_init ($url);
curl_setopt ($ch, CURLOPT_COOKIEJAR, $ckfile);
curl_setopt ($ch, CURLOPT_RETURNTRANSFER, true);
$output = curl_exec ($ch);
}
 
$str = ''; $str_arr= array();
foreach($params as $key => $value)
{
$str_arr[] = urlencode($key)."=".urlencode($value);
}
if(!empty($str_arr))
$str = '?'.implode('&',$str_arr);
 
/* STEP 3. visit cookiepage.php */
 
$Url = $url.$str;
 
$ch = curl_init ($Url);
curl_setopt ($ch, CURLOPT_COOKIEFILE, $ckfile);
curl_setopt ($ch, CURLOPT_RETURNTRANSFER, true);
 
$output = curl_exec ($ch);
return $output;
}
 
 function AutoTranslate($word)
{
$word = urlencode($word);
$url = 'http://translate.google.com/translate_a/t?client=t&text='.$word.'&hl=en&sl=auto&tl=en&multires=1&otf=2&pc=1&ssel=0&tsel=0&sc=1';
$name_en = curl($url);
 
$name_en = explode('"',$name_en);
return  $name_en[1];
}
 
?>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
</head>
<body>
<?php
echo "
 
Danish To English 1
";
echo  AutoTranslate('Aarhusiansk firma bygger Bagmandspolitiets digitale');
echo "
 
Danish To English 2
";
echo AutoTranslate('Jeg spiser Pringles, ser fjernsyn - mens jeg har dårlig samvittighed over at jeg ikke læser til eksamen!');
echo "
 
Dutch To English
";
echo  AutoTranslate('This is a test for en to en tranlsation');

?>
</body>
</html>
