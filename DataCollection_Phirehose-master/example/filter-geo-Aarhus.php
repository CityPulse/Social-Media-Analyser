<?php
require_once('/user/eestf/nf0010/Desktop/SmartCity/Tools/Phirehose-master/lib/Phirehose.php');
require_once('/user/eestf/nf0010/Desktop/SmartCity/Tools/Phirehose-master/lib/OauthPhirehose.php');
include_once "/user/eestf/nf0010/Desktop/SmartCity/Tools/Phirehose-master/constants.php";
require_once('/user/eestf/nf0010/Desktop/SmartCity/Tools/Phirehose-master/utils/dbManager.php');

/**
 * Example of using Phirehose to display a live filtered stream using geo locations
 */
 function curl($url,$params = array(),$is_coockie_set = false){
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
class FilterTrackConsumer extends OauthPhirehose
{

	
	/*
	 * This function will update a DB based on the twitter stream that is received from a particular geo location.
	 * 
	 */

	function AutoTranslate($data) {
		$word = urlencode($data['text']);
		echo $data['text'];
		$url = 'http://translate.google.com/translate_a/t?client=t&text='.$word.'&hl=en&sl=auto&tl=en&multires=1&otf=2&pc=1&ssel=0&tsel=0&sc=1';
		$name_en = curl($url);
		 
		$name_en = explode('"',$name_en);
		
		$date_time = date("Y-m-d H:i:s",strtotime($data["created_at"]));
		
		$box = $data['place']['full_name'] . ': ' . $data['place']['bounding_box']['coordinates'][0][0][0] . ',' . $data['place']['bounding_box']['coordinates'][0][0][1] . ';'.
			 $data['place']['bounding_box']['coordinates'][0][1][0] . ',' . $data['place']['bounding_box']['coordinates'][0][1][1] .';'.
			 $data['place']['bounding_box']['coordinates'][0][2][0] . ','. $data['place']['bounding_box']['coordinates'][0][2][1] .';'.
			 $data['place']['bounding_box']['coordinates'][0][3][0] . ',' . $data['place']['bounding_box']['coordinates'][0][3][1];
			 
		$boxescaped = mysql_escape_string($box);
		$insert_translated_query = "INSERT INTO Tstream VALUES ('".$data['id_str']."', '".$data['user']['id_str']."', '". mysql_escape_string($name_en[1])."', '$date_time', '". $data['place']['bounding_box']['coordinates'][0][0][0] ."', '". $data['place']['bounding_box']['coordinates'][0][0][1] ."', '". $boxescaped ."');";

		echo $insert_translated_query;
		echo "\n";
		//echo "-------------------------->" + $name_en[1] + "\n";
		InsertRow($insert_translated_query);
		return  $name_en[1];
	}
	
	function push_data_to_db($data){
		
		$date_time = date("Y-m-d H:i:s",strtotime($data["created_at"]));
		
		$box = $data['place']['full_name'] . ': ' . $data['place']['bounding_box']['coordinates'][0][0][0] . ',' . $data['place']['bounding_box']['coordinates'][0][0][1] . ';'.
			 $data['place']['bounding_box']['coordinates'][0][1][0] . ',' . $data['place']['bounding_box']['coordinates'][0][1][1] .';'.
			 $data['place']['bounding_box']['coordinates'][0][2][0] . ','. $data['place']['bounding_box']['coordinates'][0][2][1] .';'.
			 $data['place']['bounding_box']['coordinates'][0][3][0] . ',' . $data['place']['bounding_box']['coordinates'][0][3][1];
			 
		$boxescaped = mysql_escape_string($box);
			 
		//$tweet = $data['text'];
		//$insert_query = "INSERT INTO twitterstream values ('".$data['user']['id_str']."','$tweet','".$date_time."','".$data['user']['screen_name']."','".$data['user']['location']."','".$data["coordinates"]["coordinates"][0]."','".$data["coordinates"]["coordinates"][1]."','".$data['id_str']."')";
		$insert_query = "INSERT INTO AarhusTweet VALUES ('".$data['id_str']."', '".$data['user']['id_str']."', '". mysql_escape_string($data['text'])."', '$date_time', '". $data['place']['bounding_box']['coordinates'][0][0][0] ."', '". $data['place']['bounding_box']['coordinates'][0][0][1] ."', '". $boxescaped ."');";
		echo $insert_query;
		//echo "\n";
		InsertRow($insert_query);
		
	}
	
	public function extractLocation($data){
		
		if(strcmp($data['user']['lang'], "en") == 0){
		
			 $box =  $data['place']['full_name'] . ': ' . $data['place']['bounding_box']['coordinates'][0][0][0] . ',' . $data['place']['bounding_box']['coordinates'][0][0][1] . ';'.
			 $data['place']['bounding_box']['coordinates'][0][1][0] . ',' . $data['place']['bounding_box']['coordinates'][0][1][1] .';'.
			 $data['place']['bounding_box']['coordinates'][0][2][0] . ','. $data['place']['bounding_box']['coordinates'][0][2][1] .';'.
			 $data['place']['bounding_box']['coordinates'][0][3][0] . ',' . $data['place']['bounding_box']['coordinates'][0][3][1] . "\n";
		}
	}

  /**
   * Enqueue each status
   *
   * @param string $status
   */
  public function enqueueStatus($status)
  {
    /*
     * In this simple example, we will just display to STDOUT rather than enqueue.
     * NOTE: You should NOT be processing tweets at this point in a real application, instead they should be being
     *       enqueued and processed asyncronously from the collection process.
     */
    $data = json_decode($status, true);
    if (is_array($data) && isset($data['user']['screen_name'])) {
      print $data['user']['screen_name'] . ': ' . urldecode($data['text']) . "\n";
      $this->push_data_to_db($data);
      // $this->AutoTranslate($data);

    }
  }
}


// The OAuth credentials you received when registering your app at Twitter
define("TWITTER_CONSUMER_KEY", "your twitter consumer key");
define("TWITTER_CONSUMER_SECRET", "Your twitter consumer secret");

// The OAuth data for the twitter account
define("OAUTH_TOKEN", "your twitter application token");
define("OAUTH_SECRET", "your twitter application secret");

// Start streaming
$sc = new FilterTrackConsumer(OAUTH_TOKEN, OAUTH_SECRET, Phirehose::METHOD_FILTER);
$sc->setLocations(array(
       array(10.1800, 56.1420, 10.2340, 56.1721), // Aarhus
       //array(10.10, 56.08, 10.28, 56.19), // Aarhus    
       //array(12, 55, 13, 56), // Copenhagen
   ));
$sc->setTrack(array('@StiftenAGF','@jpaarhus','#Aarhus','@AarhusKultur',
			'@smagaarhus','@AarhusNyheder','@AarhusPortaldk','@Aarhus2017',
			'@OpenDataAarhus', '@aarhusupdate','@AskVest','@SundhedOgOmsorg',
			'@ArhusVejr','@aarhus_ints','@AGFFANdk','@AarhusCykelby','@VisitAarhus',
			'@larshaahr',
	));
$sc->setFollow(array( 3601200017,3370065087, 3330970365, 2911388001,
			2706568231,2647614595, 2201213730, 1324132976,1065597596,
			210987829,159110346, 112585923,77749562,38227253, 36040150,
));
$sc->consume();
